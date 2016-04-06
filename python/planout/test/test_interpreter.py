# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json
import unittest

from planout.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):
    compiled = json.loads("""
{"op":"seq","seq":[{"op":"set","var":"group_size","value":{"choices":{"op":"array","values":[1,10]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"specific_goal","value":{"p":0.8,"unit":{"op":"get","var":"userid"},"op":"bernoulliTrial"}},{"op":"cond","cond":[{"if":{"op":"get","var":"specific_goal"},"then":{"op":"seq","seq":[{"op":"set","var":"ratings_per_user_goal","value":{"choices":{"op":"array","values":[8,16,32,64]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"ratings_goal","value":{"op":"product","values":[{"op":"get","var":"group_size"},{"op":"get","var":"ratings_per_user_goal"}]}}]}}]}]}
  """)
    interpreter_salt = 'foo'

    def test_interpreter(self):
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123454})
        params = proc.get_params()
        self.assertEqual(proc.get_params().get('specific_goal'), 1)
        self.assertEqual(proc.get_params().get('ratings_goal'), 320)

    def test_interpreter_overrides(self):
        # test overriding a parameter that gets set by the experiment
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123454})
        proc.set_overrides({'specific_goal': 0})
        self.assertEqual(proc.get_params().get('specific_goal'), 0)
        self.assertEqual(proc.get_params().get('ratings_goal'), None)

        # test to make sure input data can also be overridden
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123453})
        proc.set_overrides({'userid': 123454})
        self.assertEqual(proc.get_params().get('specific_goal'), 1)

    def test_register_ops(self):
        from planout.ops.base import PlanOutOpCommutative
        class CustomOp(PlanOutOpCommutative):
            def commutativeExecute(self, values):
                return sum(values)

        custom_op_script = {"op":"seq","seq":[{"op":"set","var":"x","value":{"values":[2,4],"op":"customOp"}}]}
        proc = Interpreter(
            custom_op_script, self.interpreter_salt, {'userid': 123454})

        proc.register_operators({'customOp': CustomOp})
        self.assertEqual(proc.get_params().get('x'), 6)



if __name__ == '__main__':
    unittest.main()
