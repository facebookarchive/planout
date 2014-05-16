from abc import ABCMeta, abstractmethod, abstractproperty
from operator import itemgetter

from .experiment import Experiment, DefaultExperiment
from .ops.random import Sample, RandomInteger
from .assignment import Assignment

# decorator for methods that assume assignments have been made
def requires_experiment(f):
  def wrapped_f(self, *args, **kwargs):
    if not self._experiment:
      self._assign_experiment()
    return f(self, *args, **kwargs)
  return wrapped_f


def requires_default_experiment(f):
  def wrapped_f(self, *args, **kwargs):
    if not self._default_experiment:
      self._assign_default_experiment()
    return f(self, *args, **kwargs)
  return wrapped_f


class Namespace(object):
  __metaclass__ = ABCMeta
  def __init__(self, **kwargs):
    pass

  @abstractmethod
  def add_experiment(self, name, exp_object, num_segments, **kwargs):
    pass

  @abstractmethod
  def remove_experiment(self, name):
    pass

  @abstractmethod
  def set_auto_exposure_logging(self, value):
    pass

  @abstractproperty
  def in_experiment(self):
    pass

  @abstractmethod
  def get(self, name, default):
    pass

  @abstractmethod
  def log_exposure(self, extras=None):
    pass

  @abstractmethod
  def log_event(self, event_type, extras=None):
    pass

class SimpleNamespace(Namespace):
  __metaclass__ = ABCMeta
  def __init__(self, **kwargs):
    self.name = self.__class__  # default name is the class name
    self.inputs = kwargs
    self.num_segments = None

    # dictionary mapping segments to experiment names
    self.segment_allocations = {}

    # dictionary mapping experiment names to experiment objects
    self.current_experiments = {}

    self._experiment = None          # memoized experiment object
    self._default_experiment = None  # memoized default experiment object
    self.default_experiment_class = DefaultExperiment

    # setup name, primary key, number of segments, etc
    self.setup()
    self.available_segments = set(range(self.num_segments))

    # load namespace with experiments
    self.setup_experiments()


  @abstractmethod
  def setup(self):
    """Sets up experiment"""
    # Developers extending this class should set the following variables
    # self.name = 'sample namespace'
    # self.primary_unit = 'userid'
    # self.num_segments = 10000
    pass

  @abstractmethod
  def setup_experiments():
    # e.g.,
    # self.add_experiment('first experiment', Exp1, 100)
    pass

  @property
  def primary_unit(self):
    return self._primary_unit

  @primary_unit.setter
  def primary_unit(self, value):
    # later on we require that the primary key is a list, so we use
    # a setter to convert strings to a single element list
    if type(value) is list:
      self._primary_unit = value
    else:
      self._primary_unit = [value]


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

  def get_segment(self):
    # randomly assign primary unit to a segment
    a = Assignment(self.name)
    a.segment = RandomInteger(min=0, max=self.num_segments,
      unit=itemgetter(*self.primary_unit)(self.inputs))
    return a.segment


  def _assign_experiment(self):
    "assign primary unit to an experiment"

    segment = self.get_segment()
    # is the unit allocated to an experiment?
    if segment in self.segment_allocations:
      experiment_name = self.segment_allocations[segment]
      experiment = self.current_experiments[experiment_name](**self.inputs)
      experiment.name = '%s-%s' % (self.name, experiment_name)
      experiment.salt = '%s.%s' % (self.name, experiment_name)
      self._experiment = experiment
      self._in_experiment = experiment.in_experiment
    else:
      self._assign_default_experiment()
      self._in_experiment = False


  def _assign_default_experiment(self):
    self._default_experiment = self.default_experiment_class(**self.inputs)


  @requires_default_experiment
  def default_get(self, name, default=None):
    return self._default_experiment.get(name, default)


  @property
  @requires_experiment
  def in_experiment(self):
    return self._in_experiment


  @in_experiment.setter
  def in_experiment(self, value):
    # in_experiment cannot be externally modified
    pass


  @requires_experiment
  def set_auto_exposure_logging(self, value):
    self._experiment.set_auto_exposure_logging(value)

  @requires_experiment
  def get(self, name, default=None):
    if self._experiment is None:
      return self.default_get(name, default)
    else:
      return self._experiment.get(name, self.default_get(name, default))

  @requires_experiment
  def log_exposure(self, extras=None):
    """Logs exposure to treatment"""
    if self._experiment is None:
      pass
    self._experiment.log_exposure(extras)

  @requires_experiment
  def log_event(self, event_type, extras=None):
    """Log an arbitrary event"""
    if self._experiment is None:
      pass
    self._experiment.log_event(event_type, extras)
