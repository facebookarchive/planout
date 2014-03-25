# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from collections import Counter
import unittest
from math import sqrt

from planout.ops.random import *
from planout.assignment import Assignment

# decorator for quickly constructing PlanOutKit experiments
def experiment_decorator(name):
  def wrap(f):
    def wrapped_f(**kwargs):
      params = Assignment(name)
      return f(params, **kwargs)
    return wrapped_f
  return wrap


class TestRandomOperators(unittest.TestCase):
  z = 3.29  # z_{\alpha/2} for \alpha=0.001, e.g., 99.9% CI: qnorm(1-(0.001/2))

  @staticmethod
  def valueMassToDensity(value_mass):
    """convert value_mass dictionary to a density"""
    values, ns = zip(*value_mass.items())
    ns_sum = float(sum(ns))
    value_density = dict(zip(values, [i/ns_sum for i in ns]))
    return value_density

  def distributionTester(self, func, value_mass, N=1000):
    """Make sure an experiment object generates the desired frequencies"""
    # run N trials of f() with input i
    xs = [func(i=i).get('x') for i in xrange(N)]
    value_density = TestRandomOperators.valueMassToDensity(value_mass)

    # test outcome frequencies against expected density
    self.assertProbs(xs, value_density, float(N))


  def assertProbs(self, xs, value_density, N):
    """Assert a list of values has the same density as value_density"""
    hist = Counter(xs)

    # do binomial test of proportions for each item
    for i in hist:
      self.assertProp(hist[i]/N, value_density[i], N)


  def assertProp(self, observed_p, expected_p, N):
    """Does a test of proportions"""
    # normal approximation of binomial CI.
    # this should be OK for large N and values of p not too close to 0 or 1.
    se = TestRandomOperators.z*sqrt(expected_p*(1-expected_p)/N)
    self.assertTrue(abs(observed_p-expected_p) <= se)


  def test_bernoulli(self):
    """Test bernoulli trial"""

    # returns experiment function with x = BernoulliTrial(p) draw
    # experiment salt is p
    def bernoulliTrial(p):
      @experiment_decorator(p)
      def exp_func(e, i):
        e.x = BernoulliTrial(p=p, unit=i)
        return e
      return exp_func

    self.distributionTester(bernoulliTrial(0.0), {0:1, 1:0})
    self.distributionTester(bernoulliTrial(0.1), {0:0.9, 1:0.1})
    self.distributionTester(bernoulliTrial(1.0), {0:0, 1:1})

  def test_uniform_choice(self):
    """Test uniform choice"""

    # returns experiment function with x = UniformChoice(c) draw
    # experiment salt is a string version of c
    def uniformChoice(c):
      str_c = ','.join(map(str, c))
      @experiment_decorator(str_c)
      def exp_func(e, i):
        e.x = UniformChoice(choices=c, unit=i)
        return e
      return exp_func

    self.distributionTester(uniformChoice(['a']), {'a':1})
    self.distributionTester(uniformChoice(['a','b']), {'a':1, 'b':1})
    self.distributionTester(uniformChoice([1,2,3,4]), {1:1, 2:1, 3:1, 4:1})


  def test_weighted_choice(self):
    """Test weighted choice"""

    # returns experiment function with x = WeightedChoice(c,w) draw
    # experiment salt is a string version of weighted_dict's keys
    def weightedChoice(weight_dict):
      c, w = zip(*weight_dict.items())
      @experiment_decorator(','.join(map(str, w)))
      def exp_func(e, i):
        e.x = WeightedChoice(choices=c, weights=w, unit=i)
        return e
      return exp_func

    d = {'a':1}
    self.distributionTester(weightedChoice(d), d)
    d = {'a':1, 'b':2}
    self.distributionTester(weightedChoice(d), d)
    d = {'a':0, 'b':2, 'c':0}
    self.distributionTester(weightedChoice(d), d)

  def test_sample(self):
    """Test random sampling without replacement"""

    # returns experiment function with x = sample(c, draws)
    # experiment salt is a string version of c
    def sample(choices, draws):
      @experiment_decorator(','.join(map(str, choices)))
      def exp_func(e, i):
        e.x = Sample(choices=choices, draws=draws, unit=i)
        return e
      return exp_func

    def listDistributionTester(func, value_mass, N=1000):
      value_density = TestRandomOperators.valueMassToDensity(value_mass)

      # compute N trials
      xs_list = [func(i=i).get('x') for i in xrange(N)]

      # each xs is a row of the transpose of xs_list.
      # this is expected to have the same distribution as value_density
      for xs in zip(*xs_list):
        self.assertProbs(xs, value_density, float(N))

    listDistributionTester(sample([1,2,3], draws=3), {1:1,2:1,3:1})
    listDistributionTester(sample([1,2,3], draws=2), {1:1,2:1,3:1})
    listDistributionTester(sample(['a','a','b'], draws=3), {'a':2,'b':1})


if __name__ == '__main__':
    unittest.main()
