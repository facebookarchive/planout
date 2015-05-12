var experiment = require('./es6/experiment');
var interpreter = require('./es6/interpreter');
var random = require('./es6/ops/random');
var core = require('./es6/ops/core');

module.exports =
  {
    Experiment: experiment,
    Interpreter: interpreter,
    Ops: {
      Random: random,
      Core: core
    }
  }
