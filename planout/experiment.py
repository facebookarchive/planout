# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import logging
import time
import re
import json
import inspect
import hashlib
from abc import ABCMeta, abstractmethod
import __main__ as main

from .assignment import Assignment


# decorator for methods that assume assignments have been made
def requires_assignment(f):
  def wrapped_f(self, *args, **kwargs):
    if not self._assigned:
      self._assign()
    return f(self, *args, **kwargs)
  return wrapped_f

# decorator for methods that should be exposure logged
def requires_exposure_logging(f):
  def wrapped_f(self, *args, **kwargs):
    if self._auto_exposure_log and self.in_experiment and not self.exposure_logged:
      self.log_exposure()
    return f(self, *args, **kwargs)
  return wrapped_f

class Experiment(object):
  """Abstract base class for PlanOut experiments"""
  __metaclass__ = ABCMeta

  logger_configured = False

  def __init__(self, **inputs):
    self.inputs = inputs           # input data
    self._exposure_logged = False  # True when assignments have been exposure logged
    self._salt = None              # Experiment-level salt
    self.in_experiment = True

    # use the name of the class as the default name
    self._name = self.__class__.__name__

    # auto-exposure logging is enabled by default
    self._auto_exposure_log = True

    self.setup()                   # sets name, salt, etc.

    self._assignment = self.get_assignment()
    self._checksum = self.checksum()
    self._assigned = False

  def _assign(self):
    """Assignment and setup that only happens when we need to log data"""
    self.configure_logger() # sets up loggers
    self.assign(self._assignment, **self.inputs)
    self.in_experiment = \
      self._assignment.get('in_experiment', self.in_experiment)
    # check if inputs+params were previously logged
    self._logged = self.previously_logged()

  def setup(self):
    """Set experiment attributes, e.g., experiment name and salt."""
    # If the experiment name is not specified, just use the class name
    pass

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

  @requires_assignment
  def __asBlob(self, extras={}):
    """Dictionary representation of experiment data"""
    d = {
      'name': self.name,
      'time': int(time.time()),
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
    # if we're running from a file and want to detect if the experiment file has changed
    if hasattr(main, '__file__'):
      # src doesn't count first line of code, which includes function name
      src = ''.join(inspect.getsourcelines(self.assign)[0][1:])
      return hashlib.sha1(src).hexdigest()[:8]
    # if we're running in an interpreter, don't worry about it
    else:
      return None

  @property
  def exposure_logged(self):
    return self._exposure_logged

  @exposure_logged.setter
  def exposure_logged(self, value):
    self._exposure_logged = value

  def set_auto_exposure_logging(self, value):
    """
    Disables / enables auto exposure logging (enabled by default).
    """
    self._auto_exposure_log = value

  @requires_assignment
  @requires_exposure_logging
  def get_params(self):
    """
    Get all PlanOut parameters. Triggers exposure log.
    """
    # In general, this should only be used by custom loggers.
    return dict(self._assignment)

  @requires_assignment
  @requires_exposure_logging
  def get(self, name, default=None):
    """
    Get PlanOut parameter (returns default if undefined). Triggers exposure log.
    """
    return self._assignment.get(name, default)

  @requires_assignment
  @requires_exposure_logging
  def __str__(self):
    """
    String representation of exposure log data. Triggers exposure log.
    """
    return str(self.__asBlob())

  def log_exposure(self, extras=None):
    """Logs exposure to treatment"""
    self.exposure_logged = True
    self.log_event('exposure', extras)

  def log_event(self, event_type, extras=None):
    """Log an arbitrary event"""
    if extras:
      extra_payload = {'event': event_type, 'extra_data': extras.copy()}
    else:
      extra_payload = {'event': event_type}
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


class DefaultExperiment(Experiment):
  """
  Dummy experiment which has no logging. Default experiments used by namespaces
  should inherent from this class.
  """
  def configure_logger(self):
    pass  # we don't log anything when there is no experiment

  def log(self, data):
    pass

  def previously_logged(self):
    return True

  def assign(self, params, **kwargs):
    # more complex default experiments can override this method
    params.update(self.get_default_params())

  def get_default_params(self):
    """
    Default experiments that are just key-value stores should
    override this method."""
    return {}

class SimpleExperiment(Experiment):
  """Simple experiment base class which exposure logs to a file"""

  __metaclass__ = ABCMeta
  # We only want to set up the logger once, the first time the object is
  # instantiated. We do this by maintaining this class variable.
  logger = {}
  log_file = {}

  def configure_logger(self):
    """Sets up logger to log to a file"""
    my_logger = self.__class__.logger
    # only want to set logging handler once for each experiment (name)
    if self.name not in self.__class__.logger:
      if self.name not in self.__class__.log_file:
        self.__class__.log_file[self.name] = '%s.log' % self.name
      file_name = self.__class__.log_file[self.name]
      my_logger[self.name] = logging.getLogger(self.name)
      my_logger[self.name].setLevel(logging.INFO)
      my_logger[self.name].addHandler(logging.FileHandler(file_name))
      my_logger[self.name].propagate = False

  def log(self, data):
    """Logs data to a file"""
    self.__class__.logger[self.name].info(json.dumps(data))

  def set_log_file(self, path):
    self.__class__.log_file[self.name] = path

  def previously_logged(self):
    """Check if the input has already been logged.
       Gets called once during in the constructor."""
    # SimpleExperiment doesn't connect with any services, so we just assume
    # that if the object is a new instance, this is the first time we are
    # seeing the inputs/outputs given.
    return False
