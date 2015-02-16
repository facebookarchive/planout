require_relative '../test_helper'

module PlanOut
  class OperatorTest < Minitest::Test
    def setup
      @a = Assignment.new('mtsalt')
    end

    def test_execute
      operator = Operator.new({ foo: 'bar' })
      op_simple = OpSimple.new({ bar: 'qux' })
      assert_equal('mtsalt', operator.execute(@a))
      assert_equal(-1, op_simple.execute(@a))
    end

    def test_weighted_choice
      weighted = WeightedChoice.new({
        choices: ["c1", "c2", "c1"],
        weights: [20, 40, 60],
        unit: 42,
        salt:'x'
      })
      assert_equal("c2", weighted.execute(@a))
    end
  end
end
