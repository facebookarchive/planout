# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from ops.random import *
from mapper import PlanOutMapper


class PlanOutKitMapper(PlanOutMapper):
  def __init__(self, experiment_salt):
    self.experiment_salt = experiment_salt

  def evaluate(self, value):
    return value

  def __setattr__(self, name, value):
    if isinstance(value, PlanOutOpRandom):
      if 'salt' not in value.args:
        value.args['salt'] = name
      self.__dict__[name] = value.execute(self)
    else:
      self.__dict__[name] = value

  def __getattr__(self, name):
    return self.get(name, None)

  def get(self, name, default=None):
    return self.__dict__.get(name, default)

  def getParams(self):
    d = self.__dict__
    return dict([(i, d[i]) for i in d if i != 'experiment_salt'])

  def __str__(self):
    return str(self.getParams())
