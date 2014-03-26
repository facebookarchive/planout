from planout.experiment import SimpleExperiment, Experiment
from planout.ops.random import *
from planout.assignment import Assignment
import inspect
import hashlib
import logging
from operator import itemgetter
from abc import ABCMeta, abstractmethod
from assignment_demo import Exp1, Exp3



class DefaultExperiment(Experiment):
  """Dummy experiment which is just a key-value store"""
  def configure_logger(self):
    pass  # we don't log anything when there is no experiment

  def log(self, data):
    pass

  def previously_logged(self):
    return True

  def assign(self, params, **kwargs):
    params.update({'banner_text': 'This is the default!'})


class DemoNamespace(object):
  def __init__(self, name, primary_key):
    self.name = name
    self.num_segments = 100
    self.available_segments = set(range(self.num_segments))
    if type(primary_key) is list:
      self.primary_keys = primary_key
    else:
      self.primary_keys = [primary_key]

    # dictionary mapping segments to experiment names
    self.segment_allocations = {}

    # dictionary mapping experiment names to experiment objects
    self.current_experiments = {}

  @staticmethod
  def checksum_func(func):
    # src doesn't count first line of code, which includes function name
    src = ''.join(inspect.getsourcelines(func)[0][1:])
    return hashlib.sha1(src).hexdigest()[:8]

  def add_experiment(self, name, exp_object, segments):
    num_avail = len(self.available_segments)
    if num_avail < segments:
      print 'error: %s segments requested, only %s available.' % \
        (segments, num_avail)
      return False
    if name in self.current_experiments:
      print 'error: there is already an experiment called %s.' %  name
      return False

    # randomly select the given number of segments from all available segments
    a = Assignment(self.name)
    a.sampled_segments = \
      Sample(choices=list(self.available_segments), draws=segments, unit=name)

    # assign each segment to the experiment name
    for segment in a.sampled_segments:
      self.segment_allocations[segment] = name
      self.available_segments.remove(segment)

    # associate the experiment name with an object
    self.current_experiments[name] = exp_object

  def remove_experiment(self, name):
    if name not in self.current_experiments:
      print 'error: there is no experiment called %s.' %  name
      return False

    segments_to_free = \
      [s for s, n in self.segment_allocations.iteritems() if n == name]

    for segment in segments_to_free:
      del self.segment_allocations[segment]
      self.available_segments.add(segment)
    del self.current_experiments[name]

    return True

  def get_experiment(self, **kwargs):
    # randomly assign user to a segment
    a = Assignment(self.name)
    a.segment = RandomInteger(min=0, max=self.num_segments,
      unit=itemgetter(*self.primary_keys)(kwargs))
    if a.segment in self.segment_allocations:
      experiment_name = self.segment_allocations[a.segment]
      experiment = self.current_experiments[experiment_name](**kwargs)
      experiment.name = experiment_name
      experiment.salt = '%s.%s' % (self.name, experiment.name)
      return experiment
    else:
      return DefaultExperiment(**kwargs)

class DemoNamespaceExperiment(SimpleExperiment):
  namespace = 'demo_namespace'
  def configure_logger(self):
    """Sets up logger to log to experiment_name.log"""
    ns = self.__class__.namespace
    # only want to set logging handler once
    if not self.__class__._logger_configured:
      self.__class__.logger = logging.getLogger(ns)
      self.__class__.logger.setLevel(logging.INFO)
      self.__class__.logger.addHandler(logging.FileHandler('%s.log' % ns))
      self.__class__._logger_configured = True

class V1(DemoNamespaceExperiment):
  def assign(self, params, userid):
    params.banner_text = UniformChoice(
      choices=['Hello there!', 'Welcome!'],
      unit=userid)

class V2(DemoNamespaceExperiment):
  def assign(self, params, userid):
    params.banner_text = WeightedChoice(
      choices=['Hello there!', 'Welcome!'],
      weights=[0.8, 0.2],
      unit=userid)

class V3(DemoNamespaceExperiment):
  def assign(self, params, userid):
    params.banner_text = WeightedChoice(
      choices=['Nice to see you!', 'Welcome back!'],
      weights=[0.8, 0.2],
      unit=userid)

if __name__ == '__main__':
  ns = DemoNamespace(name='my_demo', primary_key='userid')
  ns.add_experiment('first version phase 1', V1, 10)
  ns.add_experiment('first version phase 2', V1, 30)
  ns.add_experiment('second version phase 1', V2, 40)
  ns.remove_experiment('second version phase 1')
  ns.add_experiment('third version phase 1', V3, 30)
  print ns.segment_allocations

  for i in xrange(40):
    print ns.get_experiment(userid=i)
