require_relative 'op_random'

module PlanOut
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

  class UniformChoice < OpRandom
    def simple_execute
      choices = @parameters[:choices]
      return [] if choices.length() == 0
      rand_index = get_hash() % choices.length()
      choices[rand_index]
    end
  end
end