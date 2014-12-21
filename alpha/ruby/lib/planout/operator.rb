require 'digest/sha1'

module Planout
  class Operator
    attr_accessor :args
    def initialize(parameters)
      @args = parameters
    end

    def execute(mapper)
      mapper.experiment_salt
    end
  end
end
