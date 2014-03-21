# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
from copy import deepcopy
from ops.utils import Operators
from mapper import PlanOutMapper


Operators.initFactory()

class PlanOutInterpreterMapper(PlanOutMapper):
  """PlanOut interpreter"""

  def __init__(self, serialization, experiment_salt='global_salt'):
    self._serialization = serialization
    self._env = {}
    self._overrides = {}
    self._experiment_salt = experiment_salt
    self._evaluated = False

  def getParams(self):
    if not self._evaluated:
      self.evaluate(self._serialization)
      self._evaluated = True
    return self._env

  def setEnv(self, new_env):
    self.env = deepcopy(new_env)
    for v in self._overrides:
      self._env[v] = self._overrides[v]
    return self

  def has(self, name):
    return name in self._env

  def get(self, name, default=None):
    if not self._evaluated:
      self.evaluate(self._serialization)
      self._evaluated = True
    return self._env.get(name, default)

  def set(self, name, value):
    self._env[name] = value
    return self

  def setOverrides(self, overrides):
    Operators.enableOverrides()
    self._overrides = overrides
    self.setEnv(self._env)  # this will reset overrides
    return self

  def hasOverride(self, name):
    return name in self._overrides

  def getOverrides(self):
    return self._overrides

  def evaluate(self, data):
    if Operators.isOperator(data):
      return Operators.operatorInstance(data).execute(self)
    else:
      return data  # data is a literal

  def validate(self):
    config = self._serialization
    return Operators.validateOperator(config)

  def pretty(self):
    config = self._serialization
    return Operators.operatorInstance(config).pretty()