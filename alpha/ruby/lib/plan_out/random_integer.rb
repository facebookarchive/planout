require_relative 'op_random'

module PlanOut
  class RandomInteger < OpRandom
    def simple_execute
      min_val = @parameters.fetch(:min, 0)
      max_val = @parameters.fetch(:max, 1)
      min_val + get_hash() % (max_val - min_val + 1)
    end
  end
end
