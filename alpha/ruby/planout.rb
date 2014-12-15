require 'digest/sha1'
require 'Logger'
require 'JSON'

class Operator
  attr_accessor :args
  def initialize(parameters)
    @args = parameters
  end

  def execute(mapper)
    mapper.experiment_salt
  end
end

class OpSimple < Operator
  def execute(mapper)
    @mapper = mapper
    @parameters = {}

    @args.each do |key, value|
      @parameters[key] = mapper.evaluate(value)
    end

    simple_execute
  end

  def simple_execute
    -1
  end
end

class OpRandom < OpSimple
  LongScale = Float(0xFFFFFFFFFFFFFFF)

  def get_unit(appended_unit = nil)
    unit = @parameters[:unit]
    unit = [unit] if !unit.is_a? Array
    unit += appended_unit if appended_unit != nil
    unit
  end

  def get_hash(appended_unit = nil)
    salt = @parameters[:salt]
    salty = "#{@mapper.experiment_salt}.#{salt}"
    unit_str = get_unit(appended_unit).join('.')
    x = "#{salty}.#{unit_str}"
    last_hex = (Digest::SHA1.hexdigest(x))[0..14]
    last_hex.to_i(16)
  end

  def get_uniform(min_val = 0.0, max_val = 1.0, appended_unit = nil)
    zero_to_one = self.get_hash(appended_unit)/LongScale
    min_val + (max_val-min_val) * zero_to_one
  end
end

class RandomFloat < OpRandom
  def simple_execute
    min_val = @parameters.fetch(:min, 0)
    max_val = @parameters.fetch(:max, 1)
    get_uniform(min_val, max_val)
  end
end

class RandomInteger < OpRandom
  def simple_execute
    min_val = @parameters.fetch(:min, 0)
    max_val = @parameters.fetch(:max, 1)
    min_val + get_hash() % (max_val - min_val + 1)
  end
end

class BernoulliTrial < OpRandom
  def simple_execute
    p = @parameters[:p]
    rand_val = get_uniform(0.0, 1.0)
    (rand_val <= p) ? 1 : 0
  end
end

class UniformChoice < OpRandom
  def simple_execute
    choices = @parameters[:choices]
    return [] if choices.length() == 0
    rand_index = get_hash() % choices.length()
    choices[rand_index]
  end
end

class WeightedChoice < OpRandom
  def simple_execute
    choices = @parameters[:choices]
    weights = @parameters[:weights]

    return [] if choices.length() == 0

    cum_weights = choices.zip(weights)
    cum_sum = 0.0

    cum_weights.each do |choice, weight|
      cum_sum += weight
      cum_weights[choice] = cum_sum
    end

    stop_value = get_uniform(0.0, cum_sum)

    cum_weights.each do |choice, cum_weight|
      choice if stop_value <= cum_weight
    end
  end
end


class Assignment
  attr_accessor :experiment_salt, :data

  def initialize(experiment_salt)
    @experiment_salt = experiment_salt
    @data = {}
  end

  def evaluate(data)
    data
  end

  def get(var, default = nil)
    @data[var] || default
  end

  # in python this would be defined as __setattr__ or __setitem__
  # not sure how to do this in Ruby.
  def set(name, value)
    if value.is_a? Operator
      value.args[:salt] = name if !value.args.has_key?(:salt)
      @data[name] = value.execute(self)
    else
      @data[name] = value
    end
  end

  def [](x)
    get(x)
  end

  def []=(x,y)
    set(x,y)
  end

  def get_params
    @data
  end
end

# I'd like to create decorators equivalent to Python's
# @requires_assignment() and @requires_exposure_logging
# (experiment.py:21, 29), but have no idea how...

class Experiment
  attr_accessor :auto_exposure_log

  def initialize(**inputs)
    @inputs = inputs
    @exposure_logged = false
    @_salt = nil
    @in_experiment = true
    @name = self.class.name
    @auto_exposure_log = true

    setup  # sets name, salt, etc.

    @assignment = Assignment.new(salt)
    @assigned = false

    @logger = nil
    setup
  end

  def _assign
    configure_logger
    assign(@assignment, **@inputs)
    @in_experiment = @assignment.get(:in_experiment, @in_experiment)
    @assigned = true
  end

  def setup
    nil
  end

  def salt=(value)
    @_salt = value
  end

  def salt
    @_salt ? @_salt : @name
  end

  def auto_exposure_log=(value)
    @auto_exposure_log = value
  end

  def configure_logger
    nil
  end

  def requires_assignment
    _assign if !@assigned
  end

  def is_logged?
    @logged
  end

  def requires_exposure_logging
    log_exposure if @auto_exposure_log && @in_experiment && !@exposure_logged
  end

  def get_params
    requires_assignment
    requires_exposure_logging
    @assignment.get_params
  end

  def get(name, default = nil)
    requires_assignment
    requires_exposure_logging
    @assignment.get(name, default)
  end

  def assign(params, *inputs)
    # up to child class to implement
    nil
  end

  def log_event(event_type, extras = nil)
    if extras.nil?
      extra_payload = {event: event_type}
    else
      extra_payload = {
        event: event_type,
        extra_data: extras.clone
      }
    end

    log(as_blob(extra_payload))
  end

  def log_exposure(extras = nil)
    @exposure_logged = true
    log_event(:exposure, extras)
  end

  def as_blob(extras = {})
    d = {
      name: @name,
      time: Time.now.to_i,
      salt: salt,
      inputs: @inputs,
      params: @assignment.data
    }

    d.merge!(extras)
    d
  end
end

class SimpleExperiment < Experiment
  def configure_logger
    @logger = Logger.new(STDOUT)
    #@loger.level = Logger::WARN
    @logger.formatter = proc do |severity, datetime, progname, msg|
      "logged data: #{msg}\n"
    end
  end

  def log(data)
    @logger.info(JSON.dump(data))
  end
end

class VotingExperiment < SimpleExperiment
  def setup
  #  self.salt = "VotingExperiment"
  end

  # all assign() methods take params and an inputs array
  def assign(params, **inputs)
    userid = inputs[:userid]
    params[:button_color] = UniformChoice.new({
      choices: ['ff0000', '#00ff00'],
      unit: userid
    })

    params[:button_text] = UniformChoice.new({
      choices: ["I'm voting", "I'm a voter"],
      unit: userid,
      salt:'x'
    })
  end
end

my_exp = VotingExperiment.new(userid:14)
my_button_color = my_exp.get(:button_color)
button_text = my_exp.get(:button_text)
puts "button color is #{my_button_color} and button text is #{button_text}."

(14..16).each do |i|
  my_exp = VotingExperiment.new(userid:i)
  #my_exp.auto_exposure_log = false
  # toggling the above disables or re-enables auto-logging
  puts "\ngetting assignment for user #{i} note: first time triggers a log event"
  puts "button color is #{my_exp.get(:button_color)} and button text is #{my_exp.get(:button_text)}"
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
