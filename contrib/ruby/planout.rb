require 'digest/sha1'

class Operator
  attr :args
  def initialize(**parameters)
    @args = parameters
  end

  def execute(mapper)
    return mapper.experiment_salt
  end
end

class OpSimple < Operator
  def execute(mapper)
    @mapper = mapper
    @parameters = Hash.new
    @args.each do |param, value|
      @parameters[param] = mapper.evaluate(value)
    end
    return self.simpleExecute()
  end

  def simpleExecute()
    return -1
  end
end

class OpRandom < OpSimple
  def getUnit(appended_unit=nil)
    unit = @parameters[:"unit"]

    if not unit.is_a? Array
      unit = [unit]
    end

    if appended_unit != nil
      unit += appended_unit
    end
    return unit
  end

  def getHash(appended_unit=nil)
    salt = @parameters[:"salt"]
    salty = '%s.%s' % [@mapper.experiment_salt, salt]
    unit_str = self.getUnit(appended_unit).join('.')
    x = '%s.%s' % [salty, unit_str]
    last_hex = (Digest::SHA1.hexdigest(x))[0..14]
    return last_hex.to_i(16)
  end

  def getUniform(min_val=0.0, max_val=1.0, appended_unit=nil)
    long_scale = Float(0xFFFFFFFFFFFFFFF) # not sure how to make this a constant
    zero_to_one = self.getHash(appended_unit)/long_scale
    return min_val + (max_val-min_val)*zero_to_one
  end
end

class RandomFloat < OpRandom
  def simpleExecute()
    min_val = @parameters.fetch(:min, 0)
    max_val = @parameters.fetch(:max, 1)
    return self.getUniform(min_val, max_val)
  end
end

class RandomInteger < OpRandom
  def simpleExecute()
    min_val = @parameters.fetch(:min, 0)
    max_val = @parameters.fetch(:max, 1)
    return min_val + self.getHash() % (max_val - min_val + 1)
  end
end

class BernoulliTrial < OpRandom
  def simpleExecute()
    p = @parameters[:p]
    rand_val = self.getUniform(0.0, 1.0)
    if rand_val <= p
      return 1
    else
      return 0
    end
  end
end

class UniformChoice < OpRandom
  def simpleExecute()
    choices = @parameters[:choices]
    if choices.length() == 0
      return []
    end
    rand_index = self.getHash() % choices.length()
    return choices[rand_index]
  end
end

class WeightedChoice < OpRandom
  def simpleExecute()
    choices = @parameters[:choices]
    weights = @parameters[:weights]
    if choices.length() == 0
      return []
    end
    cum_weights = Hash[choices.zip(weights)]
    cum_sum = 0.0
    cum_weights.each do |choice, weight|
      cum_sum += weight
      cum_weights[choice] = cum_sum
    end
    stop_value = self.getUniform(0.0, cum_sum)
    cum_weights.each do |choice, cum_weight|
      if stop_value <= cum_weight
        return choice
      end
    end
  end
end


class Assignment
  attr_reader :experiment_salt
  def initialize(experiment_salt)
    @experiment_salt = experiment_salt
    @data = Hash.new
  end

  # in python this would be defined as __setattr__ or __setitem__
  # not sure how to do this in Ruby.
  def set(name, value)
    if value.is_a? Operator
      if not value.args.has_key? 'salt'
        value.args[:salt] = name
      end
      @data[name] = value.execute(self)
    else
      @data[name] = value
    end
  end

  def evaluate(data)
    return data
  end

  def data()
    return @data
  end
end


# I'd like to create decorators equivalent to Python's
# @requires_assignment() and @requires_exposure_logging
# (experiment.py:21, 29), but have no idea how...
class Experiment
  def initialize(**inputs)
    @inputs = inputs
    @exposure_logged = false
    @_salt = nil
    @in_experiment = true
    @_name = self.class
    @auto_exposure_log = true

    self.setup()
    self.assignment = Assignment(self.name)
    self.assigned = false
  end

  def salt=(value)
    @_salt = value
  end

  def salt
    return @_salt ? @_salt : @name
  end

  # would like to know if I'm going in the right direction
  # from a Ruby hacker before I continue...
end

(1..10).each do |userid|
  a = Assignment.new('exp_salt')
  a.set('foo', UniformChoice.new(
    unit: userid, choices: ['x', 'y']
  ))
  a.set('bar', WeightedChoice.new(
    unit: userid,
    choices: ['a','b','c'],
    weights: [0.2, 0.5, 0.3])
  )
  a.set('baz', RandomFloat.new(unit:userid, min: 5, max: 20))
  puts a.data()
end
