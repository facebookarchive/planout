# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from copy import deepcopy
from .ops.utils import Operators


Operators.initFactory()

class Interpreter(object):
  """PlanOut interpreter"""

  def __init__(self, serialization, experiment_salt='global_salt', inputs={}):
    self._serialization = serialization
    self._env = {}
    self._overrides = {}
    self.experiment_salt = self._experiment_salt = experiment_salt
    self._evaluated = False
    self._inputs = inputs.copy()


  def get_params(self):
    """Get all assigned parameter values from an executed interpreter script"""
    # evaluate code if it hasn't already been evaluated
    if not self._evaluated:
      self.evaluate(self._serialization)
      self._evaluated = True
    return self._env

  def set_env(self, new_env):
    """Replace the current environment with a dictionary"""
    self._env = deepcopy(new_env)
    # apply overrides
    for v in self._overrides:
      self._env[v] = self._overrides[v]
    return self

  def has(self, name):
    """Check if a variable exists in the PlanOut environment"""
    return name in self._env

  def get(self, name, default=None):
    """Get a variable from the PlanOut environment"""
    return self._env.get(name, self._inputs.get(name, default))

  def set(self, name, value):
    """Set a variable in the PlanOut environment"""
    self._env[name] = value
    return self

  def set_overrides(self, overrides):
    """
    Sets variables to maintain a frozen state during the interpreter's
    execution. This is useful for debugging PlanOut scripts.
    """
    Operators.enable_overrides()
    self._overrides = overrides
    self.set_env(self._env)  # this will reset overrides
    return self

  def has_override(self, name):
    """Check to see if a variable has an override."""
    return name in self._overrides

  def get_overrides(self):
    """Get a dictionary of all overrided values"""
    return self._overrides

  def evaluate(self, planout_code):
    """Recursively evaluate PlanOut interpreter code"""
    # if the object is a PlanOut operator, execute it it.
    if Operators.isOperator(planout_code):
      return Operators.operatorInstance(planout_code).execute(self)
    # if the object is a list, iterate over the list and evaluate each element
    elif type(planout_code) is list:
      return [self.evaluate(i) for i in planout_code]
    else:
      return planout_code  # data is a literal


class Validator():
  """
  Inspects and validates serialized PlanOut experiment definitions.
  This can be used by management systems for validating JSON scripts
  and printing them in human readable "pretty" format.
  """
  def __init__(self, serialization):
    self._serialization = serialization

  def validate(self):
    """validate PlanOut serialization"""
    config = self._serialization
    return Operators.validateOperator(config)

  def pretty(self):
    """pretty print PlanOut serialization as PlanOut language code"""
    config = self._serialization
    return Operators.operatorInstance(config).pretty()

  def get_variables(self):
    """get all variables set by PlanOut script"""
    pass

  def get_input_variables(self):
    """get all variables used not defined by the PlanOut script"""
    pass
