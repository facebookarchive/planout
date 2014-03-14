import logging
from abc import ABCMeta, abstractmethod

class ExperimentBase(object):
  __metaclass__ = ABCMeta

  def __init__(self, **inputs):
    self.params = None
    self.exp = None
    self.inputs = inputs
    self.configureLogger()
    self.__assign()

  def __assign(self):
    # exp must implement basic PlanOut methods
    self.exp = self.execute(**self.inputs)
    self.params = self.exp.getParams()
    return self

  def __asBlob(self, extras={}):
    # represent data to log as a dictionary
    d = {
      'inputs': self.inputs,
      'params': self.params
    }
    for k in extras:
      d[k] = extras[k]
    return d

  def getParams(self):
    if not self.alreadyLogged():
      self.logExposure()
    return self.exp.getParams()

  def get(self, name, default=None):
    if not self.alreadyLogged():
      self.logExposure()
    return self.exp.get(name, default)

  def __str__(self):
    return str(self.__asBlob())

  # not sure if this should be private.
  def logExposure(self):
    self.logged = True
    self.log(self.__asBlob({'event': 'exposure'}))

  def logOutcome(self):
    self.logged = True
    self.log(self.__asBlob({'event': 'outcome'}))

  @abstractmethod
  def configureLogger(self):
    pass

  @abstractmethod
  def log(self, data):
    pass

  @abstractmethod
  def alreadyLogged(self):
    """check if the input has already been logged"""
    # for high-use applications, one might have this method to check if
    # there is a memcache key associated with the checksum of the inputs+params
    pass

class SimpleExperiment(ExperimentBase):
  def configureLogger(self):
    """sets up logger"""
    # For the base experiment class we just log using logging
    # to standard out. We could instead log to a file, e.g.,
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)
    self.logged = False
    logging.basicConfig(level=logging.DEBUG)

  def log(self, data):
    # alternative loggers may write to a database or thrift
    logging.info(data)

  def alreadyLogged(self):
    return self.logged
