var Interpreter = require('../es6/interpreter');
var UniformChoice = require('../es6/ops/random').UniformChoice;
var Experiment = require('../es6/experiment');

var global_log = [];

describe("Test the experiment module", function() {

	var validate_log;
	var experiment_tester;
	beforeEach(function() {
		validate_log = function (blob, expected_fields) {
			if (!expected_fields || !blob) { return; }
			Object.keys(expected_fields).forEach(function(field) {
				expect(blob[field]).not.toBe(undefined);
				if (expected_fields[field] !== undefined) {
					validate_log(blob[field], expected_fields[field]);
				}
			});
		};

		experiment_tester = function (exp_class, in_experiment) {
			if (in_experiment === undefined) { in_experiment = true; }
			console
			global_log = [];
			var e = new exp_class({ 'i': 42});
			e.set_overrides({'bar': 42});
			var params = e.get_params();

			expect(params['foo']).not.toBe(undefined);
			expect(params['foo']).toEqual('b');
			expect(params['bar']).toEqual(42);

			if (in_experiment) {
				expect(global_log.length).toEqual(1);
				validate_log(global_log[0], { 
					'inputs': { 'i': null },
					'params': { 'foo': null, 'bar': null}
				});
			} else {
				expect(global_log.length).toEqual(0);
			}

			expect(e.in_experiment(), in_experiment);
		};
	});

	it('should work with basic experiments', function() {
		class TestVanillaExperiment extends Experiment {
			configure_logger() {
				return;
			}
			log(stuff) {
				global_log.push(stuff);
			}
			previously_logged() {
				return;
			}
			setup() {
				this.name = 'test_name';
			}
			assign(params, args) {
				params.set('foo', new UniformChoice({'choices': ['a', 'b'], 'unit': args.i}));
			}
		}
		experiment_tester(TestVanillaExperiment);
	});

	it('should be able to disable an experiment', function() {
		class TestVanillaExperiment extends Experiment {
			configure_logger() {
				return;
			}
			log(stuff) {
				global_log.push(stuff);
			}
			previously_logged() {
				return;
			}
			setup() {
				this.name = 'test_name';
			}
			assign(params, args) {
				params.set('foo', new UniformChoice({'choices': ['a', 'b'], 'unit': args.i}));
				this._in_experiment = false;
			}
		}
		experiment_tester(TestVanillaExperiment, false);
	});

	it('should only assign once', function() {

		class TestSingleAssignment extends Experiment {

			configure_logger() {
				return;
			}

			log(stuff) {
				global_log.push(stuff);
			}

			previously_logged() {
				return;
			}

			setup() {
				this.name = 'test_name';
			}

			assign(params, args) {
				params.set('foo', new UniformChoice({'choices': ['a', 'b'], 'unit': args.i}));
				var counter = args.counter;
				if (!counter.count) { counter.count = 0; }
				counter.count = counter.count + 1;
			}
		}

        var assignment_count = {'count': 0};
        var e = new TestSingleAssignment({'i': 10, 'counter': assignment_count});
        expect(assignment_count.count).toEqual(0);
        e.get('foo');
        expect(assignment_count.count).toEqual(1);
        e.get('foo');
        expect(assignment_count.count).toEqual(1);
	});

	it('should work with an interpreted experiment', function() {
		class TestInterpretedExperiment extends Experiment {
			configure_logger() {
				return;
			}
			log(stuff) {
				global_log.push(stuff);
			}
			previously_logged() {
				return;
			}
			setup() {
				this.name = 'test_name';
			}

			assign(params, args) {
				var compiled = 
					{"op":"seq",
			           "seq": [
			            {"op":"set",
			             "var":"foo",
			             "value":{
			               "choices":["a","b"],
			               "op":"uniformChoice",
			               "unit": {"op": "get", "var": "i"}
			               }
			            },
			            {"op":"set",
			             "var":"bar",
			             "value": 41
			            }
	           		]};
	           	var proc = new Interpreter(compiled, this.get_salt(), args, params);
	           	var par = proc.get_params();
	           	Object.keys(par).forEach(function(param) {
	           		params.set(param, par[param]);
	           	});
			}
		};
		experiment_tester(TestInterpretedExperiment);
	});
});
