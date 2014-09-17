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
  def options(self):
    return {'value': {'required': 1}}

  def execute(self, mapper):
    return self.args['value']

  def pretty(self):
    return self.args['value']


class Get(PlanOutOp):
  def options(self):
    return {'var': {'required': 1, 'description': 'variable to get'}}

  def execute(self, mapper):
    return mapper.get(self.args['var'])

  def pretty(self):
    return self.args['var']


class Seq(PlanOutOp):
  def options(self):
    return {
      'seq': {
        'required': 1,
        'description': 'sequence of operators to execute'}}

  def execute(self, mapper):
    for op in self.args['seq']:
      mapper.evaluate(op)

  def validate(self):
    is_valid = True
    for op in self.args['seq']:
      if not ops.Operators.validateOperator(op):
        is_valid = False
    return is_valid

  def pretty(self):
    l = [ops.Operators.pretty(v) for v in self.args['seq']]
    return '\n'.join(l)


class Set(PlanOutOp):
  def options(self):
    return {
      'var': {'required': 1, 'description': 'variable to set'},
      'value': {'required': 1, 'description': 'value of variable being set'}}

  def execute(self, mapper):
    var, value = self.args['var'], self.args['value']
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

  def validate(self):
    return ops.Operators.validateOperator(self.args['value'])

  def pretty(self):
    strp = ops.Operators.pretty(self.args['value'])
    return "%s = %s;" % (self.args['var'], strp)


class Array(PlanOutOp):
  def options(self):
    return {'values': {'required': 1, 'description': 'array of values'}}

  def execute(self, mapper):
    return [mapper.evaluate(value) for value in self.args['values']]

  def validate(self):
    is_valid = True
    for value in self.args['values']:
      if not ops.Operators.validateOperator(value):
        is_valid = False
    return is_valid

  def pretty(self):
    l = [ops.Operators.pretty(v) for v in self.args['values']]
    f = "[%s]" % ', '.join(l)
    return f

class Coalesce(PlanOutOp):
  def options(self):
    return {'values': {'required': 1, 'description': 'array of values'}}

  def execute(self, mapper):
    for x in self.args['values']:
      eval_x = mapper.evaluate(x)
      if eval_x is not None:
        return eval_x
    return None

  def pretty(self):
    values = Operators.strip_array(self.args['values'])
    pretty_c = [Operators.pretty(i) for i in values]
    return 'coalesce(%s)' % ', '.join(pretty_c)


class Index(PlanOutOpSimple):
  def options(self):
    return {
      'base': {'required': 1, 'description': 'variable being indexed'},
      'index': {'required': 1, 'description': 'index'}}

  def simpleExecute(self):
    # returns value at index if it exists, returns None otherwise.
    # works with both lists and dictionaries.
    base, index = self.parameters['base'], self.parameters['index']
    if type(base) is list:
      if index >= 0 and index < len(base):
        return base[index]
      else:
        return None
    else:
      # assume we have a dictionary
      return base.get(index)

    return self.parameters['base'][self.parameters['index']]

  def pretty(self):
    b = ops.Operators.pretty(self.args['base'])
    i = ops.Operators.pretty(self.args['index'])
    return "%s[%s]" % (b, i)


class Cond(PlanOutOp):
  def options(self):
    return {
    'cond': {'required': 1, 'description': 'array of if-else tuples'}}

  def execute(self, mapper):
    for i in self.args['cond']:
      if_clause, then_clause = i['if'], i['then']
      if mapper.evaluate(if_clause):
        return mapper.evaluate(then_clause)

  def validate(self):
    is_valid = True
    for ifthen_clause in self.args['cond']:
      if len(ifthen_clause) == 2:
        if_c, then_c = ifthen_clause
        if not (ops.Operators.validateOperator(if_c) and \
            ops.Operators.validateOperator(then_c)):
          is_valid = False
      else:
        logging.error('if-then clause %s must be a tuple' \
          % Operators.pretty(ifthen_clause))
        is_valid = False
      return is_valid

  def pretty(self):
    pretty_str = ""
    first_if = True
    for i in self.args['cond']:
      if_clause, then_clause = i['if'], i['then']
      if if_clause == 'true':
        pretty_str += 'else {\n'
      else:
        prefix = 'if(%s) {\n' if first_if else 'else if(%s) {\n'
        pretty_str += prefix % ops.Operators.pretty(if_clause)
      pretty_str += indent(ops.Operators.pretty(then_clause)) + '\n}'
    return pretty_str


class And(PlanOutOp):
  def options(self):
    return {
      'values': {'required': 1, 'description': 'array of truthy values'}}

  def execute(self, mapper):
    for clause in self.args['values']:
      if not mapper.evaluate(clause):
        return False
    return True

  def validate(self):
    is_valid = True
    for clause in self.args['values']:
      if not ops.Operators.validateOperator(clause):
        is_valid = False
    return is_valid

  def pretty(self):
    pretty_c = [Operators.pretty(i) for i in self.args['values']]
    return '&& '.join(pretty_c)

class Or(PlanOutOp):
  def options(self):
    return {
      'values': {'required': 1, 'description': 'array of truthy values'}}

  def execute(self, mapper):
    for clause in self.args['values']:
      if mapper.evaluate(clause):
        return True
    return False

  def validate(self):
    is_valid = True
    for clause in self.args['values']:
      if not ops.Operators.validateOperator(clause):
        is_valid = False
    return is_valid

  def pretty(self):
    pretty_c = [Operators.pretty(c) for c in self.args['values']]
    return '|| '.join(pretty_c)

class Product(PlanOutOpCommutative):
  def commutativeExecute(self, values):
    return reduce(lambda x,y: x*y, values)

  def pretty(self):
    values = Operators.strip_array(self.args['values'])
    pretty_c = [Operators.pretty(i) for i in values]
    return ' * '.join(pretty_c)

class Sum(PlanOutOpCommutative):
  def commutativeExecute(self, values):
    return sum(values)

  def pretty(self):
    pretty_c = [Operators.pretty(c) for c in self.args['values']]
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

class Length(PlanOutOpCommutative):
  def commutativeExecute(self, values):
    return len(values)
