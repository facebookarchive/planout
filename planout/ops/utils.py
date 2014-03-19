import json

class Operators():
  @staticmethod
  def initFactory():
    import core, random
    Operators.operators = {
      "literal": core.Literal,
      "get": core.Get,
      "seq": core.Seq,
      "set": core.Set,
      "index": core.Index,
      "array": core.Array,
      "equals": core.Equals,
      "cond": core.Cond,
      "and": core.And,
      ">": core.GreaterThan,
      "<": core.LessThan,
      ">=": core.GreaterThanOrEqualTo,
      "<=": core.LessThanOrEqualTo,
      "%": core.Mod,
      "/": core.Divide,
      "not": core.Not,
      "negative": core.Negative,
      "product": core.Product,
      "sum": core.Sum,
      "randomFloat": random.RandomFloat,
      "randomInteger": random.RandomInteger,
      "bernoulliTrial": random.BernoulliTrial,
      "bernoulliFilter": random.BernoulliFilter,
      "uniformChoice": random.UniformChoice,
      "weightedChoice": random.WeightedChoice
    }

  @staticmethod
  def enableOverrides():
    import core
    Operators.operators['set'] = core.SetOverride

  @staticmethod
  def isOperator(op):
    return \
      type(op) is dict and "op" in op and op["op"] in Operators.operators

  @staticmethod
  def operatorInstance(params):
    return Operators.operators[params['op']](**params)

  @staticmethod
  def validateOperator(params):
    if Operators.isOperator(params):
      if params['op'] in Operators.operators:
        return Operators.operatorInstance(params)._validate()
      else:
        logging.error('invalid operator %s' % params['op'])
    else:
      return True  # literals are always valid

  @staticmethod
  def prettyParamFormat(params):
    ps = [p+'='+Operators.pretty(params[p]) for p in params if p != 'op']
    return ', '.join(ps)

  @staticmethod
  def pretty(params):
    if Operators.isOperator(params):
      try:
        # if an op is invalid, we may not be able to pretty print it
        my_pretty = Operators.operatorInstance(params).pretty()
      except:
        my_pretty = params
      return my_pretty
    elif type(params) is list:
      return '[%s]' % ', '.join([Operators.pretty(p) for p in params])
    else:
      return json.dumps(params)
