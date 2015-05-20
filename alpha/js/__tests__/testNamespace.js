var Namespace = require('../es6/namespace.js');
var Experiment = require('../es6/experiment.js');

var global_log = [];
class Experiment1 extends Experiment {
  configure_logger() {
    return;
  }

  log(data) {
    global_log.push(data);
  }

  previously_logged() {
    return true;
  }

  setup() {
    this.name = 'test_name';
  }

  assign(params, args) {
    params.set('test', 1)
  }
}

class Experiment2 extends Experiment {
  configure_logger() {
    return;
  }

  setup() {
    this.name = 'test_name';
  }

  log(data) {
    global_log.push(data);
  }

  previously_logged() {
    return true;
  }

  assign(params, args) {
    params.set('test', 2)
  }
}


describe("Test namespace module", function() {
  var validate_log;
  beforeEach(function() {
    validate_log = function(exp) {
      expect(global_log[0].salt).toEqual(`test-${exp}`)
    }

  });

  afterEach(function() {
    global_log = [];
  });
  it('Adds segment correctly', function() {
    class TestNamespace extends Namespace.SimpleNamespace {
      setup() {
        this.name = "test";
        this.num_segments = 100;
        this.set_primary_unit('userid');
      }

      setup_experiments() {
        this.add_experiment('Experiment1', Experiment1, 100);
      }
    }
    var namespace = new TestNamespace({'userid': 'blah'});
    expect(namespace.get('test')).toEqual(1);
    validate_log("Experiment1");
  });

  it('Adds two segments correctly', function() {
    class TestNamespace extends Namespace.SimpleNamespace {
      setup() {
        this.name = "test";
        this.num_segments = 100;
        this.set_primary_unit('userid');
      }

      setup_experiments() {
        this.add_experiment('Experiment1', Experiment1, 50);
        this.add_experiment('Experiment2', Experiment2, 50);
      }
    }
    var namespace = new TestNamespace({'userid': 'blah'});
    expect(namespace.get('test')).toEqual(1);
    validate_log("Experiment1");
    global_log = [];
    var namespace2 = new TestNamespace({'userid': 'abb'});
    expect(namespace2.get('test')).toEqual(2);
    validate_log("Experiment2");
  });

  it('Can remove segment correctly', function() {
    class TestNamespace extends Namespace.SimpleNamespace {
      setup() {
        this.name = "test";
        this.num_segments = 10;
        this.set_primary_unit('userid');
      }

      setup_experiments() {
        this.add_experiment('Experiment1', Experiment1, 10);
        this.remove_experiment('Experiment1');
        this.add_experiment('Experiment2', Experiment2, 10);
      }
    }
    var str = "bla";
    for(var i = 0; i < 100; i++) {
      str += "h";
      var namespace = new TestNamespace({'userid': str});
      expect(namespace.get('test')).toEqual(2);
      validate_log("Experiment2");
    }

  });
});