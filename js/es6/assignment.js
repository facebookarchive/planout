import _ from "underscore";
import PlanOutOpRandom from "/Users/garidor1/Desktop/planout/js/es6/ops/random";

class Assignment {
	constructor(experiment_salt, overrides) {
        if (!overrides) {
            overrides = {};
        }
		this.experiment_salt = experiment_salt;
		this._overrides = _.clone(overrides);
		this._data = _.clone(overrides);
		this.dict = {}
	}

	evaluate(value) {
		return value;
	}

	get_overrides() {
		return this._overrides;
	}

	set_overrides(overrides) {
		this._overrides = _.clone(overrides);
		var self = this;
		_.each(Object.keys(this._overrides), function(override_key) {
			self._data[override_key] = self._overrides[override_key];
		});
	}

	set(name, value) {

        console.log("HEREEE");
		if (name === '_data' || name === '_overrides' || name === 'experiment_salt') {
			this.dict[name] = value;
            return;
		}
		if (this._overrides[name]) {
            return;
        }

        if (value instanceof PlanOutOpRandom) {
        	if (!value.args.salt) {
        		value.args.salt = name;
        	}
        	this._data[name] = value.execute(this);
        } else {
            console.log("HEE");
            this._data[name] = value;
        }
     }

     get(name) {
     	if (name === '_data' || name === '_overrides' || name === 'experiment_salt') {
     		return this.dict[name];
     	} else {
     		return this._data[name];
     	}
     }

    del(name) {
    	delete this._data[name];
    }

    to_string() {
    	return String(this._data);
    }

    length() {
    	return Object.keys(this._data).length;
    }
};

export default Assignment;
