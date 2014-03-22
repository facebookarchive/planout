import unittest
from interpreter import *

class TestBasicOperators(unittest.TestCase):
  def runConfig(self, config, init={}):
    e = None
    e = PlanOutInterpreterMapper(config)
    e.setEnv(init)
    is_valid = e.validate()
    self.assertTrue(is_valid)
    return e.getParams()

  def runConfigSingle(self, config):
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
    arr = [4,5,'a']
    a = self.runConfigSingle({'op': 'array', 'values': arr})
    self.assertEquals(arr, a)

  def test_cond(self):
    getInput = lambda i, r: {'op': 'equals', 'left': i, 'right': r}
    testIf = lambda i: self.runConfig({
      'op': 'cond', 'cond': [
      {'if': getInput(i, 0), 'then': {'op': 'set', 'var': 'x', 'value': 'x_0'}},
      {'if': getInput(i, 1), 'then': {'op': 'set', 'var': 'x', 'value': 'x_1'}}
    ]})
    self.assertEquals({'x': 'x_0'}, testIf(0))
    self.assertEquals({'x': 'x_1'}, testIf(1))

  def test_get(self):
    d = self.runConfig({'op': 'seq', 'seq': [
      {'op': 'set', 'var': 'x', 'value': 'x_val'},
      {'op': 'set', 'var': 'y', 'value':
        {'op': 'get', 'var': 'x'}}
    ]})
    self.assertEquals({'x': 'x_val', 'y': 'x_val'}, d)

  def test_index(self):
    x = self.runConfigSingle({'op': 'index', 'index': 0, 'base': [1,2,3]})
    self.assertEquals(x, 1)
    x = self.runConfigSingle({'op': 'index', 'index': 2, 'base': [1,2,3]})
    self.assertEquals(x, 3)
    x = self.runConfigSingle({'op': 'index', 'index': 2, 'base':
     {'op': 'array', 'values': [1,2,3]}})
    self.assertEquals(x, 3)

  def test_length(self):
    arr = range(5)
    length_test = self.runConfigSingle({'op': 'length', 'values': arr})
    self.assertEquals(len(arr), length_test)
    length_test = self.runConfigSingle({'op': 'length', 'values': []})
    self.assertEquals(0, length_test)
    length_test = self.runConfigSingle({'op': 'length', 'values':
      {'op': 'array', 'values': arr}
    })
    self.assertEquals(length_test, len(arr))

  def test_not(self):
    # test not
    x = self.runConfigSingle({'op': 'not', 'value': 0})
    self.assertEquals(True, x)
    x = self.runConfigSingle({'op': 'not', 'value': False})
    self.assertEquals(True, x)

    x = self.runConfigSingle({'op': 'not', 'value': 1})
    self.assertEquals(False, x)
    x = self.runConfigSingle({'op': 'not', 'value': True})
    self.assertEquals(False, x)

  def test_or(self):
    x = self.runConfigSingle({
      'op': 'or',
      'values': [0, 0, 0]})
    self.assertEquals(False, x)

    x = self.runConfigSingle({
      'op': 'or',
      'values': [0, 0, 1]})
    self.assertEquals(True, x)

    x = self.runConfigSingle({
      'op': 'or',
      'values': [False, True, False]})
    self.assertEquals(True, x)

  def test_and(self):
    x = self.runConfigSingle({
      'op': 'and',
      'values': [1, 1, 0]})
    self.assertEquals(False, x)

    x = self.runConfigSingle({
      'op': 'and',
      'values': [0, 0, 1]})
    self.assertEquals(False, x)

    x = self.runConfigSingle({
      'op': 'and',
      'values': [True, True, True]})
    self.assertEquals(True, x)

  def test_commutative(self):
    arr = [33, 7, 18, 21, -3]

    min_test = self.runConfigSingle({'op': 'min', 'values': arr})
    self.assertEquals(min(arr), min_test)
    max_test = self.runConfigSingle({'op': 'max', 'values': arr})
    self.assertEquals(max(arr), max_test)
    sum_test = self.runConfigSingle({'op': 'sum', 'values': arr})
    self.assertEquals(sum(arr), sum_test)
    product_test = self.runConfigSingle({'op': 'product', 'values': arr})
    self.assertEquals(reduce(lambda x,y: x*y, arr), product_test)

  def test_binary_ops(self):
    eq = self.runConfigSingle({'op': 'equals', 'left': 1, 'right': 2})
    self.assertEquals(1==2, eq)
    eq = self.runConfigSingle({'op': 'equals', 'left': 2, 'right': 2})
    self.assertEquals(2==2, eq)
    gt = self.runConfigSingle({'op': '>', 'left': 1, 'right': 2})
    self.assertEquals(1>2, gt)
    lt = self.runConfigSingle({'op': '<', 'left': 1, 'right': 2})
    self.assertEquals(1<2, lt)
    gte = self.runConfigSingle({'op': '>=', 'left': 2, 'right': 2})
    self.assertEquals(2>=2, gte)
    gte = self.runConfigSingle({'op': '>=', 'left': 1, 'right': 2})
    self.assertEquals(1>=2, gte)
    lte = self.runConfigSingle({'op': '<=', 'left': 2, 'right': 2})
    self.assertEquals(2<=2, lte)
    mod = self.runConfigSingle({'op': '%', 'left': 11, 'right': 3})
    self.assertEquals(11 % 3, mod)
    div = self.runConfigSingle({'op': '/', 'left': 3, 'right': 4})
    self.assertEquals(0.75, div)

if __name__ == '__main__':
    unittest.main()
