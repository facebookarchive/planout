# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from abc import ABCMeta, abstractmethod

class Mapper:
  """Abstract base class for PlanOut Mappers"""
  __metaclass__ = ABCMeta


  @property
  def experiment_salt(self):
    return self._experiment_salt

  @experiment_salt.setter
  def experiment_salt(self, value):
    self._experiment_salt = value

  def evaluate(self, value):
    # Custom evaluation may be implemented here if values are computed lazily
    # (i.e. in the case of the PlanOut interpreter).
    return value

  @abstractmethod
  def get(self, name, default=None):
    pass

  @abstractmethod
  def get_params(self):
    pass
