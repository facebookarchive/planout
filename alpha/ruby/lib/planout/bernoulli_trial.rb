require_relative 'op_random'

module Planout
  class BernoulliTrial < OpRandom
    def simple_execute
      p = @parameters[:p]
      rand_val = get_uniform(0.0, 1.0)
      (rand_val <= p) ? 1 : 0
    end
  end
end
