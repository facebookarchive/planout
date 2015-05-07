import Assignment from './assignment';
import { initFactory, operatorInstance, StopPlanOutException } from './ops/utils';
import { shallowCopy, deepCopy, isObject, isArray, map } from "./lib/utils";

class Interpreter {
	constructor(serialization, experiment_salt='global_salt', inputs={}, environment) {
		this._serialization = serialization;
		if (!environment) {
			this._env = new Assignment(experiment_salt);
		} else {
			this._env = environment;
		}
		this.experiment_salt = this._experiment_salt = experiment_salt;
		this._evaluated = false;
		this._in_experiment = false;
		this._inputs = shallowCopy(inputs);
	}

	in_experiment() {
		return this._in_experiment;
	}

	set_env(new_env) {
		this._env = deepCopy(new_env);
		return this;
	}

	has(name) {
		return this._env[name];
	}

	get(name, default_val) {
		input_val = this._inputs[name];
		if (!input_val) {
			input_val = default_val;
		}
		env_val = this._env.get(name);
		if (env_val) { 
			return env_val;
		}
		return input_val;
	}

	get_params() {
		if (!this._evaluated) {
			try {
				this.evaluate(this._serialization);
			} catch(err) {
				if (err instanceof StopPlanOutException) {
					this._in_experiment = err.in_experiment;
				}
			}
			this._evaluated = true;
		}
		return this._env.get_params();
	}

	set(name, value) {
		this._env.set(name, value);
		return this;
	}

	set_overrides(overrides) {
		this._env.set_overrides(overrides);
		return this;
	}

	get_overrides() {
		return this._env.get_overrides();
	}

	has_override(name) {
		overrides = this.get_overrides();
		return overrides && overrides[name] !== undefined;
	}

	evaluate(planout_code) {
		if (isObject(planout_code) && planout_code.op) {
			
			return operatorInstance(planout_code).execute(this);
		} else if (isArray(planout_code)) {
			var self = this;
			return map(planout_code, function(obj) {
				return self.evaluate(obj);
			});
		} else {
			return planout_code;
		}
	}

}

export default Interpreter;
