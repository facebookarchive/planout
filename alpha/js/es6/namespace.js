import Experiment from "./experiment.js";
import Assignment from "./assignment.js";
import { Sample, RandomInteger } from "./ops/random.js";
import { range, isObject, forEach } from "./lib/utils.js";


class DefaultExperiment extends Experiment {
  configure_logger() {
    return;
  }

  setup() {
    this.name = 'test_name';
  }

  log(data) {
    return;
  }

  previously_logged() {
    return true;
  }

  assign(params, args) {
    return;
  }
}

class Namespace {

  add_experiment(name, obj, segments) {
    throw "IMPLEMENT add_experiment";
  }

  remove_experiment(name) {
    throw "IMPLEMENT remove_experiment";
  }

  set_auto_exposure_logging(value) {
    throw "IMPLEMENT set_auto_exposure_logging";
  }

  in_experiment() {
    throw "IMPLEMENT in_experiment";
  }

  get(name, default_val) {
    throw "IMPLEMENT get";
  }

  log_exposure(extras) {
    throw "IMPLEMENT log_exposure";
  }

  log_event(event_type, extras) {
    throw "IMPLEMENT log_event";
  }

  require_experiment() {
    if (!this._experiment) {
      this._assign_experiment();
    }
  }

  require_default_experiment() {
    if (!this._default_experiment) {
      this._assign_default_experiment();
    }
  }
}

class SimpleNamespace extends Namespace {
  
  constructor(args) {
    super(args);
    this.name = this.getDefaultNamespaceName();
    this.inputs = args;
    this.num_segments = 1;
    this.segment_allocations = {};
    this.current_experiments = {};

    this._experiment = null;
    this._default_experiment = null;
    this.default_experiment_class = DefaultExperiment
    this._in_experiment = false;

    this.setup();
    this.available_segments = range(this.num_segments);

    this.setup_experiments();
  }

  setup() {
    throw "IMPLEMENT setup";
  }

  setup_experiments() {
    throw "IMPLEMENT setup_experiments";
  }

  get_primary_unit() {
    return this._primary_unit;
  }

  set_primary_unit(value) {
    this._primary_unit = value;
  }

  add_experiment(name, exp_object, segments) {
    var number_available = this.available_segments.length;
    if (number_available < segments) {
      return false;
    } else if (this.current_experiments[name] !== undefined) {
      return false;
    }
    var a = new Assignment(this.name);
    a.set('sampled_segments', new Sample({'choices': this.available_segments, 'draws': segments, 'unit': name}));
    var sample = a.get('sampled_segments');
    for(var i = 0; i < sample.length; i++) {
      this.segment_allocations[sample[i]] = name;
      this.available_segments.splice(this.available_segments.indexOf(sample[i]), 1);
    }
    this.current_experiments[name] = exp_object
    
  }

  remove_experiment(name) {
    if (this.current_experiments[name] === undefined) {
      return false;
    }

    var segments_to_free = [];
    forEach(Object.keys(this.segment_allocations), (cur) => {
      if(this.segment_allocations[cur] === name) {
        segments_to_free.push(cur);
      }
    });
    for (var i = 0; i < segments_to_free.length; i++) {
      var segment = segments_to_free[i];
      delete this.segment_allocations[segment];
      this.available_segments.push(segment);
    }
    delete this.current_experiments[name];
    return true;
  }

  get_segment() {
    var a = new Assignment(this.name);
    var segment = new RandomInteger({'min': 0, 'max': this.num_segments-1, 'unit': this.inputs[this.get_primary_unit()]});
    a.set('segment', segment);
    return a.get('segment');
  }

  _assign_experiment() {
    var in_experiment = false;
    var segment = this.get_segment();

    if (this.segment_allocations[segment] !== undefined) {
      var experiment_name = this.segment_allocations[segment];
      var experiment = new this.current_experiments[experiment_name](this.inputs);
      experiment.set_name(`${this.name}-${experiment_name}`);
      experiment.set_salt(`${this.name}-${experiment_name}`);
      this._experiment = experiment;
      this._in_experiment = experiment.in_experiment();
      if (!this._in_experiment) {
        this._assign_default_experiment();
      }
    }
  }

  _assign_default_experiment() {
    this._default_experiment = new this.default_experiment_class(this.inputs);
  }

  default_get(name, default_val) {
    super.require_default_experiment();
    return this._default_experiment.get(name, default_val);
  }

  in_experiment() {
    super.require_experiment();
    return this._in_experiment;
  }

  set_auto_exposure_logging(value) {
    super.require_experiment();
    this._experiment.set_auto_exposure_logging(value);
  }

  get(name, default_val) {
    super.require_experiment();
    if (!this._experiment) {
      return this.default_get(name, default_val);
    } else {
      return this._experiment.get(name, this.default_get(name, default_val));
    }
  }

  log_exposure(extras) {
    super.require_experiment();
    if (!this.experiment) {
      return;
    }
    this._experiment.log_exposure(extras);
  }

  log_event(event_type, extras) {
    super.require_experiment();
    if (!this._experiment) {
      return;
    }
    this._experiment.log_event(event_type, extras);

  }

  //helper function to return the class name of the current experiment class
  getDefaultNamespaceName() {
    if (isObject(this) && this.constructor && this !== this.window) {
      var arr = this.constructor.toString().match(/function\s*(\w+)/);
      if (arr && arr.length === 2) {
        return arr[1];
      }
    }
    return "GenericNamespace";
  }
}

export { Namespace, SimpleNamespace }