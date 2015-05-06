import _ from "underscore";
import { PlanOutOpRandom } from "./ops/random";

class Assignment {
	constructor(experiment_salt, overrides) {
        if (!overrides) {
            overrides = {};
        }
		this.experiment_salt = experiment_salt;
		this._overrides = _.clone(overrides);
		this._data = _.clone(overrides);
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
		if (name === '_data') {
            this._data = value;
            return;
        } else if (name === '_overrides') {
            this._overrides = value;
            return;
        } else if (name === 'experiment_salt') {
            this.experiment_salt = value;
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
            this._data[name] = value;
        }
     }

     get(name) {
     	if (name === '_data') {
            return this._data;
        } else if( name === '_overrides') {
            return this._overrides;
        } else if ( name === 'experiment_salt') {
            return this.experiment_salt;
     	} else {
     		return this._data[name];
     	}
     }

    get_params() {
        return this._data;
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
