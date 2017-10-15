# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from copy import deepcopy
from .ops.utils import Operators, StopPlanOutException
from .assignment import Assignment


Operators.initFactory()


class Interpreter(object):

    """PlanOut interpreter"""

    def __init__(self, serialization, experiment_salt='global_salt',
                 inputs={}, environment=None):
        self._serialization = serialization
        if environment is None:
            self._env = Assignment(experiment_salt)
        else:
            self._env = environment
        self.experiment_salt = self._experiment_salt = experiment_salt
        self._evaluated = False
        self._in_experiment = True
        self._inputs = inputs.copy()

    def register_operators(self, operators):
        Operators.registerOperators(operators)
        return self

    def get_params(self):
        """Get all assigned parameter values from an executed interpreter script"""
        # evaluate code if it hasn't already been evaluated
        if not self._evaluated:
            try:
                self.evaluate(self._serialization)
            except StopPlanOutException as e:
                # StopPlanOutException is raised when script calls "return", which
                # short circuits execution and sets in_experiment
                self._in_experiment = e.in_experiment
            self._evaluated = True
        return self._env

    @property
    def in_experiment(self):
        return self._in_experiment

    @property
    def salt_sep(self):
        return self._env.salt_sep

    def set_env(self, new_env):
        """Replace the current environment with a dictionary"""
        self._env = deepcopy(new_env)
        # note that overrides are inhereted from new_env
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
        self._env.set_overrides(overrides)
        return self

    def get_overrides(self):
        """Get a dictionary of all overrided values"""
        return self._env.get_overrides()

    def has_override(self, name):
        """Check to see if a variable has an override."""
        return name in self.get_overrides()

    def evaluate(self, planout_code):
        """Recursively evaluate PlanOut interpreter code"""
        # if the object is a PlanOut operator, execute it it.
        if type(planout_code) is dict and 'op' in planout_code:
            return Operators.operatorInstance(planout_code).execute(self)
        # if the object is a list, iterate over the list and evaluate each
        # element
        elif type(planout_code) is list:
            return [self.evaluate(i) for i in planout_code]
        else:
            return planout_code  # data is a literal
