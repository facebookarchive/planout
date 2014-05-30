import hashlib
import base


class PlanOutOpRandom(base.PlanOutOpSimple):
  LONG_SCALE = float(0xFFFFFFFFFFFFFFF)

  def options(self):
    return {
     'unit': {'required': 1, 'description': 'unit to hash on'},
     'salt': {'required': 0,'description':
       'salt for hash. should generally be unique for each random variable'}}

  def getUnit(self, appended_unit=None):
    unit = self.parameters['unit']
    if type(unit) is not list:
      unit = [unit]
    if appended_unit is not None:
      unit += [appended_unit]
    return unit

  def getHash(self, appended_unit=None):
    salt = self.parameters['salt']
    salty = '%s.%s' % (self.mapper.experiment_salt, salt)
    unit_str = '.'.join(map(str, self.getUnit(appended_unit)))
    return int(hashlib.sha1(salty + unit_str).hexdigest()[:15], 16)

  def getUniform(self, min_val=0.0, max_val=1.0, appended_unit=None):
    zero_to_one = self.getHash(appended_unit)/PlanOutOpRandom.LONG_SCALE
    return min_val + max_val*zero_to_one


class RandomFloat(PlanOutOpRandom):
  def options(self):
    return {
      'min': {'required': 1, 'description': 'min (float) value drawn'},
      'max': {'required': 1, 'description': 'max (float) value being drawn'}}

  def simpleExecute(self):
    min_val = self.parameters.get('min', 0)
    max_val = self.parameters.get('max', 1)
    return self.getUniform(min_val, max_val)


class RandomInteger(PlanOutOpRandom):
  def options(self):
    return {
      'min': {'required': 1, 'description': 'min (int) value drawn'},
      'max': {'required': 1, 'description': 'max (int) value being drawn'}}

  def simpleExecute(self):
    min_val = self.parameters.get('min', 0)
    max_val = self.parameters.get('max', 1)
    return min_val + self.getHash() % (max_val - min_val + 1)


class BernoulliTrial(PlanOutOpRandom):
  def options(self):
    return {'p': {'required': 1, 'description': 'probability of drawing 1'}}

  def simpleExecute(self):
    p = self.parameters['p']
    rand_val = self.getUniform(0.0, 1.0)
    return 1 if rand_val <= p else 0


class BernoulliFilter(PlanOutOpRandom):
  def options(self):
   return {
      'p': {'required': 1, 'description': 'probability of retaining element'},
      'choices': {'required': 1, 'description': 'elements being filtered'}}

  def simpleExecute(self):
    p, values = self.parameters['p'], self.parameters['choices']
    if len(values) == 0:
      return []
    return [i for i in values if self.getUniform(0.0, 1.0, i) <= p]


class UniformChoice(PlanOutOpRandom):
  def options(self):
    return {'choices': {'required': 1, 'description': 'elements to draw from'}}

  def simpleExecute(self):
    choices = self.parameters['choices']
    if len(choices) == 0:
      return []
    rand_index = self.getHash() % len(choices)
    return choices[rand_index]


class WeightedChoice(PlanOutOpRandom):
  def options(self):
    return {
      'choices': {'required': 1, 'description': 'elements to draw from'},
      'weights': {'required': 1, 'description': 'probability of draw'}}
  def simpleExecute(self):
    choices = self.parameters['choices']
    weights = self.parameters['weights']
    # eventually add weighted choice
    if len(choices) == 0:
      return []
    cum_weights = dict(zip(choices, weights))
    cum_sum = 0.0
    for choice in cum_weights:
      cum_sum += cum_weights[choice]
      cum_weights[choice] = cum_sum
    stop_value = self.getUniform(0.0, cum_sum)
    for choice in cum_weights:
      if stop_value <= cum_weights[choice]:
        return choice

class Sample(PlanOutOpRandom):
  def options(self):
    return {
      'choices': {'required': 1, 'description': 'choices to sample'},
      'draws': {'required': 0, 'description': 'number of samples to draw'}}

  # implements Fisher-Yates shuffle
  def simpleExecute(self):
    # copy the list of choices so that we don't mutate it
    choices = [x for x in self.parameters['choices']]
    num_draws = self.parameters.get('draws', len(choices))
    for i in xrange(len(choices) - 1, 0, -1):
      j = self.getHash(i) % (i + 1)
      choices[i], choices[j] = choices[j], choices[i]
    return choices[:num_draws]
