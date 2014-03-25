# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import logging
import re
from abc import ABCMeta, abstractmethod
import json
import inspect
import hashlib

from .assignment import Assignment

class Experiment(object):
  """Abstract base class for PlanOut experiments"""
  __metaclass__ = ABCMeta

  logger_configured = False

  def __init__(self, **inputs):
    self.inputs = inputs       # input data
    self._logged = False       # True when assignments have been exposure logged
    self._salt = None          # Experiment-level salt
    self._name = None          # Name of the experiment
    self.in_experiment = True
    # auto-exposure logging is enabled by default
    self._auto_exposure_log = True

    self.set_experiment_properties()          # sets name, salt, etc.
    self.configure_logger()                  # sets up loggers

    self._assignment = self.get_assignment()
    self._checksum = self.checksum()
    self.assign(self._assignment, **self.inputs)
    self.in_experiment = \
      self._assignment.get('in_experiment', self.in_experiment)

    # check if inputs+params were previously logged
    self._logged = self.previously_logged()


  def set_experiment_properties(self):
    """Set experiment properties, e.g., experiment name and salt."""
    # If the experiment name is not specified, just use the class name
    self.name = self.__class__.__name__

  def get_assignment(self):
    return Assignment(self.salt)

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

  @abstractmethod
  def assign(params, **kwargs):
    """Returns evaluated PlanOut mapper with experiment assignment"""
    pass

  def __asBlob(self, extras={}):
    """Dictionary representation of experiment data"""
    d = {
      'name': self.name,
      'salt': self.salt,
      'inputs': self.inputs,
      'params': dict(self._assignment),
    }
    for k in extras:
      d[k] = extras[k]
    if self._checksum:
      d['checksum'] = self._checksum
    return d

  def checksum(self):
    # src doesn't count first line of code, which includes function name
    src = ''.join(inspect.getsourcelines(self.assign)[0][1:])
    return hashlib.sha1(src).hexdigest()[:8]

  # the logged setter / getter may be unnecessary
  @property
  def logged(self):
    return self._logged

  @logged.setter
  def logged(self, value):
    self._logged = value

  def set_auto_exposure_logging(self, value):
    """
    Disables / enables auto exposure logging (enabled by default).
    """
    self._auto_exposure_log = value

  def get_params(self):
    """
    Get all PlanOut parameters. Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment and not self.logged:
      self.log_exposure()
    return dict(self._assignment)

  def get(self, name, default=None):
    """
    Get PlanOut parameter (returns default if undefined). Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment and not self.logged:
      self.log_exposure()
    return self._assignment.get(name, default)

  def __str__(self):
    """
    String representation of exposure log data. Triggers exposure log.
    """
    if self._auto_exposure_log and self.in_experiment and not self.logged:
      self.log_exposure()
    return str(self.__asBlob())

  def log_exposure(self, extras={}):
    """Manual call to log exposure"""
    self.logged = True
    if extras:
      exta_payload = dict(extras.items() + ('event', 'exposure'))
    else:
      extra_payload = extras
    self.log(self.__asBlob(extra_payload))

  def log_outcome(self):
    """Log outcome event"""
    self.logged = True
    exta_payload = dict(extras.items() + ('event', 'outcome'))
    self.log(self.__asBlob(extra_payload))

  @abstractmethod
  def configure_logger(self):
    """Set up files, database connections, sockets, etc for logging."""
    pass

  @abstractmethod
  def log(self, data):
    """Log experimental data"""
    pass

  @abstractmethod
  def previously_logged(self):
    """Check if the input has already been logged.
       Gets called once during in the constructor."""
    # For high-use applications, one might have this method to check if
    # there is a memcache key associated with the checksum of the inputs+params
    pass

class SimpleExperiment(Experiment):
  """Simple experiment base class which exposure logs to a file"""

  __metaclass__ = ABCMeta
  # We only want to set up the logger once, the first time the object is
  # instantiated. We do this by maintaining this class variable.
  _logger_configured = False

  def configure_logger(self):
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

  def previously_logged(self):
    """Check if the input has already been logged.
       Gets called once during in the constructor."""
    # SimpleExperiment doesn't connect with any services, so we just assume
    # that if the object is a new instance, this is the first time we are
    # seeing the inputs/outputs given.
    return False
