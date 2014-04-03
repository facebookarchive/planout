from planout.namespace import SimpleNamespace
from planout.experiment import SimpleExperiment, DefaultExperiment
from planout.ops.random import *


class V1(SimpleExperiment):
  def assign(self, params, userid):
    params.banner_text = UniformChoice(
      choices=['Hello there!', 'Welcome!'],
      unit=userid)

class V2(SimpleExperiment):
  def assign(self, params, userid):
    params.banner_text = WeightedChoice(
      choices=['Hello there!', 'Welcome!'],
      weights=[0.8, 0.2],
      unit=userid)

class V3(SimpleExperiment):
  def assign(self, params, userid):
    params.banner_text = WeightedChoice(
      choices=['Nice to see you!', 'Welcome back!'],
      weights=[0.8, 0.2],
      unit=userid)


class DefaultButtonExperiment(DefaultExperiment):
  def get_default_params(self):
    return {'banner_text': 'Generic greetings!'}

class ButtonNamespace(SimpleNamespace):
  def setup(self):
    self.name = 'my_demo'
    self.primary_unit = 'userid'
    self.num_segments = 100
    self.default_experiment_class = DefaultButtonExperiment

  def setup_experiments(self):
    self.add_experiment('first version phase 1', V1, 10)
    self.add_experiment('first version phase 2', V1, 30)
    self.add_experiment('second version phase 1', V2, 40)
    self.remove_experiment('second version phase 1')
    self.add_experiment('third version phase 1', V3, 30)

if __name__ == '__main__':
  for i in xrange(100):
    e = ButtonNamespace(userid=i)
    print 'user %s: %s' % (i, e.get('banner_text'))
