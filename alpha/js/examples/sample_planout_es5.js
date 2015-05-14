var express = require('express');
var app = express();
var planout = require('planout');


/* This is basically a way to easily extend classes in ES5 - source: https://gist.github.com/juandopazo/1367191 */
Object.getOwnPropertyDescriptors = function getOwnPropertyDescriptors(obj) {
    var descriptors = {};
    for (var prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            descriptors[prop] = Object.getOwnPropertyDescriptor(obj, prop);
        }
    }
    return descriptors;
};
 
Function.prototype.extend = function extend(proto) {
    var superclass = this;
    var constructor;
 
    if (!proto.hasOwnProperty('constructor')) {
        Object.defineProperty(proto, 'constructor', {
            value: function () {
                // Default call to superclass as in maxmin classes
                superclass.apply(this, arguments);
            },
            writable: true,
            configurable: true,
            enumerable: false
        });
    }
    constructor = proto.constructor;
    
    constructor.prototype = Object.create(this.prototype, Object.getOwnPropertyDescriptors(proto));
    
    return constructor;
};

/* End extend helper */

var DummyExperiment = planout.Experiment.extend({
  setup: function() {
    this.name = "SampleExperiment";
  },
  assign: function(params, args) {
    params.set('foo', new planout.Ops.Random.UniformChoice({ 'choices': ['Variation A', 'Variation B'], 'unit': args.id }));
  },
  configure_logger: function() {
    return;
  },
  log: function(stuff) {
    return;
  },
  previously_logged: function() {
    return;
  }
});


app.get('/', function (req, res) {
  var experiment = new DummyExperiment({'id': req.connection.remoteAddress})
  res.send('<html><body>' + experiment.get('foo') + '</body></html>');
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Listening at http://%s:%s', host, port);

});
