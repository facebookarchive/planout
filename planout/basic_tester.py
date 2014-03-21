import unittest
from interpreter import *

def runConfig(config, init={}):
  e = None
  e = PlanOutInterpreterMapper(config)
  e.setEnv(init)
  if e.validate():
    return e.getParams()
  else:
    return {}

class TestBasicOperators(unittest.TestCase):

  def runConfigSingle(self, config):
    x_config = {'op': 'set', 'var': 'x', 'value': config}
    return runConfig(x_config)['x']

  def test_set(self):
    """Test setter"""
    # returns experiment object with probability p
    c = {'op': 'set', 'value': 'x_val', 'var': 'x'}
    d = runConfig(c)
    self.assertEquals({'x': 'x_val'}, d)

  def test_seq(self):
    """Test sequence"""
    config = {'op': 'seq', 'seq': [
      {'op': 'set', 'value': 'x_val', 'var': 'x'},
      {'op': 'set', 'value': 'y_val', 'var': 'y'}
    ]}
    d = runConfig(config)
    self.assertEquals({'x': 'x_val', 'y': 'y_val'}, d)

  def test_logic(self):
    x = self.runConfigSingle({'op': 'not', 'value': 0})
    self.assertEquals(1, x)

if __name__ == '__main__':
    unittest.main()
