var Interpreter = require('/Users/garidor1/Desktop/planout/js/es6/interpreter');
/*
function runConfig(config, init={}) {
	var interpreter = new Interpreter(config, 'test_salt', init);
	return interpreter.get_params();
}

function run_config_single(config) {
	var x_config = {'op': 'set', 'var': 'x', 'value': config};
	return runConfig(x_config)['x'];
}

describe ("Test core operators", function() {
	it('should set appropriately', function() {
		var c = {'op': 'set', 'value': 'x_val', 'var': 'x'}
		var d = runConfig(c);
		expect(d).toEqual({ 'x': 'x_val'});
	});

	it('should work with seq', function() {
		var config = {'op': 'seq', 'seq': [
            {'op': 'set', 'value': 'x_val', 'var': 'x'},
            {'op': 'set', 'value': 'y_val', 'var': 'y'}
        ]};
        var d = runConfig(config)
        expect(d).toEqual({'x': 'x_val', 'y': 'y_val'});
	});

	it('should work with arr', function() {
		var arr = [4, 5, 'a']
        var a = run_config_single({'op': 'array', 'values': arr})
        expect(arr).toEqual(a);
	});

	it('should work with get', function() {
		var d = runConfig({
            'op': 'seq',
            'seq': [
                {'op': 'set', 'var': 'x', 'value': 'x_val'},
                {'op': 'set', 'var': 'y', 'value': {'op': 'get', 'var': 'x'}}
            ]
        });
        expect({'x': 'x_val', 'y': 'x_val'}).toEqual(d);
	});

	it('should work with cond', function() {
		var getInput = function(i, r) {
			return {'op': 'equals', 'left': i, 'right': r};
		};
		var testIf = function(i) {
			return runConfig({
				'op': 'cond',
           		'cond': [
	                {'if': getInput(i, 0),
	                 'then': {'op': 'set', 'var': 'x', 'value': 'x_0'}},
	                {'if': getInput(i, 1),
	                 'then': {'op': 'set', 'var': 'x', 'value': 'x_1'}}
            	]
			});
		};
		expect(testIf(0)).toEqual({ 'x': 'x_0'});
		expect(testIf(1)).toEqual({ 'x': 'x_1'});
	});

	it('should work with index', function() {
		var array_literal = [10, 20, 30];
		var obj_literal = {'a': 42, 'b': 43};

        var x = run_config_single(
            {'op': 'index', 'index': 0, 'base': array_literal}
        )
        expect(x).toEqual(10);
        
        x = run_config_single(
            {'op': 'index', 'index': 2, 'base': array_literal}
        )
        expect(x).toEqual(30);

        x = run_config_single(
            {'op': 'index', 'index': 'a', 'base': obj_literal}
        )
        expect(x).toEqual(42);

        x = run_config_single(
            {'op': 'index', 'index': 6, 'base': array_literal}
        )
        expect(x).toBe(undefined);

        x = run_config_single(
            {'op': 'index', 'index': 'c', 'base': obj_literal}
        )
        expect(x).toBe(undefined);

        x = run_config_single({
            'op': 'index',
            'index': 2,
            'base': {'op': 'array', 'values': array_literal}
        });
        expect(x).toEqual(30);
    });

	it('should work with length', function() {
		var arr = [0, 1, 2, 3, 4, 5];
        var length_test = run_config_single({'op': 'length', 'value': arr});
        expect(length_test).toEqual(arr.length);
        length_test = run_config_single({'op': 'length', 'value': []});
        expect(length_test).toEqual(0);
        length_test = run_config_single({'op': 'length', 'value':
                                        	{'op': 'array', 'values': arr}
                                        });
       	expect(length_test).toEqual(arr.length);
	});

	it('should work with not', function() {
		var x = run_config_single({'op': 'not', 'value': 0})
        expect(x).toBe(true);

        x = run_config_single({'op': 'not', 'value': false});
        expect(x).toBe(true);

        x = run_config_single({'op': 'not', 'value': 1})
        expect(x).toBe(false);

        x = run_config_single({'op': 'not', 'value': true});
        expect(x).toBe(false);
	});

	it('should work with or', function() {
		var x = run_config_single({
            'op': 'or',
            'values': [0, 0, 0]})
        expect(x).toBe(false);

        x = run_config_single({
            'op': 'or',
            'values': [0, 0, 1]})
        expect(x).toBe(true);

        x = run_config_single({
            'op': 'or',
            'values': [false, true, false]})
        expect(x).toBe(true);
	});    

	it('should work with and', function() {
		var x = run_config_single({
            'op': 'and',
            'values': [1, 1, 0]})
        expect(x).toEqual(false);

        x = run_config_single({
            'op': 'and',
            'values': [0, 0, 1]})
       expect(x).toBe(false);

        x = run_config_single({
            'op': 'and',
            'values': [true, true, true]})
        expect(x).toBe(true);
	});

	it('should work with commutative operators', function() {
        var arr = [33, 7, 18, 21, -3];

        var min_test = run_config_single({'op': 'min', 'values': arr});
        expect(min_test).toEqual(-3);

        var max_test = run_config_single({'op': 'max', 'values': arr});
        expect(max_test).toEqual(33);

        var sum_test = run_config_single({'op': 'sum', 'values': arr});
        expect(sum_test).toEqual(76);

        var product_test = run_config_single({'op': 'product', 'values': arr});
        expect(product_test).toEqual(-261954);
	});

	it('should work with binary operators', function() {
        var eq = run_config_single({'op': 'equals', 'left': 1, 'right': 2});
        expect(eq).toEqual(1 == 2);

        eq = run_config_single({'op': 'equals', 'left': 2, 'right': 2});
        expect(eq).toEqual(2 == 2);
   
        var gt = run_config_single({'op': '>', 'left': 1, 'right': 2});
        expect(gt).toEqual(1 > 2);
        
        var lt = run_config_single({'op': '<', 'left': 1, 'right': 2});
        expect(lt).toEqual(1 < 2);
        
        var gte = run_config_single({'op': '>=', 'left': 2, 'right': 2});
        expect(gte).toEqual(2 >= 2);
        gte = run_config_single({'op': '>=', 'left': 1, 'right': 2});
        expect(gte).toEqual(1 >= 2);

        var lte = run_config_single({'op': '<=', 'left': 2, 'right': 2});
        expect(lte).toEqual(2 <= 2);

        var mod = run_config_single({'op': '%', 'left': 11, 'right': 3});
        expect(mod).toEqual(11 % 3);

        var div = run_config_single({'op': '/', 'left': 3, 'right': 4})
        expect(div).toEqual(0.75);
	});

	it('should work with return', function() {
		var return_runner = function(return_value) {
            var config = {
                "op": "seq",
                "seq": [
                    {
                      "op": "set",
                      "var": "x",
                      "value": 2
                    },
                    {
                        "op": "return",
                        "value": return_value
                    },
                    {
                        "op": "set",
                        "var": "y",
                        "value": 4
                    }
                ]
            };
	        var e = new Interpreter(config, 'test_salt');
            return e;
        };
        var i = return_runner(true);
        expect(i.get_params()).toEqual({'x': 2});
        expect(i.in_experiment()).toEqual(true);

        i = return_runner(42);
        expect(i.get_params()).toEqual({ 'x': 2});
        expect(i.in_experiment()).toEqual(true);

        i = return_runner(false);
        expect(i.get_params()).toEqual({ 'x': 2});
        expect(i.in_experiment()).toEqual(false);

        i = return_runner(0);
        expect(i.get_params()).toEqual({ 'x': 2});
        expect(i.in_experiment()).toEqual(false);
	});

});*/