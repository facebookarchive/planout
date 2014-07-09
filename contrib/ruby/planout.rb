require 'digest/sha1'
require 'Logger'
require 'JSON'


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
  attr_reader :data

  def initialize(experiment_salt)
    @experiment_salt = experiment_salt
    @data = Hash.new
  end

  def evaluate(data)
    return data
  end

  def get(var, default=nil)
    if @data.has_key? var
      return @data[var]
    else
      return default
    end
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

  def [](x)
    return self.get(x)
  end

  def []=(x,y)
    self.set(x,y)
  end

  def get_params()
    return @data
  end
end

# I'd like to create decorators equivalent to Python's
# @requires_assignment() and @requires_exposure_logging
# (experiment.py:21, 29), but have no idea how...

class Experiment
  attr :auto_exposure_log

  def initialize(**inputs)
    @inputs = inputs
    @exposure_logged = false
    @_salt = nil
    @in_experiment = true
    @name = self.class.name
    @auto_exposure_log = true

    self.setup()  # sets name, salt, etc.

    @assignment = Assignment.new(self.salt)
    @assigned = false

    @logger = nil
    setup()
  end

  def _assign()
    self.configure_logger()
    self.assign(@assignment, **@inputs)
    @in_experiment = @assignment.get(
      'in_experiment', @in_experiment)
    @assigned = true
  end

  def setup()
    return nil
  end

  def salt=(value)
    @_salt = value
  end

  def salt
    return @_salt ? @_salt : @name
  end

  def auto_exposure_log=(value)
    @auto_exposure_log = value
  end

  def configure_logger()
    return nil
  end

  def requires_assignment()
    if not @assigned
      self._assign()
    end
  end

  def is_logged?
    return @logged
  end

  def requires_exposure_logging()
    if @auto_exposure_log and @in_experiment and not @exposure_logged
      self.log_exposure()
    end
  end


  def get_params()
    requires_assignment()
    requires_exposure_logging()
    return @assignment.get_params()
  end

  def get(name, default=nil)
    requires_assignment()
    requires_exposure_logging()
    return @assignment.get(name, default)
  end

  def assign(params, *inputs)
    # up to child class to implement
    return nil
  end

  def log_event(event_type, extras = nil)
    if extras.nil?
      extra_payload = {'event' => event_type}
    else
      extra_payload = {
        'event' => event_type,
        'extra_data' => extras.clone
      }
    end
    self.log(self.as_blob(extra_payload))
  end

  def log_exposure(extras = nil)
    @exposure_logged = true
    self.log_event('exposure', extras)
  end

  def as_blob(extras = {})
    d = {
      'name' => @name,
      'time' => Time.now.to_i,
      'salt' => self.salt,
      'inputs' => @inputs,
      'params' => @assignment.data
    }
    extras.each do |key, value|
      d[key] = value
    end
    return d
  end
  # would like to know if I'm going in the right direction
  # from a Ruby hacker before I continue...
end

class SimpleExperiment < Experiment
  def configure_logger()
    @logger = Logger.new(STDOUT)
    #@loger.level = Logger::WARN
    @logger.formatter = proc do
      |severity, datetime, progname, msg|
      "logged data: #{msg}\n"
    end
  end

  def log(data)
    @logger.info(JSON.dump(data))
  end
end

class VotingExperiment < SimpleExperiment
  def setup()
  #  self.salt = "VotingExperiment"
  end

  # all assign() methods take params and an inputs array
  def assign(params, **inputs)
    userid = inputs[:userid]
    params[:button_color] = UniformChoice.new(
      choices: ['ff0000', '#00ff00'], unit: userid)
    params[:button_text] = UniformChoice.new(
      choices: ["I'm voting", "I'm a voter"], unit: userid, salt:'x')
  end
end

my_exp = VotingExperiment.new(userid:14)
my_button_color = my_exp.get(:button_color)
button_text = my_exp.get(:button_text)
puts "button color is %s and button text is %s." % [my_button_color,button_text]

(14..16).each do |i|
  my_exp = VotingExperiment.new(userid:i)
  #my_exp.auto_exposure_log = false
  # toggling the above disables or re-enables auto-logging
  puts "\ngetting assignment for user %s note: first time triggers a log event" % i
  puts "button color is %s and button text is %s" % 
    [my_exp.get(:button_color), my_exp.get(:button_text)]
end



# ### this is just a proof of concept for Assignment
# (1..10).each do |userid|
#   a = Assignment.new('exp_salt')
#   a.set('foo', UniformChoice.new(
#     unit: userid, choices: ['x', 'y']
#   ))
#   a.set('bar', WeightedChoice.new(
#     unit: userid,
#     choices: ['a','b','c'],
#     weights: [0.2, 0.5, 0.3])
#   )
#   a.set('baz', RandomFloat.new(
#     unit:userid, min: 5, max: 20))
#   puts a.data
# end
