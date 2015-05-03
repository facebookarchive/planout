var Interpreter = require('/Users/garidor1/Desktop/planout/js/es6/interpreter');
var compiled = 
{"op":"seq","seq":[{"op":"set","var":"group_size","value":{"choices":{"op":"array","values":[1,10]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"specific_goal","value":{"p":0.8,"unit":{"op":"get","var":"userid"},"op":"bernoulliTrial"}},{"op":"cond","cond":[{"if":{"op":"get","var":"specific_goal"},"then":{"op":"seq","seq":[{"op":"set","var":"ratings_per_user_goal","value":{"choices":{"op":"array","values":[8,16,32,64]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"ratings_goal","value":{"op":"product","values":[{"op":"get","var":"group_size"},{"op":"get","var":"ratings_per_user_goal"}]}}]}}]}]};
var interpreter_salt = 'foo';

describe("Test interpreter", function() {
	it('should interpret properly', function() {
		var proc = new Interpreter(compiled, interpreter_salt, { 'userid': 123454});
		var params = proc.get_params();
	});
});
/*class InterpreterTest(unittest.TestCase):
    compiled = json.loads("""
{"op":"seq","seq":[{"op":"set","var":"group_size","value":{"choices":{"op":"array","values":[1,10]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"specific_goal","value":{"p":0.8,"unit":{"op":"get","var":"userid"},"op":"bernoulliTrial"}},{"op":"cond","cond":[{"if":{"op":"get","var":"specific_goal"},"then":{"op":"seq","seq":[{"op":"set","var":"ratings_per_user_goal","value":{"choices":{"op":"array","values":[8,16,32,64]},"unit":{"op":"get","var":"userid"},"op":"uniformChoice"}},{"op":"set","var":"ratings_goal","value":{"op":"product","values":[{"op":"get","var":"group_size"},{"op":"get","var":"ratings_per_user_goal"}]}}]}}]}]}
  """)
    interpreter_salt = 'foo'

    def test_interpreter(self):
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123454})
        params = proc.get_params()
        self.assertEqual(proc.get_params().get('specific_goal'), 1)
        self.assertEqual(proc.get_params().get('ratings_goal'), 320)

    def test_interpreter_overrides(self):
        # test overriding a parameter that gets set by the experiment
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123454})
        proc.set_overrides({'specific_goal': 0})
        self.assertEqual(proc.get_params().get('specific_goal'), 0)
        self.assertEqual(proc.get_params().get('ratings_goal'), None)

        # test to make sure input data can also be overridden
        proc = Interpreter(
            self.compiled, self.interpreter_salt, {'userid': 123453})
        proc.set_overrides({'userid': 123454})
        self.assertEqual(proc.get_params().get('specific_goal'), 1)
*/