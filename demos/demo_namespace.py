from planout.experiment import SimpleExperiment
from planout.ops.random import *
from planout.assignment import Assignment
import inspect
import hashlib
from operator import itemgetter
from abc import ABCMeta, abstractmethod

class SimpleNamespace(SimpleExperiment):
  __metaclass__ = ABCMeta

  @abstractmethod
  def set_experiment_properties(self):
    self.experiments = {} # list of lists of functions
    self.primary_key = [None] # must set primary key of namespace


  @staticmethod
  def checksum_func(func):
    # src doesn't count first line of code, which includes function name
    src = ''.join(inspect.getsourcelines(func)[0][1:])
    return hashlib.sha1(src).hexdigest()[:8]

  def assign(self, params, **kwargs):
    self.experiment_names = self.experiments.keys()
    self.experiment_weights = [v['prop'] for k,v in self.experiments.items()]
    assert(sum(self.experiment_weights) <= 1.0)
    if sum(self.experiment_weights) < 1.0:
      self.experiment_names += [None]
      self.experiment_weights += [1.0 - sum(self.experiment_weights)]

    a = Assignment(self.salt)
    a.experiment_name = WeightedChoice(
      choices=self.experiment_names,
      weights=self.experiment_weights,
      unit=itemgetter(*self.primary_keys)(kwargs))

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


def a_func(params, userid):
  params.button_color = UniformChoice(choices=[1,2,3], unit=userid)

def b_func(params, userid):
  params.button_color = UniformChoice(choices=[1,2,3], unit=userid)

def c_func(params, userid):
  params.button_color = UniformChoice(choices=[3,4,5], unit=userid)
  params.text_color = UniformChoice(choices=['a','b'], unit=userid)

class DemoNamespace(SimpleNamespace):
  def set_experiment_properties(self):
    self.experiments = {
      'exp1': {'func': a_func, 'prop': 0.1},
      'exp2': {'func': a_func, 'prop': 0.2},
      'exp3': {'func': b_func, 'prop': 0.2},
      'exp4': {'func': c_func, 'prop': 0.2}}
    self.primary_keys = ['userid']
    self.name = 'DemoNamespace'
    self.salt = 'DemoNamespace'

  def default_value_store(self):
    return {'button_color': 6, 'text': 'ahoy there!'}

for i in range(10):
  print DemoNamespace(userid=i)
