import Assignment from './assignment';
import { clone, extend } from './lib/utils';

class Experiment {
	constructor(inputs) {
		this.logger_configured = false;
		this.inputs = inputs;
		this._exposure_logged = false;
		this._salt = null;
		this._in_experiment = true;

		this.name = "EXPERIMENT";
		this._auto_exposure_log = true;

		this.setup();

		this._assignment = new Assignment(this.get_salt());
		this._assigned = false;	
	}


	require_assignment() {
		if (!this._assigned) {
			this._assign();
		}
	}

	require_exposure_logging() {
		if (this._auto_exposure_log && !this._exposure_logged) {
			this.log_exposure();
		}
	}

	_assign() {
		this.configure_logger();
		this.assign(this._assignment, this.inputs);
		this._assigned = true;
	}

	setup() {
		return;
	}

	in_experiment() {
		return this._in_experiment;
	}

	set_overrides(value) {
		this._assignment.set_overrides(value);
		var o = this._assignment.get_overrides();
		var self = this;
		Object.keys(o).forEach(function(key) {
			if (self.inputs[key] !== undefined) {
				self.inputs[key] = o[key];
			}
		});
	}

	get_salt() {
		if (this._salt) {
			return this._salt;
		} else {
			return this.name;
		}
	}

	set_salt(value) {
		this._salt = value;
		if(this._assignment) {
			this._assignment.experiment_salt = value;
		}
	}

	get_name() {
		return this._name;
	}

	assign(params, args) {
		throw "IMPLEMENT THIS";
	}

	set_name(value) {
		var re = /\s+/g; 
		var name = value.replace(re, '-')
		if (this._assignment) {
			this._assignment.experiment_salt = this.get_salt();
		}
	}

	__asBlob(extras) {
		if (!extras) { extras = {}; }

		var d = { 
			'name': this.get_name(),
			'time': new Date().getTime() / 1000,
			'salt': this.get_salt(),
			'inputs': this.inputs,
			'params': this._assignment.get_params()
		};
		extend(d, extras);
    return d;
	}

	set_auto_exposure_logging(value) {
		this._auto_exposure_log = value;
	}

	get_params() {
		this.require_assignment();
		this.require_exposure_logging();
		return this._assignment.get_params();
	}

	get(name, def) {
		this.require_assignment();
		this.require_exposure_logging();
		return this._assignment.get(name, def);
	}

	toString() {
		this.require_assignment();
		this.require_exposure_logging();
		return JSON.stringify(this.__asBlob());
	}

	log_exposure(extras) {
		if (!this._in_experiment) {
			return;
		}
		this._exposure_logged = true;
		this.log_event('exposure', extras);
	}

	log_event(event_type, extras) {
		if (!this._in_experiment) {
			return;
		}

		var extra_payload;

		if(extras) {
			extra_payload = { 'event': event_type, 'extra_data': clone(extras)};
		} else {
			extra_payload = { 'event': event_type };
		}

		this.log(this.__asBlob(extra_payload));
	}

	configure_logger() {
		throw "IMPLEMENT THIS";
	}

	log(data) {
		throw "IMPLEMENT THIS";
	}

	previously_logged() {
		throw "IMPLEMENT THIS";
	}
}

export default Experiment;
