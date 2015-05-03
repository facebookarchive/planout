var Assignment = require('/Users/garidor1/Desktop/planout/js/es6/assignment');
var Random = require('/Users/garidor1/Desktop/planout/js/es6/ops/random');


var z = 3.29;


function assertProp(observed_p, expected_p, N) {
	var se = z * Math.sqrt(expected_p * (1 - expected_p) / N);
	console.log(observed_p);
	expect(Math.abs(observed_p - expected_p) <= se).toBe(true);
}

function sum(obj) {
	return obj.reduce(function(totalSum, cur) {
		return totalSum + cur;
	}, 0);
}

function valueMassToDensity(value_mass) {
	var values = value_mass.map(function(val) { return Object.keys(val)[0]; });
	var ns     = value_mass.map(function(val) { return val[Object.keys(val)[0]]});
	var ns_sum = parseFloat(sum(ns));
	ns         = ns.map(function(val) {
		return val / ns_sum;
	});
	var ret    = {};
	for (var i = 0; i < values.length; i++) {
		ret[values[i]] = ns[i];
	}
	return ret;
}

function Counter(l) {
	ret = {}
	l.forEach(function(el) {
		if (ret[el]) {
			ret[el] += 1;
		} else {
			ret[el] = 1;
		}
	});
	return ret;
}

function assertProbs(xs, value_density, N) {
	var hist = Counter(xs);
	Object.keys(hist).forEach(function(el) {
		assertProp(hist[el] / N, value_density[el], N);
	});
}

function distributionTester(xs, value_mass, N) {
	value_density = valueMassToDensity(value_mass);

	assertProbs(xs, value_density, parseFloat(N));
}

describe('Test randomization ops', function() {
	it('salts correctly', function() {
		var i = 20;
		var a = new Assignment("assign_salt_a");

		a.set('x', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i}));
		a.set('y', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i}));
		expect(a.get('x')).not.toEqual(a.get('y'));

		a.set('z', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i, 'salt': 'x'}));
		expect(a.get('x')).toEqual(a.get('z'));

		var b = new Assignment('assign_salt_b');
        b.set('x', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i}));
        expect(a.get('x')).not.toEqual(b.get('x'));

        a.set('f', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i, 'full_salt':'fs'}));
        b.set('f', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i, 'full_salt':'fs'}));
        expect(a.get('f')).toEqual(b.get('f'));

       	a.set('f', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i, 'full_salt':'fs2'}));
        b.set('f', new Random.RandomInteger({ 'min': 0, 'max': 100000, 'unit': i, 'full_salt':'fs2'}));
        expect(a.get('f')).toEqual(b.get('f'));

	});

	it('works for bernoulli trials', function() {
		var N = 10000;
		function bernoulli(p) {
			var xs = [];
			for (var i = 0; i < N; i++) {
				var a = new Assignment(p);
				a.set('x', new Random.BernoulliTrial({ 'p': p, 'unit': i }));
				xs[i] = a.get('x');
			}
			return xs;
		}
		
		distributionTester(bernoulli(0.0), [{0: 1}, {1: 0}], N);
		distributionTester(bernoulli(0.1), [{0: 0.9}, {1: 0.1}], N);
		distributionTester(bernoulli(1.0), [{0: 0}, {1: 1}], N);
	});

	it('works for uniform choice', function() {
		var N = 10000;
		function uniformChoice(choices) {
			var xs = [];
			for (var i = 0; i < N; i++) {
				var a = new Assignment(choices.join(','));
				a.set('x', new Random.UniformChoice({ 'choices': choices, 'unit': i }));
				xs[i] = a.get('x');
			}
			return xs;
		}
		distributionTester(uniformChoice(['a']), [{'a': 1}], N);
		distributionTester(uniformChoice(['a', 'b']), [{'a': 1}, {'b': 1}], N);
	});
});