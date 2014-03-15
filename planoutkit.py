from ops.random import *
from ops.core import PlanOutOp
from planout import PlanOutInterpreterMapper
import logging
from experiment import SimpleExperiment

class PlanOutKitMapper:
  def __init__(self, experiment_salt):
    self.interpreter = PlanOutInterpreterMapper({})
    self.interpreter.set('global_salt', experiment_salt)

  def __setattr__(self, name, value):
    if isinstance(value, PlanOutOp): 
      if 'salt' not in value.args:
        value.args['salt'] = name
      self.__dict__[name] = value.execute(self.interpreter)
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    return self.get(name, None)

  def get(self, name, default=None):
    return self.__dict__.get(name, default)

  def getParams(self):
    d = self.__dict__
    return dict([(i, d[i]) for i in d if i != 'interpreter'])

  def __str__(self):
    return str(self.getParams())

## deprecated...
# in case you don't need QE fanciness
def experiment_decorator(name):
  def wrap(f):
    def wrapped_f(**kwargs):
      e = PlanOutKitMapper(name)
      e.input = kwargs
      return f(e, **kwargs)
    return wrapped_f
  return wrap 



class myExample(SimpleExperiment):
  def execute(self, userid, pageid):
    e = PlanOutKitMapper(self.salt)
    e.foo = UniformChoice(choices=["red", "blue"], unit=userid)
    e.bar = BernoulliTrial(p=0.5, unit=pageid)
    return e

class myExample2(SimpleExperiment):
  def setExperimentProperties(self):
    self.salt = 'blah'
    self.name = 'my_experimenT_name'

  def execute(self, userid, pageid):
    e = PlanOutKitMapper(self.salt)
    e.foo = UniformChoice(choices=["red", "blue"], unit=userid)
    e.bar = BernoulliTrial(p=0.5, unit=pageid)
    return e



class NamespaceExperimentProvider(SimpleExperiment):
  def execute(self, namespace, **kwargs):
    e = self.getExperimentForNamespace(namespace, kwargs)
    return e

  def getExperimentForNamespace(self, namespace, userid, pageid):
    e = PlanOutKitMapper(self.salt)
    e.salt = '%s.%s' % (namespace , e.salt)
    e.foo = UniformChoice(choices=["red", "blue"], unit=userid)
    e.bar = BernoulliTrial(p=0.5, unit=pageid)
    return e


#print NamespaceExperimentProvider('bob dylan', userid=1, pageid=2 % 3)
