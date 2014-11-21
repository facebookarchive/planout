from collections import Mapping, Sequence
from grako.exceptions import SemanticError

_str_types = [str]
try:
    str_types.append(unicode)
    str_types.append(basestring)
except NameError:
    #python 3
    pass
_str_types = tuple(_str_types)


class PlanoutSemantics(object):

    def _binary_list_expr(self, ast, sym=None):
        assert sym, 'No symbol expressed'
        left = ast[0]
        right = ast[-1]
        return {'op': sym, 'values': [left, right]}

    def _binary_expr(self, ast, sym=None):
        assert sym, 'No symbol expressed'
        left = ast[0]
        right = ast[-1]
        return {'op': sym, 'left': left, 'right': right}

    def seq(self, ast):
        return {'op': 'seq', 'seq': ast}

    def assignment(self, ast):
        return {'op': 'set', 'var': ast[0], 'value': ast[2]}

    def identifier(self, ast):
        return ast

    def mod_expr(self, ast):
        return self._binary_expr(ast, sym='%')

    def div_expr(self, ast):
        return self._binary_expr(ast, sym='/')

    def gt_expr(self, ast):
        return self._binary_expr(ast, sym='>')

    def lt_expr(self, ast):
        return self._binary_expr(ast, sym='<')

    def eql_expr(self, ast):
        return self._binary_expr(ast, sym='equals')

    def lte_expr(self, ast):
        return self._binary_expr(ast, sym='<=')

    def gte_expr(self, ast):
        return self._binary_expr(ast, sym='>=')

    def add_expr(self, ast):
        return self._binary_list_expr(ast, sym='sum')

    def mul_expr(self, ast):
        return self._binary_list_expr(ast, sym='product')

    def or_expr(self, ast):
        return self._binary_list_expr(ast, sym='or')

    def and_expr(self, ast):
        return self._binary_list_expr(ast, sym='and')

    def coalesce_expr(self, ast):
        return self._binary_list_expr(ast, sym='coalesce')

    def ne_expr(self, ast):
        return {'op': 'not', 'value': self.eql_expr(ast)}

    def sub_expr(self, ast):
        return {'op': 'sum', 'values': [ast[0], self.neg_expr(ast)]}

    def not_expr(self, ast):
        return {'op': 'not', 'value': ast[-1]}

    def neg_expr(self, ast):
        return {'op': 'negative', 'value': ast[-1]}

    def int(self, ast):
        return int(ast)

    def float(self, ast):
        return float(ast)

    def string(self, ast):
        return ast[1:-1]

    def comment(self, ast):
        return None

    def slice_expr(self, ast):
        return {'op': 'index', 'base': ast[0], 'index': ast[2]}

    def array(self, ast):
        return {'op': 'array', 'values': list(ast)}

    def func_call(self, ast):
        d = {'op': ast[0]}
        for arg in ast[2]:
            d.update(arg)
        return d

    def get_expr(self, ast):
        return {'op': 'get', 'var': ast}

    def argument(self, ast):
        if isinstance(ast, Mapping):
            return ast
        elif isinstance(ast, _str_types):
            return ast
        elif isinstance(ast, Sequence):
            return {ast[0]: ast[-1]}
        else:
            return ast

    def true(self, ast):
        return True

    def false(self, ast):
        return False

    def null(self, ast):
        return None

    def json(self, ast):
        return {'op': 'literal', 'value': ast[-1]}

    def return_expression(self, ast):
        return {'op': 'return', 'value': ast[-1]}

    def if_expression(self, ast):
        thunk = ast[4][1]
        return {'op': 'cond', 'cond': [{'if': ast[2], 'then': thunk}]}

    def _default(self, ast):
        return ast
