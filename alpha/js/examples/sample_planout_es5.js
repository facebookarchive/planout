var express = require('express');
var app = express();
var planout = require('planout');

var DummyExperiment = function(args) {
  var experiment = new planout.Experiment(args);
  experiment.setup = function() { this.name = "SampleExperiment"; }
  experiment.setup();
  experiment.assign = function(params, args) {
    params.set('foo', new planout.Ops.Random.UniformChoice({ 'choices': ['Variation A', 'Variation B'], 'unit': args.id }));
  };
  experiment.configure_logger = function() { return; }
  experiment.log = function(stuff) { return; }
  experiment.previously_logged = function() { return; }
  return experiment;
};


app.get('/', function (req, res) {
  var experiment = DummyExperiment({'id': req.connection.remoteAddress})
  res.send('<html><body>' + experiment.get('foo') + '</body></html>');
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Listening at http://%s:%s', host, port);

});
