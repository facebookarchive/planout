# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from abc import ABCMeta, abstractmethod

class PlanOutMapper:
  """Abstract base class for PlanOut Mappers"""
  __metaclass__ = ABCMeta

  @property
  def experiment_salt(self):
    # use the experiment name as the salt if the salt is not set
    return self._experiment_salt

  @experiment_salt.setter
  def experiment_salt(self, value):
    self._experiment_salt = value

  @abstractmethod
  def get(self, name, default=None):
    pass

  @abstractmethod
  def getParams(self):
    pass

  def evaluate(self, value):
    return value
