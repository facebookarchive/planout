require_relative '../../lib/plan_out/simple_experiment'

module PlanOut
  class VotingExperiment < SimpleExperiment
    def setup; end

    def assign(params, **inputs)
      userid = inputs[:userid]
      params[:button_color] = UniformChoice.new({
        choices: ['ff0000', '00ff00'],
        unit: userid
      })

      params[:button_text] = UniformChoice.new({
        choices: ["I'm voting", "I'm a voter"],
        unit: userid,
        salt:'x'
      })
    end
  end

  if __FILE__ == $0
    (14..16).each do |i|
      my_exp = VotingExperiment.new(userid:i)
      # toggling the above disables or re-enables auto-logging
      #my_exp.auto_exposure_log = false
      puts "\ngetting assignment for user #{i} note: first time triggers a log event"
      puts "button color is #{my_exp.get(:button_color)} and button text is #{my_exp.get(:button_text)}"
    end
  end
end
