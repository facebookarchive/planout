# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json
import unittest

from planout.experiment import Experiment
from planout.interpreter import Interpreter
from planout.ops.random import UniformChoice

class ExperimentTest(unittest.TestCase):

  def test_simple_experiment(self):

    my_log = []

    class TestExperiment(Experiment):
      name = 'foo'

      def configure_logger(self): pass
      def log(self, stuff): my_log.append(stuff)
      def previously_logged(self): pass

      def assign(self, params):
        params.foo = UniformChoice(choices=['a', 'b'])
    
    e = TestExperiment()
    val = e.get_params()

    self.assertTrue('foo' in val)
    self.assertEqual(val['foo'], 'b')

    self.assertEqual(len(my_log), 1)

  def test_simple_planout_experiment(self):

    compiled = json.loads("""
    {"op":"set",
     "var":"foo",
     "value":{
       "choices":{
         "op":"array",
         "values":["a","b"]
        },
       "op":"uniformChoice"
       }
    }
""")
    my_log = []

    class TestExperiment(Experiment):
      name = 'foo'

      def configure_logger(self): pass
      def log(self, stuff): my_log.append(stuff)
      def previously_logged(self): pass

      def assign(self, params):
        proc = Interpreter(compiled, self.salt, {})
        params.update(proc.get_params())
    
    e = TestExperiment()
    val = e.get_params()

    self.assertTrue('foo' in val)
    self.assertEqual(val['foo'], 'b')

    self.assertEqual(len(my_log), 1)


if __name__ == '__main__':
  unittest.main()
