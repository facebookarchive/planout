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

global_log = []
class ExperimentTest(unittest.TestCase):

  def experiment_tester(self, exp_class):
    global global_log
    global_log = []

    e = exp_class(i=42)
    val = e.get_params()

    self.assertTrue('foo' in val)
    self.assertEqual(val['foo'], 'a')

    self.assertEqual(len(global_log), 1)


  def test_vanilla_experiment(self):
    class TestVanillaExperiment(Experiment):
      def configure_logger(self): pass
      def log(self, stuff): global_log.append(stuff)
      def previously_logged(self): pass

      def setup(self):
        self.name = 'test_name'

      def assign(self, params, i):
        params.foo = UniformChoice(choices=['a', 'b'], unit=i)

    self.experiment_tester(TestVanillaExperiment)


  def test_interpreted_experiment(self):
    class TestInterpretedExperiment(Experiment):
      def configure_logger(self): pass
      def log(self, stuff): global_log.append(stuff)
      def previously_logged(self): pass

      def setup(self):
        self.name = 'test_name'

      def assign(self, params, **kwargs):
        compiled = json.loads("""
            {"op":"set",
             "var":"foo",
             "value":{
               "choices":["a","b"],
               "op":"uniformChoice",
               "unit": {"op": "get", "var": "i"}
               }
            }
            """)
        proc = Interpreter(compiled, self.salt, kwargs)
        params.update(proc.get_params())

    self.experiment_tester(TestInterpretedExperiment)
    
    
if __name__ == '__main__':
  unittest.main()
