from ops.utils import Operators
Operators.initFactory()

class PlanOutInterpreter(object):
  """PlanOut interpreter"""

  def __init__(self, serialization):
    self._serialization = serialization
    self._env = {}
    self._overrides = {}

  def result(self):
    self.execute(self._serialization)
    return self._env

  def setEnv(self, new_env):
    ne = new_env
    for v in self._overrides:
      ne[v] = self._overrides[v]
    self._env = ne
    return self  

  def has(self, name):
    return name in self._env

  def get(self, name, default=None):
    return self._env.get(name, default)

  def set(self, name, value):
    self._env[name] = value
    return self

  def setOverrides(self, overrides):
    Operators.enableOverrides()
    self._overrides = overrides
    self.setEnv(self._env)
    return self

  def hasOverride(self, name):
    return name in self._overrides

  def getOverrides(self):
    return self._overrides

  def execute(self, plan):
    if Operators.isOperator(plan):
      return Operators.operatorInstance(plan).execute(self)
    else:
      return plan  # plan is a literal

  def validate(self):
    config = self._serialization
    return Operators.validateOperator(config)

  def pretty(self):
    config = self._serialization
    return Operators.operatorInstance(config).pretty()
