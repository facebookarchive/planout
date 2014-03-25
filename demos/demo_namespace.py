from planout.experiment import SimpleExperiment, Experiment
from planout.ops.random import *
from planout.assignment import Assignment
import inspect
import hashlib
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
    pass


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

    # stores experiment assignment functions, index by exp name
    self.current_experiments = {}

    # not quite sure how we can fake non-experiments
    self._default_params = {}  

  @staticmethod
  def checksum_func(func):
    # src doesn't count first line of code, which includes function name
    src = ''.join(inspect.getsourcelines(func)[0][1:])
    return hashlib.sha1(src).hexdigest()[:8]

  def add_experiment(self, name, func, segments):
    num_avail = len(self.available_segments)
    if num_avail < segments:
      print 'error: %s segments requested, only %s available.' % \
        (segments, num_avail)
      return False
    if name in self.current_experiments:
      print 'error: there is already an experiment called %s.' %  name
      return False
    self.current_experiments[name] = func

    # randomly assign segments to experiments
    a = Assignment(self.name)
    a.allocations = Sample(
      choices=list(self.available_segments), draws=segments, unit=name)
    for segment in a.allocations:
      self.segment_allocations[segment] = name
      self.available_segments.remove(segment)

  def remove_experiment(self, name):
    if name not in current_experiments:
      print 'error: there is no experiment called %s.' %  name
      return False
    for segment, name in self.segment_allocations.iteritems():
      del self.segment_allocations[segment]
      self.available_segments.add(segment)
    del current_experiments[name]
    return True

  def get_experiment(self, **kwargs):
    self._checksum = None

    # randomly assign user to a segment
    a = Assignment(self.name)
    a.segment = RandomInteger(min=0, max=self.num_segments,
      unit=itemgetter(*self.primary_keys)(kwargs))
    if a.segment in self.segment_allocations:
      experiment_name = self.segment_allocations[a.segment]
      experiment = self.current_experiments[experiment_name]
      experiment.salt = '%s.%s' % (self.name, str(experiment.salt))
      return experiment(**kwargs)
    else:
      return DefaultExperiment(**kwargs)
      # we would probably want to return a fake-o experiment that
      # connects with a key-value
      #self.in_experiment = False  # turns off auto-exposure logging
      # would this work for other kvs?
      #params.update(self.default_value_store())

if __name__ == '__main__':
  ns = DemoNamespace(name='my_demo', primary_key='userid')
  ns.add_experiment('experiment 1', Exp1, 10)
  ns.add_experiment('experiment 2', Exp1, 30)
  ns.add_experiment('experiment 3', Exp3, 30)
  for i in xrange(10):
    print ns.get_experiment(userid=i)
