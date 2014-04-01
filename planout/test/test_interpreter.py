# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json
import unittest

from planout.interpreter import Interpreter, Validator

class InterpreterTest(unittest.TestCase):
  compiled = json.loads("""
{"op":"seq","seq":[{"op":"set","var":"group_size","value":{"choices":{"op":"array","values":[1,10]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"specific_goal","value":{"p":0.8,"unit":{"op":"get","var":"userid"},"op":"bernoulliTrial"}},{"op":"cond","cond":[{"if":{"op":"get","var":"specific_goal"},"then":{"op":"seq","seq":[{"op":"set","var":"ratings_per_user_goal","value":{"choices":{"op":"array","values":[8,16,32,64]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"ratings_goal","value":{"op":"product","values":[{"op":"get","var":"group_size"},{"op":"get","var":"ratings_per_user_goal"}]}}]}}]}]}
  """)

  def test_validator(self):
    v = Validator(self.compiled)
    self.assertTrue(v.validate())

    # these should print errors and return fail.
    incomplete_op = Validator({'op': 'uniformChoice', 'value': 42})
    self.assertFalse(incomplete_op.validate())

    bogus_op = Validator({'op': 'bogoOp', 'value': 42})
    self.assertFalse(bogus_op.validate())

  def test_interpreter(self):
    proc = Interpreter(self.compiled, 'foo', {'userid': 123456})
    self.assertTrue(proc.get_params())


if __name__ == '__main__':
  unittest.main()
