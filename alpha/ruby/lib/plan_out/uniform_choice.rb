require_relative 'op_random'

module PlanOut
  class UniformChoice < OpRandom
    def simple_execute
      choices = @parameters[:choices]
      return [] if choices.length() == 0
      rand_index = get_hash() % choices.length()
      choices[rand_index]
    end
  end
end
