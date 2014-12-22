require_relative '../test_helper'
require_relative '../../examples/plan_out/voting_experiment'

module PlanOut
  class ExperimentTest < Minitest::Test
    def setup
      @voting_experiment = VotingExperiment.new(userid: 14)
      @voting_experiment2 = VotingExperiment.new(userid: 15)
      @voting_experiment.auto_exposure_log = false
      @voting_experiment2.auto_exposure_log = false
    end

    def test_get_attributes
      assert_equal('ff0000', @voting_experiment.get(:button_color))
      assert_equal(1, @voting_experiment.get(:missing_key, 1))
      assert_equal('ff0000', @voting_experiment2.get(:button_color))
      assert_equal("I'm voting", @voting_experiment.get(:button_text))
      assert_equal("I'm voting", @voting_experiment2.get(:button_text))
    end

    def test_get_params
      assert_equal({ button_color: 'ff0000', button_text: "I'm voting" }, @voting_experiment.get_params)
      assert_equal({ button_color: 'ff0000', button_text: "I'm voting" }, @voting_experiment2.get_params)
    end

    def test_as_blob
      result = @voting_experiment.as_blob
      assert_equal('PlanOut::VotingExperiment', result[:name])
      assert_equal('PlanOut::VotingExperiment', result[:salt])
      assert_equal({ userid: 14 }, result[:inputs])
    end
  end
end
