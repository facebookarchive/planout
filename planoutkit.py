from ops.random import *
from ops.core import PlanOutOp
from planout import PlanOut

class PlanOutExperiment:
  def __init__(self, experiment_salt):
    self.exp = PlanOut({})
    self.exp.set('global_salt', experiment_salt)

  def __setattr__(self, name, value):
    if isinstance(value, PlanOutOp): 
      if 'salt' not in value.args:
        value.args['salt'] = name
      self.__dict__[name] = value.execute(self.exp)
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    if name in self.__dict__:
      return self.__dict__[name]
    else:
      return None

  def get_params(self):
    d = self.__dict__
    return dict([(i, d[i]) for i in d if i != 'exp'])

  def __str__(self):
    return str(self.get_params())


class PlanOutQE(PlanOutExperiment):
  def __init__(self, experiment_salt):
    self.e = PlanOutExperiment(experiment_salt)

  def setLogger(self, logger):
    pass

  def logExposure(self):
    pass

  def logOutcome(self):
    pass

  def get_params(self):
    self.e.get_params()

  def __str__(self):
    return str(self.get_params())

def experiment(name):
  def wrap(f):
    def wrapped_f(**kwargs):
      e = PlanOutExperiment(name)
      e.input = kwargs
      return f(e, **kwargs)
    return wrapped_f
  return wrap 
