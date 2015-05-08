var Interpreter = require('../es6/interpreter');

var compiled = 
{"op":"seq","seq":[{"op":"set","var":"group_size","value":{"choices":{"op":"array","values":[1,10]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"specific_goal","value":{"p":0.8,"unit":{"op":"get","var":"userid"},"op":"bernoulliTrial"}},{"op":"cond","cond":[{"if":{"op":"get","var":"specific_goal"},"then":{"op":"seq","seq":[{"op":"set","var":"ratings_per_user_goal","value":{"choices":{"op":"array","values":[8,16,32,64]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"ratings_goal","value":{"op":"product","values":[{"op":"get","var":"group_size"},{"op":"get","var":"ratings_per_user_goal"}]}}]}}]}]};
var interpreter_salt = 'foo';

describe("Test interpreter", function() {
	it('should interpret properly', function() {
		var proc = new Interpreter(compiled, interpreter_salt, { 'userid': 123454});
    expect(proc.get_params().specific_goal).toEqual(1);
    expect(proc.get_params().ratings_goal).toEqual(320);

	});
  it('should allow overrides', functio{n() {
    var proc = new Interpreter(compiled, interpreter_salt, { 'userid': 123454});
    proc.set_overrides({'specific_goal': 0});
    expect(proc.get_params().specific_goal).toEqual(0);
    expect(proc.get_params().ratings_goal).toEqual(undefined);

    proc = new Interpreter(compiled, interpreter_salt, { 'userid': 123453});
    proc.set_overrides({'userid': 123454});
    expect(proc.g}et_params().specific_goal).toEqual(1);
  });
});
