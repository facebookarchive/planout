require_relative '../test_helper'

module PlanOut
  class AssignmentTest < Minitest::Test
    def setup
      @assignment = Assignment.new('mtsalt')
    end

    def test_salt
      assert_equal('mtsalt', @assignment.experiment_salt)
    end

    def test_evaluate
      assert_equal(1, @assignment.evaluate(1))
      assert_equal(2, @assignment.evaluate(2))
    end

    def test_set
      @assignment.set(:color, 'green')
      @assignment.set('platform', 'ios')
      @assignment.set('foo', UniformChoice.new({ unit: 1, choices: ['x', 'y'] }))
      assert_equal('green', @assignment.data[:color])
      assert_equal('ios', @assignment.data[:platform])
      assert_equal('y', @assignment.data[:foo])
    end

    def test_get
      @assignment.set(:button_text, 'Click Me!')
      @assignment.set(:gender, 'f')
      assert_equal('Click Me!', @assignment.get('button_text'))
      assert_equal('f', @assignment.get('gender'))
      assert_equal(10, @assignment.get('missing_key', 10))
      assert_nil(@assignment.get('missing_key'))
    end

    def test_get_params
      @assignment.set('foo', 'bar')
      @assignment.set(:baz, 'qux')
      assert_equal({ foo: 'bar', baz: 'qux' }, @assignment.get_params)
    end
  end
end
