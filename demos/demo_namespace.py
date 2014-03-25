from planout.experiment import SimpleExperiment
from planout.ops.random import *
from planout.assignment import Assignment
import inspect
import hashlib

def a_func(params, userid):
  params.button_color = UniformChoice(choices=[1,2,3], unit=userid)

def b_func(params, userid):
  params.button_color = UniformChoice(choices=[1,2,3], unit=userid)

def c_func(params, userid):
  params.button_color = UniformChoice(choices=[3,4,5], unit=userid)
  params.text_color = UniformChoice(choices=['a','b'], unit=userid)


class SimpleNamespace(SimpleExperiment):
  experiments = {
    'exp1': {'func': a_func},
    'exp2': {'func': a_func},
    'exp3': {'func': b_func},
    'exp4': {'func': c_func}}

  @staticmethod
  def checksum_func(func):
    # src doesn't count first line of code, which includes function name
    src = ''.join(inspect.getsourcelines(func)[0][1:])
    return hashlib.sha1(src).hexdigest()[:8]

  def assign(self, params, **kwargs):
    a = Assignment('my_namespace')
    a.experiment_name = WeightedChoice(
      choices=['exp1', 'exp2', 'exp3', 'exp4', None],
      weights=[0.1, 0.2, 0.2, 0.2, 0.3],
      unit=kwargs['userid'])

    self._checksum = None
    if a.experiment_name is not None:
      self.salt = '%s.%s' % (self.salt, a.experiment_name)
      self.name = a.experiment_name
      proc = Assignment(self.salt)
      my_exp = self.experiments[a.experiment_name]['func']
      self._checksum = self.checksum_func(my_exp)

      my_exp(proc, kwargs)
      params.update(proc)

    else:
      self.in_experiment = False  # turns off auto-exposure logging
      # would this work for other kvs?
      params.update(self.default_value_store())

  def default_value_store(self):
    return {'button_color': 6, 'text': 'ahoy there!'}

for i in range(10):
  print SimpleNamespace(userid=i)
