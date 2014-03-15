from abc import ABCMeta, abstractmethod

class PlanOutMapper(Object):
  """Abstract base class for PlanOut Mappers"""
  __metaclass__ = ABCMeta

  @abstractmethod
  def get(self, name, default=None):
    pass

  @abstractmethod
  def getParams(self):
    pass
