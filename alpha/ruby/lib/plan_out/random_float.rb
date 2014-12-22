require_relative 'op_random'

module PlanOut
  class RandomFloat < OpRandom
    def simple_execute
      min_val = @parameters.fetch(:min, 0)
      max_val = @parameters.fetch(:max, 1)
      get_uniform(min_val, max_val)
    end
  end
end
