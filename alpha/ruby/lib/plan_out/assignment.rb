module PlanOut
  class Assignment
    attr_accessor :experiment_salt, :data

    def initialize(experiment_salt)
      @experiment_salt = experiment_salt
      @data = {}
    end

    def evaluate(data)
      data
    end

    def get(var, default = nil)
      @data[var.to_sym] || default
    end

    # in python this would be defined as __setattr__ or __setitem__
    # not sure how to do this in Ruby.
    def set(name, value)
      if value.is_a? Operator
        value.args[:salt] = name if !value.args.has_key?(:salt)
        @data[name.to_sym] = value.execute(self)
      else
        @data[name.to_sym] = value
      end
    end

    def [](x)
      get(x)
    end

    def []=(x,y)
      set(x,y)
    end

    def get_params
      @data
    end
  end
end
