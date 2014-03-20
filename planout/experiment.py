# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import logging
import re
from abc import ABCMeta, abstractmethod

class Experiment(object):
  """Abstract base class for PlanOut experiments"""
  __metaclass__ = ABCMeta

  logger_configured = False

  def __init__(self, **inputs):
    self.inputs = inputs       # input data
    self.params = None         # stores parameter assignment results
    self.mapper = None    # stores instance of the PlanOut mapper
    self._logged = False       # True when assignments have been exposure logged
    self._salt = None          # Experiment-level salt
    self._name = None          # Name of the experiment
    self._in_experiment = True

    self.setExperimentProperties()          # sets name, salt, etc.
    self.configureLogger()                  # sets up loggers
    self.__assign()                         # assign inputs to parameters

    # check if inputs+params were previously logged
    self._logged = self.previouslyLogged()

    # auto-exposure logging is enabled by default
    self._auto_exposure_log = True


  def setExperimentProperties(self):
    """Set experiment properties, e.g., experiment name and salt."""
    # If the experiment name is not specified, just use the class name
    self.name = self.__class__.__name__

  @property
  def salt(self):
    # use the experiment name as the salt if the salt is not set
    return self._salt if self._salt else self.name

  @salt.setter
  def salt(self, value):
    self._salt = value

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = re.sub(r'\s+', '-', value)

  def in_experiment(self):
    return self._in_experiment

  def __assign(self):
    """Execute assignment procedure and set parameters"""
    # exp must implement basic PlanOut methods
    self.mapper = \
        self.execute(**self.inputs)
    self.params = self.mapper.getParams()
    self._in_experiment = self.params.get('in_experiment', True)
    return self

  @abstractmethod
  def execute(**kwargs):
    """Returns evaluated PlanOut mapper with experiment assignment"""
    pass

  def __asBlob(self, extras={}):
    """Dictionary representation of experiment data"""
    d = {
      'name': self.name,
      'salt': self.salt,
      'inputs': self.inputs,
      'params': self.params
    }
    for k in extras:
      d[k] = extras[k]
    return d

  # the logged setter / getter may be unnecessary
  @property
  def logged(self):
    return self._logged

  @logged.setter
  def logged(self, value):
    self._logged = value

  def setAutoExposureLogging(self, value):
    """
    Disables / enables auto exposure logging (enabled by default).
    """
    self._auto_exposure_log = value

  def getParams(self):
    """
    Get all PlanOut parameters. Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment() and not self.logged:
      self.logExposure()
    return self.mapper.getParams()

  def get(self, name, default=None):
    """
    Get PlanOut parameter (returns default if undefined). Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment() and not self.logged:
      self.logExposure()
    return self.mapper.get(name, default)

  def __str__(self):
    """
    String representation of exposure log data. Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment() and not self.logged:
      self.logExposure()
    return str(self.__asBlob())

  def logExposure(self, extras={}):
    """Manual call to log exposure"""
    self.logged = True
    if extras:
      exta_payload = dict(extras.items() + ('event', 'exposure'))
    else:
      extra_payload = extras
    self.log(self.__asBlob(extra_payload))

  def logOutcome(self):
    """Log outcome event"""
    self.logged = True
    exta_payload = dict(extras.items() + ('event', 'outcome'))
    self.log(self.__asBlob(extra_payload))

  @abstractmethod
  def configureLogger(self):
    """Set up files, database connections, sockets, etc for logging."""
    pass

  @abstractmethod
  def log(self, data):
    """Log experimental data"""
    pass

  @abstractmethod
  def previouslyLogged(self):
    """Check if the input has already been logged.
       Gets called once during in the constructor."""
    # For high-use applications, one might have this method to check if
    # there is a memcache key associated with the checksum of the inputs+params
    pass

class SimpleExperiment(Experiment):
  """Simple experiment base class which exposure logs to a file"""

  # We only want to set up the logger once, the first time the object is
  # instantiated. We do this by maintaining this class variable.
  _logger_configured = False

  def configureLogger(self):
    """Sets up logger to log to experiment_name.log"""
    # only want to set logging handler once
    if not self.__class__._logger_configured:
      self.__class__.logger = logging.getLogger(self.name)
      self.__class__.logger.setLevel(logging.INFO)
      self.__class__.logger.addHandler(logging.FileHandler('%s.log' % self.name))
      self.__class__._logger_configured = True


  def log(self, data):
    """Logs data to a file"""
    self.__class__.logger.info(data)

  def previouslyLogged(self):
    """Check if the input has already been logged.
       Gets called once during in the constructor."""
    # SimpleExperiment doesn't connect with any services, so we just assume
    # that if the object is a new instance, this is the first time we are
    # seeing the inputs/outputs given.
    return False
