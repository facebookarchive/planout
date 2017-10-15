# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from .ops.random import *
from .ops.base import PlanOutOp
from collections import MutableMapping


# The Assignment class is the main work horse that lets you to execute
# random operators using the names of variables being assigned as salts.
# It is a MutableMapping, which means it plays nice with things like Flask
# template renders.
class Assignment(MutableMapping):

    """
    A mutable mapping that contains the result of an assign call.
    """

    def __init__(self, experiment_salt, overrides={}):
        self.experiment_salt = experiment_salt
        self._overrides = overrides.copy()
        self._data = overrides.copy()
        self.salt_sep = '.' # separates unit from experiment/variable salt

    def evaluate(self, value):
        return value

    def get_overrides(self):
        return self._overrides

    def set_overrides(self, overrides):
        # maybe this should be a deep copy?
        self._overrides = overrides.copy()
        for var in self._overrides:
            self._data[var] = self._overrides[var]

    def __setitem__(self, name, value):
        if name in ('_data', '_overrides', 'salt_sep', 'experiment_salt'):
            self.__dict__[name] = value
            return

        if name in self._overrides:
            return

        if isinstance(value, PlanOutOpRandom):
            if 'salt' not in value.args:
                value.args['salt'] = name
            self._data[name] = value.execute(self)
        else:
            self._data[name] = value

    __setattr__ = __setitem__

    def __getitem__(self, name):
        if name in ('_data', '_overrides', 'experiment_salt'):
            return self.__dict__[name]
        else:
            return self._data[name]

    __getattr__ = __getitem__

    def __delitem__(self, name):
        del self._data[name]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)
