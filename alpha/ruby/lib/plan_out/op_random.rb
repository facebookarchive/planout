require_relative 'op_simple'

module PlanOut
  class OpRandom < OpSimple
    LONG_SCALE = Float(0xFFFFFFFFFFFFFFF)

    def get_unit(appended_unit = nil)
      unit = @parameters[:unit]
      unit = [unit] if !unit.is_a? Array
      unit += appended_unit if appended_unit != nil
      unit
    end

    def get_hash(appended_unit = nil)
      salt = @parameters[:salt]
      salty = "#{@mapper.experiment_salt}.#{salt}"
      unit_str = get_unit(appended_unit).join('.')
      x = "#{salty}.#{unit_str}"
      last_hex = (Digest::SHA1.hexdigest(x))[0..14]
      last_hex.to_i(16)
    end

    def get_uniform(min_val = 0.0, max_val = 1.0, appended_unit = nil)
      zero_to_one = self.get_hash(appended_unit)/LONG_SCALE
      min_val + (max_val-min_val) * zero_to_one
    end
  end
end
