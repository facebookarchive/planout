import {PlanOutOp, PlanOutOpSimple, PlanOutOpBinary, PlanOutOpUnary, PlanOutOpCommutative} from "./base";
import _ from "underscore";
import {isOperator, StopPlanOutException} from "./utils";

class Literal extends PlanOutOp {
	execute(mapper) {
		return this.getArgMixed('value');
	}
}

class Get extends PlanOutOp {
	execute(mapper) {
		return mapper.get(this.getArgString('var'));
	}
}

class Seq extends PlanOutOp {
	execute(mapper) {
		_.each(this.getArgList('seq'), function(op) {
			mapper.evaluate(op);
		});
	}
}


class Return extends PlanOutOp {
	execute(mapper) {
		var value = mapper.evaluate(this.getArgMixed('value'));
		var in_experiment = false;
		if(value) {
			in_experiment = true;
		}
		throw new StopPlanOutException(in_experiment);
	}
}


class Set extends PlanOutOp {
	execute(mapper) {
		let variable = this.getArgString('var');
		let value = this.getArgMixed('value');
		if (mapper.has_override(variable)) {
			return;
		}
		
		if (isOperator(value) && !value.salt) {
			value.salt = variable;
		}

		if (variable == "experiment_salt") {
			mapper.experiment_salt = value;
		}
		mapper.set(variable, mapper.evaluate(value));
	}
}

class Arr extends PlanOutOp {
	execute(mapper) {
		return _.map(this.getArgList('values'), function(value) {
			return mapper.evaluate(value);
		});
	}
}

class Coalesce extends PlanOutOp {
	execute(mapper) {
		for (let x of this.getArgList('values')) {
			var eval_x = mapper.evaluate(x);
			if (!eval_x) {
				return eval_x;
			}
		}
		return null;
	}
}

class Index extends PlanOutOpSimple {
	simpleExecute() {
		var base = this.getArgIndexish('base');
		var index = this.getArgMixed('index');
		if (typeof(index) === "number") {
			if (index >=0 && index < base.length) {
				return base[index];
			} else {
				return undefined;
			}
		} else {
			return base[index];
		}
	}
}

class Cond extends PlanOutOp {
	execute(mapper) {
		let list = this.getArgList('cond');
		for (let i in list) {
			var if_clause = list[i]['if'];
			var then_clause = list[i]['then'];
			if (mapper.evaluate(if_clause)) {
				return mapper.evaluate(then_clause);
			}
		}
		return null;
	}
}

class And extends PlanOutOp {
	execute(mapper) {
		return _.reduce(this.getArgList('values'), function(ret, clause) {
			if (!ret) { return ret; }

			return Boolean(mapper.evaluate(clause));
		}, true);
	}
}

class Or extends PlanOutOp {
	execute(mapper) {
		return _.reduce(this.getArgList('values'), function(ret, clause) {
			if (ret) { return ret; }

			return Boolean(mapper.evaluate(clause));
		}, false);
	}
}

class Product extends PlanOutOpCommutative {
	commutativeExecute(values) {
		return _.reduce(values, function(memo, value) {
			return memo * value;
		}, 1);
	}
}

class Sum extends PlanOutOpCommutative {
	commutativeExecute(values) {
		return _.reduce(values, function(memo, value) {
			return memo + value;
		}, 0);
	}
}

class Equals extends PlanOutOpBinary {
	getInfixString() {
		return "==";
	}

	binaryExecute(left, right) {
		return left === right;
	}
}

class GreaterThan extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return left > right;
	}
}

class LessThan extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return left < right;
	}
}

class LessThanOrEqualTo extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return left<= right;
	}
}

class GreaterThanOrEqualTo extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return left >= right;
	}
}

class Mod extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return left % right;
	}
}

class Divide extends PlanOutOpBinary {
	binaryExecute(left, right) {
		return parseFloat(left) / parseFloat(right);
	}
}

class Round extends PlanOutOpBinary {
	unaryExecute(value) {
		return Math.round(value);
	}
}

class Not extends PlanOutOpUnary {
	getUnaryString() {
		return '!';
	}

	unaryExecute(value) {
		return !value;
	}
}

class Negative extends PlanOutOpUnary {
	getUnaryString() {
		return '-';
	}

	unaryExecute(value) {
		return  0 - value;
	}
}

class Min extends PlanOutOpCommutative {
	commutativeExecute(values) {
		return Math.min.apply(null, values);
	}
}

class Max extends PlanOutOpCommutative {
	commutativeExecute(values) {
		return Math.max.apply(null, values);
	}
}

class Length extends PlanOutOpUnary {
	unaryExecute(value) {
		return value.length;
	}
}

export { Literal, Get, Seq, Set, Arr, Coalesce, Index, Cond, And, Or, Product, Sum, Equals, GreaterThan, LessThan, LessThanOrEqualTo, GreaterThanOrEqualTo, Mod, Divide, Round, Not, Negative, Min, Max, Length, Return }