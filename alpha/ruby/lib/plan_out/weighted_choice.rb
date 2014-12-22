require_relative 'op_random'

module PlanOut
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
end
