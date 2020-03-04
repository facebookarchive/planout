from copy import deepcopy
from math import exp, sqrt
import six


from .base import (
    PlanOutOp,
    PlanOutOpSimple,
    PlanOutOpBinary,
    PlanOutOpUnary,
    PlanOutOpCommutative,
)

import planout.ops.utils as ops


def indent(s, n=1):
    l = [("  " * n) + i for i in s.split('\n')]
    return '\n'.join(l)


class Literal(PlanOutOp):

    def execute(self, mapper):
        return self.getArgMixed('value')

    def pretty(self):
        return self.getArgMixed('value')


class Get(PlanOutOp):

    def execute(self, mapper):
        return mapper.get(self.getArgString('var'))

    def pretty(self):
        return self.getArgString('var')


class Seq(PlanOutOp):

    def execute(self, mapper):
        for op in self.getArgList('seq'):
            mapper.evaluate(op)

    def pretty(self):
        l = [ops.Operators.pretty(v) for v in self.getArgList('seq')]
        return '\n'.join(l)


class Set(PlanOutOp):

    def execute(self, mapper):
        var, value = self.getArgString('var'), self.getArgMixed('value')
        if mapper.has_override(var):
            return

        # if the value is operator, add the name of the variable as a salt if no
        # salt is provided.
        if ops.Operators.isOperator(value) and 'salt' not in value:
            value['salt'] = var

        # if we are setting the special variable, experiment_salt, update mapper
        # object accordingly with the new experiment-level salt
        if var == 'experiment_salt':
            mapper.experiment_salt = value

        mapper.set(var, mapper.evaluate(value))

    def pretty(self):
        strp = ops.Operators.pretty(self.getArgMixed('value'))
        return "%s = %s;" % (self.getArgString('var'), strp)


class Return(PlanOutOp):

    def execute(self, mapper):
        # if script calls return; or return();, assume the unit is in the
        # experiment
        value = mapper.evaluate(self.getArgMixed('value'))
        in_experiment = True if value else False
        raise ops.StopPlanOutException(in_experiment)


class Array(PlanOutOp):

    def execute(self, mapper):
        return [mapper.evaluate(value) for value in self.getArgList('values')]

    def pretty(self):
        l = [ops.Operators.pretty(v) for v in self.getArgList('values')]
        f = "[%s]" % ', '.join(l)
        return f


class Map(PlanOutOpSimple):

    def simpleExecute(self):
        m = deepcopy(self.args)
        del m['op']
        del m['salt']
        return m


class Coalesce(PlanOutOp):

    def execute(self, mapper):
        for x in self.getArgList('values'):
            eval_x = mapper.evaluate(x)
            if eval_x is not None:
                return eval_x
        return None

    def pretty(self):
        values = Operators.strip_array(self.getArgList('values'))
        pretty_c = [Operators.pretty(i) for i in values]
        return 'coalesce(%s)' % ', '.join(pretty_c)


class Index(PlanOutOpSimple):

    def simpleExecute(self):
        # returns value at index if it exists, returns None otherwise.
        # works with both lists and dictionaries.
        base, index = self.getArgIndexish('base'), self.getArgMixed('index')
        if type(base) is list:
            if index >= 0 and index < len(base):
                return base[index]
            else:
                return None
        else:
            # assume we have a dictionary
            return base.get(index)

        return self.getArgIndexish('base')[self.getArgMixed('index')]

    def pretty(self):
        b = ops.Operators.pretty(self.getArgIndexish('base'))
        i = ops.Operators.pretty(self.getArgMixed('index'))
        return "%s[%s]" % (b, i)


class Cond(PlanOutOp):

    def execute(self, mapper):
        for i in self.getArgList('cond'):
            if_clause, then_clause = i['if'], i['then']
            if mapper.evaluate(if_clause):
                return mapper.evaluate(then_clause)

    def pretty(self):
        pretty_str = ""
        first_if = True
        for i in self.getArgList('cond'):
            if_clause, then_clause = i['if'], i['then']
            if if_clause == 'true':
                pretty_str += 'else {\n'
            else:
                prefix = 'if(%s) {\n' if first_if else 'else if(%s) {\n'
                pretty_str += prefix % ops.Operators.pretty(if_clause)
            pretty_str += indent(ops.Operators.pretty(then_clause)) + '\n}'
        return pretty_str


class And(PlanOutOp):

    def execute(self, mapper):
        for clause in self.getArgList('values'):
            if not mapper.evaluate(clause):
                return False
        return True

    def pretty(self):
        pretty_c = [Operators.pretty(i) for i in self.getArgList('values')]
        return '&& '.join(pretty_c)


class Or(PlanOutOp):

    def execute(self, mapper):
        for clause in self.getArgList('values'):
            if mapper.evaluate(clause):
                return True
        return False

    def pretty(self):
        pretty_c = [Operators.pretty(c) for c in self.getArgList('values')]
        return '|| '.join(pretty_c)


class Product(PlanOutOpCommutative):

    def commutativeExecute(self, values):
        return six.moves.reduce(lambda x, y: x * y, values)

    def pretty(self):
        values = Operators.strip_array(self.getArgList('values'))
        pretty_c = [Operators.pretty(i) for i in values]
        return ' * '.join(pretty_c)


class Sum(PlanOutOpCommutative):

    def commutativeExecute(self, values):
        return sum(values)

    def pretty(self):
        pretty_c = [Operators.pretty(c) for c in self.getArgList('values')]
        return '+ '.join(pretty_c)


class Equals(PlanOutOpBinary):

    def getInfixString(self):
        return "=="

    def binaryExecute(self, left, right):
        return left == right


class GreaterThan(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return left > right


class LessThan(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return left < right


class LessThanOrEqualTo(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return left <= right


class GreaterThanOrEqualTo(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return left >= right


class Mod(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return left % right


class Divide(PlanOutOpBinary):

    def binaryExecute(self, left, right):
        return float(left) / float(right)


class Round(PlanOutOpUnary):

    def unaryExecute(self, value):
        return round(value)


class Not(PlanOutOpUnary):

    def unaryExecute(self, value):
        return not value

    def getUnaryString():
        return '!'


class Negative(PlanOutOpUnary):

    def unaryExecute(self, value):
        return 0 - value

    def getUnaryString():
        return '-'


class Min(PlanOutOpCommutative):

    def commutativeExecute(self, values):
        return min(values)


class Max(PlanOutOpCommutative):

    def commutativeExecute(self, values):
        return max(values)


class Length(PlanOutOpUnary):

    def unaryExecute(self, value):
        return len(value)

class Exp(PlanOutOpUnary):

    def unaryExecute(self, value):
        return exp(value)

class Sqrt(PlanOutOpUnary):

    def unaryExecute(self, value):
        return sqrt(value)
