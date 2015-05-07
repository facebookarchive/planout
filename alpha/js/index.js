module.exports = function() {
  Experiment: require('./es6/experiment')
  Interpeter: require('./es6/interpreter')
  Ops: {
    Random: require('./es6/ops/random')
    Core: require('./es6/ops/core')
  }
};
