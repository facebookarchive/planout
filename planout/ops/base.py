# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import logging
from abc import ABCMeta, abstractmethod

from .utils import Operators

class PlanOutOp(object):
  """Abstract base class for PlanOut Operators"""
  __metaclass__ = ABCMeta
  # all PlanOut operator have some set of parameters that act as required and
  # optional arguments
  def __init__(self, **parameters):
    self.args = parameters

  # all PlanOut operators must implement execute
  @abstractmethod
  def execute(self, mapper):
    pass

  # all PlanOut operators must specify required and optional parameters
  # that get used in execute() by defining options():
  #   def options(self):
  #     return {
  #       'p': {'required': 1, 'description': 'probability of success'},
  #       'n': {'required': 0, 'description': 'number of samples'}
  #     }
  #
  def options(self):
    return {}

  # if custom operators needs to perform additional, custom validation,
  # override this method (see the Cond operator in core as an example)
  def validate(self):
    return True

  def prettyArgs(self):
    return Operators.prettyParamFormat(self.args)

  def pretty(self):
    return '%s(%s)' % (self.args['op'], self.prettyArgs())

  # validates the presence of operator parameters.
  # this only gets called from Operators.validateOperator()
  def _validate(self):
    parameters = self.args
    is_valid = True
    # any operator can safely use these parameters
    # in particular, salt is automatically appended to variables
    # which don't have salt specified.
    safe_params = set(['op', 'salt'])
    # verify that all parameters are legit parameters
    instance_opts = self._options()
    for param in parameters:
      if param not in safe_params and param not in instance_opts:
        logging.error("'%s' is not a valid parameter for %s" \
            % (param, Operators.pretty(parameters)))
        is_valid = False
    # verify that all required parameters are present
    for param in instance_opts:
      if self.getOptionRequired(param) and param not in parameters:
        logging.error("required parameter '%s' not found in %s" \
            % (param, Operators.pretty(parameters)))
        is_valid = False
    # perform additional validation, if necessary
    return is_valid and self.validate()

  # recursively appends parents' options() with instance's options()
  # this only gets called by the PlanOutOp base class.
  def _options(self):
    if type(self) is PlanOutOp:
      return {}
    else:
      parent_opts = super(type(self), self).options()  # init with parent opts
      instance_opts = self.options()
      for option_name in parent_opts:
        instance_opts[option_name] = parent_opts[option_name]
      return instance_opts

  # methods that can be used by the QE to generate UI elements for operators
  def getOptionDescription(self, option_name):
    return self._options()[option_name].get('description', option_name)

  def getOptionRequired(self, option_name):
    return self._options()[option_name].get('required', 1)

  def getOptions(self):
    return [p for p in self._options()]


# PlanOutOpSimple is the easiest way to implement simple operators.
# The class automatically evaluates the values of all parameters passed in via
# execute(), and stores the PlanOut mapper object and evaluated
# parameters as instance variables.  The user can then extend PlanOutOpSimple
# and implement simpleExecute().

class PlanOutOpSimple(PlanOutOp):
  __metaclass__ = ABCMeta

  def execute(self, mapper):
    self.mapper = mapper
    self.parameters = {}    # evaluated parameters
    for param in self.args:
      self.parameters[param] = mapper.evaluate(self.args[param])
    return self.simpleExecute()

  def validate(self):
    is_valid = True
    for param_name in self.args:
      if not Operators.validateOperator(self.args[param_name]):
        is_valid = False
    return is_valid

class PlanOutOpBinary(PlanOutOpSimple):
  __metaclass__ = ABCMeta

  def options(self):
    return {
      'left': {'required': 1, 'description': 'left side of binary operator'},
      'right': {'required': 1, 'description': 'right side of binary operator'}}

  def simpleExecute(self):
    return self.binaryExecute(self.parameters['left'], self.parameters['right'])

  def pretty(self):
    return '%s %s %s' % (
      Operators.pretty(self.args['left']),
      self.getInfixString(),
      Operators.pretty(self.args['right']))

  def getInfixString(self):
    return self.args['op']

  @abstractmethod
  def binaryExecute(self, left, right):
    pass


class PlanOutOpUnary(PlanOutOpSimple):
  __metaclass__ = ABCMeta
  def options(self):
    return {
      'value': {'required': 1, 'description': 'input value to commutative operator'}}

  def simpleExecute(self):
    return self.unaryExecute(self.parameters['value'])

  def pretty(self):
    return self.getUnaryString + Operators.pretty(self.args['value'])

  def getUnaryString(self):
    return self.args['op']

  @abstractmethod
  def unaryExecute(self, value):
    pass

class PlanOutOpCommutative(PlanOutOpSimple):
  __metaclass__ = ABCMeta

  def options(self):
    return {
      'values': {'required': 1, 'description': 'input value to commutative operator'}}

  def simpleExecute(self):
    return self.commutativeExecute(self.parameters['values'])

  def pretty(self):
    values = Operators.strip_array(self.args['values'])
    if type(values) is list:
      pretty_values = ', '.join([Operators.pretty(i) for i in values])
    else:
      pretty_values = Operators.pretty(values)

    return '%s(%s)' % (self.getCommutativeString(), pretty_values)

  def getCommutativeString(self):
    return self.args['op']

  @abstractmethod
  def commutativeExecute(self, values):
    pass
