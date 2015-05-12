var express = require('express');
var app = express();

var planout = require('planout');

var Experiment1 = function(args) {
  var experiment = new planout.Experiment(args);
  experiment.setup = function() { this.set_salt("Exp1"); }
  experiment.setup();
  experiment.assign = function(params, args) {
    params.set('group_size', new planout.Ops.Random.UniformChoice({ 'choices': [1, 10], 'unit': args.userid}));
    params.set('specific_goal', new planout.Ops.Random.BernoulliTrial({'p': 0.8, 'unit': args.userid}));
    if (params.get('specific_goal')) {
      params.set('ratings_per_user_goal', new planout.Ops.Random.UniformChoice({ 'choices': [8, 16, 32, 64], 'unit': args.userid}));
      params.set('ratings_goal', params.get('group_size') * params.get('ratings_per_user_goal'));
    }
  };
  experiment.configure_logger = function() { return; }
  experiment.log = function(stuff) { return; }
  experiment.previously_logged = function() { return; }
  return experiment;
};

var Experiment3 = function(args) {
  var experiment = new planout.Experiment(args);
  experiment.setup = function() { this.set_salt("Exp3"); }
  experiment.setup();
  experiment.assign = function(params, args) {
    params.set('has_banner', new planout.Ops.Random.BernoulliTrial({ 'p': 0.97, 'unit': args.userid}));
    var cond_probs = [0.5, 0.95];
    params.set('has_feed_stories', new planout.Ops.Random.BernoulliTrial({'p': cond_probs[params.get('has_banner')], 'unit': args.userid}));
    params.set('button_text', new planout.Ops.Random.UniformChoice({'choices': ["I'm a voter", "I'm voting"], 'unit': args.userid}))
  };
  experiment.configure_logger = function() { return; }
  experiment.log = function(stuff) { return; }
  experiment.previously_logged = function() { return; }
  return experiment;

}

var experiment1_results = [];
for (var i = 0; i < 10; i++) {
  var exp = Experiment1({'userid': i});
  experiment1_results.push([exp.get('group_size'), exp.get('ratings_goal')]);
}

var experiment3_results = [];
for (var i =0 ; i < 5; i++) {
  var exp = Experiment3({'userid': i});
  experiment3_results.push([exp.get('button_text')]);
}

app.get('/', function (req, res) {
  res.send('Experiment 1 results ' + experiment1_results + '<br>Experiment 3 results ' + experiment3_results);
});


var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Listening at http://%s:%s', host, port);

});
