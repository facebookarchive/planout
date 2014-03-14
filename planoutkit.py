from ops.random import *
from ops.core import PlanOutOp
from planout import PlanOutInterpreter
import logging
from experiment import SimpleExperiment

class PlanOutKit:
  def __init__(self, experiment_salt):
    self.exp = PlanOutInterpreter({})
    self.exp.set('global_salt', experiment_salt)

  def __setattr__(self, name, value):
    if isinstance(value, PlanOutOp): 
      if 'salt' not in value.args:
        value.args['salt'] = name
      self.__dict__[name] = value.execute(self.exp)
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    return self.get(name, None)

  def get(self, name, default=None):
    return self.__dict__.get(name, default)

  def getParams(self):
    d = self.__dict__
    return dict([(i, d[i]) for i in d if i != 'exp'])

  def __str__(self):
    return str(self.getParams())

# in case you don't need QE fanciness
def experiment(name):
  def wrap(f):
    def wrapped_f(**kwargs):
      e = PlanOutKit(name)
      e.input = kwargs
      return f(e, **kwargs)
    return wrapped_f
  return wrap 

class SimpleExample(SimpleExperiment):
  def execute(self, userid, pageid):
    e = PlanOutKit('myhash')
    e.foo = UniformChoice(choices=["red", "blue"], unit=userid)
    e.bar = BernoulliTrial(p=0.2, unit=pageid)
    return e

x = SimpleExample(userid=3, pageid=4)
print x.get('foo'), x.get('bar')
