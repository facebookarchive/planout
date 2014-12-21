require_relative 'operator'

module Planout
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
