var Assignment = require('../es6/assignment');
var UniformChoice = require('../es6/ops/random').UniformChoice;

var tester_unit = '4';
var tester_salt = 'test_salt';


describe('Test the assignment module', function() {
	it('Should set constants correctly', function() {
		var a = new Assignment(tester_salt);
		a.set('foo', 12);
		expect(a.get('foo')).toBe(12);
	});
	it('Should work with uniform choice', function() {
		var a = new Assignment(tester_salt);
		var choices = ['a', 'b'];
		a.set('foo', new UniformChoice({'choices': choices, 'unit': tester_unit}));
		a.set('bar', new UniformChoice({'choices': choices, 'unit': tester_unit}));
		a.set('baz', new UniformChoice({'choices': choices, 'unit': tester_unit}));

		expect(a.get('foo')).toEqual('b');
		expect(a.get('bar')).toEqual('a');
		expect(a.get('baz')).toEqual('a');
	});

	it('Should work with overrides', function() {
    var a = new Assignment(tester_salt);
    a.set_overrides({'x': 42, 'y': 43})
    a.set('x', 5);
    a.set('y', 6);
    expect(a.get('x')).toEqual(42);
    expect(a.get('y')).toEqual(43);
	});
});
