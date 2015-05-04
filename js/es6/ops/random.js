import { PlanOutOpSimple } from "/Users/garidor1/Desktop/planout/js/es6/ops/base";
import sha1 from "js-sha1";
import _ from "underscore";
import BigNumber from "bignumber.js"

class PlanOutOpRandom extends PlanOutOpSimple {

	constructor(args) {
		super(args);
		this.LONG_SCALE = parseFloat(0xFFFFFFFFFFFFF);
	}

	getUnit(appended_unit) {
		var unit = this.getArgMixed('unit');
		if (Object.prototype.toString.call( unit ) !== '[object Array]') {
			unit = [unit];
		}
		if (appended_unit) {
			unit += [appended_unit]
		}
		return unit;
	}

	getUniform(min_val, max_val, appended_unit) {
		min_val = typeof min_val !== 'undefined' ? min_val : 0.0;
		max_val = typeof max_val !== 'undefined' ? max_val : 1.0;
		var zero_to_one = this.getHash(appended_unit) / this.LONG_SCALE;
		return min_val + (max_val - min_val) * zero_to_one;
	}

	getHash(appended_unit) {
		var full_salt;
		if (this.args.full_salt) {
			full_salt = this.getArgString('full_salt');
		} else {
			var salt = this.getArgString('salt');
			full_salt = this.mapper.get('experiment_salt') + "." + salt;
		}


		var unit_str = _.map(this.getUnit(appended_unit), element =>
			String(element)
		).join('.');
		var hash_str = full_salt + "." + unit_str;
		var hash = sha1(hash_str);
		//return this.hashCode(hash_str);
		//console.log(intHash)
		//var big = new BigNumber(hash.substr(0, 15));
		//return big;
		return parseInt(hash.substr(0, 13), 16);
	}

	hashCode(str) {
		var ret = 0;
  		for(i = 0, len = str.length; i < len; i++) {
   			ret = (31 * ret + str.charCodeAt(i)) << 1;
  		}
  		return ret;
	}

}

class RandomFloat extends PlanOutOpRandom {

    simpleExecute() {
        var min_val = this.getArgNumber('min');
        var max_val = this.getArgNumber('max');

        return this.getUniform(min_val, max_val);
    }
}

class RandomInteger extends PlanOutOpRandom {
	simpleExecute() {
        var min_val = this.getArgNumber('min');
        var max_val = this.getArgNumber('max');

        return min_val + this.getHash() % (max_val - min_val + 1);
     }
}

class BernoulliTrial extends PlanOutOpRandom {

	simpleExecute() {
		var p = this.getArgNumber('p');
		if (p < 0 || p > 1) {
			throw "Invalid probability";
		}
		if (this.getUniform(0.0, 1.0) <= p) {
			return 1;
		} else {
			return 0;
		}
	}
}

class BernoulliFilter extends PlanOutOpRandom {
	simpleExecute() {
		var p = this.getArgNumber('p');
		var values = this.getArgList('choices');
		if (p < 0 || p > 1) {
			throw "Invalid probability";
		}
		if (values.length == 0) {
			return [];
		}
		var ret = [];
		for (let i of values) {
			if (this.getUniform(0.0, 1.0, i) <= p) {
				ret.push(i);
			}
		}
		return ret;
	}
}

class UniformChoice extends PlanOutOpRandom {
	simpleExecute() {
		var choices = this.getArgList('choices');
		if (choices.length === 0) {
			return [];
		}
		var rand_index = this.getHash() % choices.length;
		//console.log(this.getHash());
		return choices[rand_index];
	}
}

class WeightedChoice extends PlanOutOpRandom {
	simpleExecute() {
		var choices = this.getArgList('choices');
		var weights = this.getArgList('weights');
		if (choices.length === 0) {
			return [];
		}
		var cum_sum = 0;
		var cum_weights = _.map(weights, function(weight) {
			cum_sum += weight;
			return cum_sum;
		});

		var stop_val = this.getUniform(0.0, cum_sum);
		return _.reduce(cum_weights, function(ret_val, cur_val) {
			if (ret_val) {
				return ret_val;
			}
			if (stop_val <= cur_val) {
				return cur_val;
			}
			return ret_val;
		}, null);
	}
}

class Sample extends PlanOutOpRandom {

	//http://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
	shuffle(array) {
		for (var i = array.length - 1; i > 0; i--) {
		  var j = Math.floor(Math.random() * (i + 1));
		  var temp = array[i];
		  array[i] = array[j];
		  array[j] = temp;
		}
		return array;
	}

	simpleExecute() {
		var choices = _.clone(this.getArgList('choices'));
		var num_draws = 0;
		if (this.args.draws) {
			num_draws = this.args.draws;
		} else {
			num_draws = choices.length;
		}
		var shuffled_arr = shuffle(choices);
		return shuffled_arr.slice(0, num_draws);
	}
}

export default {PlanOutOpRandom, Sample, WeightedChoice, UniformChoice, BernoulliFilter, BernoulliTrial, RandomInteger, RandomFloat };