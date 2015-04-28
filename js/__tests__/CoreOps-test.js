jest.dontMock('/Users/garidor1/Desktop/planout/js/es6/interpreter');
jest.dontMock('/Users/garidor1/Desktop/planout/js/es6/assignment');


function runConfig(config, init={}) {
	var interpret = require('/Users/garidor1/Desktop/planout/js/es6/interpreter');
	var Interpreter = new interpret(config, 'test_salt', init);
	return Interpreter.get_params();
}
describe ("Test basic operators", function() {
	it('should set appropriately', function() {
		var c = {'op': 'set', 'value': 'x_val', 'var': 'x'}
		var d = runConfig(c);
		expect(d).toBe({ 'x': 'x_val'});
	});
});