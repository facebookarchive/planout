require 'digest/sha1'

module PlanOut
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
end
