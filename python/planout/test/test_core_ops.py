# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import unittest
import six

from planout.interpreter import (
    Interpreter,
)


class TestBasicOperators(unittest.TestCase):

    def runConfig(self, config, init={}):
        e = None
        e = Interpreter(config, 'test_salt', init)
        return e.get_params()

    def run_config_single(self, config):
        x_config = {'op': 'set', 'var': 'x', 'value': config}
        return self.runConfig(x_config)['x']

    def test_set(self):
        """Test setter"""
        # returns experiment object with probability p
        c = {'op': 'set', 'value': 'x_val', 'var': 'x'}
        d = self.runConfig(c)
        self.assertEquals({'x': 'x_val'}, d)

    def test_seq(self):
        """Test sequence"""
        config = {'op': 'seq', 'seq': [
            {'op': 'set', 'value': 'x_val', 'var': 'x'},
            {'op': 'set', 'value': 'y_val', 'var': 'y'}
        ]}
        d = self.runConfig(config)
        self.assertEquals({'x': 'x_val', 'y': 'y_val'}, d)

    def test_array(self):
        arr = [4, 5, 'a']
        a = self.run_config_single({'op': 'array', 'values': arr})
        self.assertEquals(arr, a)

    def test_map(self):
        my_map = {'a': 2, 'b': 'c', 'd': False}
        m = self.run_config_single({'op': 'map', 'a': 2, 'b': 'c', 'd': False})
        self.assertEquals(my_map, m)
        
        my_map = {}
        m = self.run_config_single({'op': 'map'})
        self.assertEquals(my_map, m)

    def test_cond(self):
        getInput = lambda i, r: {'op': 'equals', 'left': i, 'right': r}
        testIf = lambda i: self.runConfig({
            'op': 'cond',
            'cond': [
                {'if': getInput(i, 0),
                 'then': {'op': 'set', 'var': 'x', 'value': 'x_0'}},
                {'if': getInput(i, 1),
                 'then': {'op': 'set', 'var': 'x', 'value': 'x_1'}}
            ]
        })
        self.assertEquals({'x': 'x_0'}, testIf(0))
        self.assertEquals({'x': 'x_1'}, testIf(1))

    def test_get(self):
        d = self.runConfig({
            'op': 'seq',
            'seq': [
                {'op': 'set', 'var': 'x', 'value': 'x_val'},
                {'op': 'set', 'var': 'y', 'value': {'op': 'get', 'var': 'x'}}
            ]
        })
        self.assertEquals({'x': 'x_val', 'y': 'x_val'}, d)

    def test_index(self):
        array_literal = [10, 20, 30]
        dict_literal = {'a': 42, 'b': 43}

        # basic indexing works with array literals
        x = self.run_config_single(
            {'op': 'index', 'index': 0, 'base': array_literal}
        )
        self.assertEquals(x, 10)

        x = self.run_config_single(
            {'op': 'index', 'index': 2, 'base': array_literal}
        )
        self.assertEquals(x, 30)

        # basic indexing works with dictionary literals
        x = self.run_config_single(
            {'op': 'index', 'index': 'a', 'base': dict_literal}
        )
        self.assertEquals(x, 42)

        # invalid indexes are mapped to None
        x = self.run_config_single(
            {'op': 'index', 'index': 6, 'base': array_literal}
        )
        self.assertEquals(x, None)

        # invalid indexes are mapped to None
        x = self.run_config_single(
            {'op': 'index', 'index': 'c', 'base': dict_literal}
        )
        self.assertEquals(x, None)

        # non literals also work
        x = self.run_config_single({
            'op': 'index',
            'index': 2,
            'base': {'op': 'array', 'values': array_literal}
        })
        self.assertEquals(x, 30)

    def test_coalesce(self):
        x = self.run_config_single({'op': 'coalesce', 'values': [None]})
        self.assertEquals(x, None)

        x = self.run_config_single(
            {'op': 'coalesce', 'values': [None, 42, None]})
        self.assertEquals(x, 42)

        x = self.run_config_single(
            {'op': 'coalesce', 'values': [None, None, 43]})
        self.assertEquals(x, 43)

    def test_length(self):
        arr = list(range(5))
        length_test = self.run_config_single({'op': 'length', 'value': arr})
        self.assertEquals(len(arr), length_test)
        length_test = self.run_config_single({'op': 'length', 'value': []})
        self.assertEquals(0, length_test)
        length_test = self.run_config_single({'op': 'length', 'value':
                                              {'op': 'array', 'values': arr}
                                              })
        self.assertEquals(length_test, len(arr))

    def test_not(self):
        # test not
        x = self.run_config_single({'op': 'not', 'value': 0})
        self.assertEquals(True, x)
        x = self.run_config_single({'op': 'not', 'value': False})
        self.assertEquals(True, x)

        x = self.run_config_single({'op': 'not', 'value': 1})
        self.assertEquals(False, x)
        x = self.run_config_single({'op': 'not', 'value': True})
        self.assertEquals(False, x)

    def test_or(self):
        x = self.run_config_single({
            'op': 'or',
            'values': [0, 0, 0]})
        self.assertEquals(False, x)

        x = self.run_config_single({
            'op': 'or',
            'values': [0, 0, 1]})
        self.assertEquals(True, x)

        x = self.run_config_single({
            'op': 'or',
            'values': [False, True, False]})
        self.assertEquals(True, x)

    def test_and(self):
        x = self.run_config_single({
            'op': 'and',
            'values': [1, 1, 0]})
        self.assertEquals(False, x)

        x = self.run_config_single({
            'op': 'and',
            'values': [0, 0, 1]})
        self.assertEquals(False, x)

        x = self.run_config_single({
            'op': 'and',
            'values': [True, True, True]})
        self.assertEquals(True, x)

    def test_commutative(self):
        # test commutative arithmetic operators
        arr = [33, 7, 18, 21, -3]

        min_test = self.run_config_single({'op': 'min', 'values': arr})
        self.assertEquals(min(arr), min_test)

        max_test = self.run_config_single({'op': 'max', 'values': arr})
        self.assertEquals(max(arr), max_test)

        sum_test = self.run_config_single({'op': 'sum', 'values': arr})
        self.assertEquals(sum(arr), sum_test)

        product_test = self.run_config_single({'op': 'product', 'values': arr})
        self.assertEquals(six.moves.reduce(lambda x, y: x * y, arr), product_test)

    def test_binary_ops(self):
        eq = self.run_config_single({'op': 'equals', 'left': 1, 'right': 2})
        self.assertEquals(1 == 2, eq)
        eq = self.run_config_single({'op': 'equals', 'left': 2, 'right': 2})
        self.assertEquals(2 == 2, eq)
        gt = self.run_config_single({'op': '>', 'left': 1, 'right': 2})
        self.assertEquals(1 > 2, gt)
        lt = self.run_config_single({'op': '<', 'left': 1, 'right': 2})
        self.assertEquals(1 < 2, lt)
        gte = self.run_config_single({'op': '>=', 'left': 2, 'right': 2})
        self.assertEquals(2 >= 2, gte)
        gte = self.run_config_single({'op': '>=', 'left': 1, 'right': 2})
        self.assertEquals(1 >= 2, gte)
        lte = self.run_config_single({'op': '<=', 'left': 2, 'right': 2})
        self.assertEquals(2 <= 2, lte)
        mod = self.run_config_single({'op': '%', 'left': 11, 'right': 3})
        self.assertEquals(11 % 3, mod)
        div = self.run_config_single({'op': '/', 'left': 3, 'right': 4})
        self.assertEquals(0.75, div)

    def test_exp(self):
        # test exp operator
        x = self.run_config_single({'op': 'exp', 'value': 1})
        self.assertEqual(2.718281828459045, x)

        x = self.run_config_single({'op': 'exp', 'value': -0.5})
        self.assertEqual(0.6065306597126334, x)

        x = self.run_config_single({'op': 'exp', 'value': 0.123})
        self.assertEqual(1.1308844209474893, x)

        x = self.run_config_single({'op': 'exp', 'value': 1.88})
        self.assertEqual(6.553504862191148, x)

    def test_sqrt(self):
        # test sqrt operator
        x = self.run_config_single({'op': 'sqrt', 'value': 1})
        self.assertEqual(1, x)

        with self.assertRaises(ValueError):
            x = self.run_config_single({'op': 'sqrt', 'value': -0.5})

        x = self.run_config_single({'op': 'sqrt', 'value': 0.123})
        self.assertEqual(0.3507135583350036, x)

        x = self.run_config_single({'op': 'sqrt', 'value': 1.88})
        self.assertEqual(1.3711309200802089, x)

    def test_return(self):
        def return_runner(return_value):
            config = {
                "op": "seq",
                "seq": [
                    {
                      "op": "set",
                      "var": "x",
                      "value": 2
                    },
                    {
                        "op": "return",
                        "value": return_value
                    },
                    {
                        "op": "set",
                        "var": "y",
                        "value": 4
                    }
                ]
            }
            e = Interpreter(config, 'test_salt')
            return e

        i = return_runner(True)
        self.assertEquals({'x': 2}, i.get_params())
        self.assertEquals(True, i.in_experiment)
        i = return_runner(42)
        self.assertEquals({'x': 2}, i.get_params())
        self.assertEquals(True, i.in_experiment)
        i = return_runner(False)
        self.assertEquals({'x': 2}, i.get_params())
        self.assertEquals(False, i.in_experiment)
        i = return_runner(0)
        self.assertEquals({'x': 2}, i.get_params())
        self.assertEquals(False, i.in_experiment)

if __name__ == '__main__':
    unittest.main()
