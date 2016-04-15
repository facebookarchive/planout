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
    tester_unit = 4
    tester_salt = 'test_salt'

    def test_set_get_constant(self):
        a = Assignment(self.tester_salt)
        a.foo = 12
        self.assertEqual(a.foo, 12)

    def test_set_get_uniform(self):
        a = Assignment(self.tester_salt)
        a.foo = UniformChoice(choices=['a', 'b'], unit=self.tester_unit)
        a.bar = UniformChoice(choices=['a', 'b'], unit=self.tester_unit)
        a.baz = UniformChoice(choices=['a', 'b'], unit=self.tester_unit)
        self.assertEqual(a.foo, 'b')
        self.assertEqual(a.bar, 'a')
        self.assertEqual(a.baz, 'a')

    def test_overrides(self):
        a = Assignment(self.tester_salt)
        a.set_overrides({'x': 42, 'y': 43})
        a.x = 5
        a.y = 6
        self.assertEqual(a.x, 42)
        self.assertEqual(a.y, 43)

    def test_custom_salt(self):
        a = Assignment(self.tester_salt)
        custom_salt = lambda x,y: '%s-%s' % (x,y)
        a.foo = UniformChoice(choices=list(range(8)), unit=self.tester_unit)
        self.assertEqual(a.foo, 7)

if __name__ == '__main__':
    unittest.main()
