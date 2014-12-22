require 'logger'
require 'json'

module PlanOut
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
      @_salt || @name
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
    end
  end

end
