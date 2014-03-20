from collections import Counter
import unittest
from math import sqrt
from planoutkit import *

## deprecated...
# in case you don't need QE fanciness
def experiment_decorator(name):
  def wrap(f):
    def wrapped_f(**kwargs):
      e = PlanOutKitMapper(name)
      e.input = kwargs
      return f(e, **kwargs)
    return wrapped_f
  return wrap


class TestRandomOperators(unittest.TestCase):
  z=3.5

  def distributionTester(self, func, value_mass, N=1000):
    """Make sure an experiment object generates the desired frequencies"""
    xs = [func(i=i).get('x') for i in xrange(N)]
    values, ns = zip(*value_mass.items())
    ns_sum = float(sum(ns))
    value_density = dict(zip(values, [i/ns_sum for i in ns]))
    self.assertProbs(xs, value_density, float(N))


  def assertProbs(self, xs, value_density, N):
    """Assert a list of values has the same density as value_density"""
    hist = Counter(xs)

    # do binomial test of proportions for each item
    for i in hist:
      self.assertProp(hist[i]/N, value_density[i], N)


  def assertProp(self, observed_p, expected_p, N):
    """Does a test of proportions"""
    z = TestRandomOperators.z
    se = z*sqrt(expected_p*(1-expected_p)/N)
    self.assertTrue(abs(observed_p-expected_p) <= se)


  def test_bernoulli(self):
    """Test bernoulli trial"""
    # returns experiment object with probability p
    def bern(p):
      @experiment_decorator(p)
      def exp_func(e, i):
        e.x = BernoulliTrial(p=p, unit=i)
        return e
      return exp_func

    self.distributionTester(bern(0.0), {0:1, 1:0})
    self.distributionTester(bern(0.1), {0:0.9, 1:0.1})
    self.distributionTester(bern(1.0), {0:0, 1:1})

  def test_uniform_choice(self):
    """Test uniform choice"""
    def uniform(c):
      str_c = ','.join(map(str, c))
      @experiment_decorator(str_c)
      def exp_func(e, i):
        e.x = UniformChoice(choices=c, unit=i)
        return e
      return exp_func

    self.distributionTester(uniform(['a']), {'a':1})
    self.distributionTester(uniform(['a','b']), {'a':1, 'b':1})
    self.distributionTester(uniform([1,2,3,4]), {1:1, 2:1, 3:1, 4:1})


  def test_weighted_choice(self):
    """Test weighted choice"""
    def weighted(weight_dict):
      c, w = zip(*weight_dict.items())
      @experiment_decorator(','.join(map(str, w)))
      def exp_func(e, i):
        e.x = WeightedChoice(choices=c, weights=w, unit=i)
        return e
      return exp_func

    d = {'a':1}
    self.distributionTester(weighted(d), d)
    d = {'a':1, 'b':2}
    self.distributionTester(weighted(d), d)
    {'a':0, 'b':2, 'c':0}
    self.distributionTester(weighted(d), d)

  def test_sample(self):
    """Test random sampling without replacement"""
    def sample(choices, draws):
      @experiment_decorator(','.join(map(str, choices)))
      def exp_func(e, i):
        e.x = Sample(choices=choices, draws=draws, unit=i)
        return e
      return exp_func

    def listDistributionTester(func, value_mass, N=1000):
      values, ns = zip(*value_mass.items())
      ns_sum = float(sum(ns))
      value_density = dict(zip(values, [i/ns_sum for i in ns]))

      xs_list = [func(i=i).get('x') for i in xrange(N)]
      for xs in zip(*xs_list):
        self.assertProbs(xs, value_density, float(N))

    listDistributionTester(sample([1,2,3], draws=3), {1:1,2:1,3:1})
    listDistributionTester(sample([1,2,3], draws=2), {1:1,2:1,3:1})
    listDistributionTester(sample(['a','a','b'], draws=3), {'a':2,'b':1})


if __name__ == '__main__':
    unittest.main()
