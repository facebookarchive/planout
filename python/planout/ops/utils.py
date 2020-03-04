import json
import six

class StopPlanOutException(Exception):

    """Exception that gets raised when "return" op is evaluated"""

    def __init__(self, in_experiment):
        self.in_experiment = in_experiment


class Operators():
    """Singleton class for inspecting and registering operators"""

    @staticmethod
    def initFactory():
        from . import core, random
        Operators.operators = {
            "literal": core.Literal,
            "get": core.Get,
            "seq": core.Seq,
            "set": core.Set,
            "return": core.Return,
            "index": core.Index,
            "array": core.Array,
            "map": core.Map,
            "equals": core.Equals,
            "cond": core.Cond,
            "and": core.And,
            "or": core.Or,
            ">": core.GreaterThan,
            "<": core.LessThan,
            ">=": core.GreaterThanOrEqualTo,
            "<=": core.LessThanOrEqualTo,
            "%": core.Mod,
            "/": core.Divide,
            "not": core.Not,
            "round": core.Round,
            "negative": core.Negative,
            "min": core.Min,
            "max": core.Max,
            "length": core.Length,
            "coalesce": core.Coalesce,
            "product": core.Product,
            "sum": core.Sum,
            "exp": core.Exp,
            "sqrt": core.Sqrt,
            "randomFloat": random.RandomFloat,
            "randomInteger": random.RandomInteger,
            "bernoulliTrial": random.BernoulliTrial,
            "bernoulliFilter": random.BernoulliFilter,
            "uniformChoice": random.UniformChoice,
            "weightedChoice": random.WeightedChoice,
            "sample": random.Sample,
            "fastSample": random.FastSample
        }

    @staticmethod
    def registerOperators(operators):
        for op, obj in six.iteritems(operators):
            assert op not in Operators.operators
            Operators.operators[op] = operators[op]

    @staticmethod
    def isOperator(op):
        return type(op) is dict and "op" in op

    @staticmethod
    def operatorInstance(params):
        op = params['op']
        assert (op in Operators.operators), "Unknown operator: %s" % op
        return Operators.operators[op](**params)

    @staticmethod
    def prettyParamFormat(params):
        ps = [p + '=' + Operators.pretty(params[p])
              for p in params if p != 'op']
        return ', '.join(ps)

    @staticmethod
    def strip_array(params):
        if type(params) is list:
            return params
        if type(params) is dict and params.get('op', None) == 'array':
            return params['values']
        else:
            return params

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
