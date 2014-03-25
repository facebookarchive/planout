# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import unittest

from planout.assignment import Assignment
from planout.ops.random import UniformChoice

class AssignmentTest(unittest.TestCase):
  def test_set_get_constant(self):
    a = Assignment('foo')
    a.foo = 12
    self.assertEqual(a.foo, 12)

  def test_set_get_uniform(self):
    a = Assignment('foo')
    a.foo = UniformChoice(choices=['a', 'b'])
    self.assertEqual(a.foo, 'a')


if __name__ == '__main__':
  unittest.main()
