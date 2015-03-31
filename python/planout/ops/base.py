# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import logging
from abc import ABCMeta, abstractmethod
import six

from .utils import Operators


class PlanOutOp(object):

    """Abstract base class for PlanOut Operators"""
    __metaclass__ = ABCMeta
    # all PlanOut operator have some set of args that act as required and
    # optional arguments

    def __init__(self, **args):
        self.args = args

    # all PlanOut operators must implement execute
    @abstractmethod
    def execute(self, mapper):
        pass

    def prettyArgs(self):
        return Operators.prettyParamFormat(self.args)

    def pretty(self):
        return '%s(%s)' % (self.args['op'], self.prettyArgs())

    def getArgMixed(self, name):
        assert name in self.args, \
            "%s: missing argument: %s." % (self.__class__, name)
        return self.args[name]

    def getArgInt(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, six.integer_types), \
            "%s: %s must be an int." % (self.__class__, name)
        return arg

    def getArgFloat(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, (six.integer_types, float)), \
            "%s: %s must be a number." % (self.__class__, name)
        return float(arg)

    def getArgString(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, six.string_types), \
            "%s: %s must be a string." % (self.__class__, name)
        return arg

    def getArgNumeric(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, (six.integer_types, float)), \
            "%s: %s must be a numeric." % (self.__class__, name)
        return arg

    def getArgList(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, (list, tuple)), \
            "%s: %s must be a list." % (self.__class__, name)
        return arg

    def getArgMap(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, dict), \
            "%s: %s must be a map." % (self.__class__, name)
        return arg

    def getArgIndexish(self, name):
        arg = self.getArgMixed(name)
        assert isinstance(arg, (dict, list, tuple)), \
            "%s: %s must be a map or list." % (self.__class__, name)
        return arg

# PlanOutOpSimple is the easiest way to implement simple operators.
# The class automatically evaluates the values of all args passed in via
# execute(), and stores the PlanOut mapper object and evaluated
# args as instance variables.  The user can then extend PlanOutOpSimple
# and implement simpleExecute().

class PlanOutOpSimple(PlanOutOp):
    __metaclass__ = ABCMeta

    def execute(self, mapper):
        self.mapper = mapper
        parameter_names = self.args.keys()
        for param in parameter_names:
            self.args[param] = mapper.evaluate(self.args[param])
        return self.simpleExecute()


class PlanOutOpBinary(PlanOutOpSimple):
    __metaclass__ = ABCMeta

    def simpleExecute(self):
        return self.binaryExecute(
            self.getArgMixed('left'),
            self.getArgMixed('right'))

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

    def simpleExecute(self):
        return self.unaryExecute(self.getArgMixed('value'))

    def pretty(self):
        return self.getUnaryString + Operators.pretty(self.getArgMixed('value'))

    def getUnaryString(self):
        return self.args['op']

    @abstractmethod
    def unaryExecute(self, value):
        pass


class PlanOutOpCommutative(PlanOutOpSimple):
    __metaclass__ = ABCMeta

    def simpleExecute(self):
        assert ('values' in self.args), "expected argument 'values'"
        return self.commutativeExecute(self.getArgList('values'))

    def pretty(self):
        values = Operators.strip_array(self.getArgList('values'))
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
