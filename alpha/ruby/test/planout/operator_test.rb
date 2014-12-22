require_relative '../test_helper'

module Planout
  class OperatorTest < Minitest::Test
    def setup
      @operator = Operator.new({ foo: 'bar' })
      @op_simple = OpSimple.new({ bar: 'qux' })
    end

    def test_execute
      a = Assignment.new('mtsalt')
      assert_equal('mtsalt', @operator.execute(a))
      assert_equal(-1, @op_simple.execute(a))
    end
  end
end