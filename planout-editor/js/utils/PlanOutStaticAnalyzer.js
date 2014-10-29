/**
 * Copyright 2004-present Facebook. All Rights Reserved.
 *
 * @providesModule PlanOutStaticAnalyzer
 * @typechecks
 */

var _ = require('underscore');

// code may be an object or array
var _getVariables = function(code) /*object*/ {
  if (!code || Object.keys(code).length === 0) {
    return {'get_vars': [], 'set_vars': []};
  }
  var get_vars = {};
  var set_vars = {};
  var child_vars = {};

  var op = code.op;
  if (op === 'set') {
    set_vars[code['var']] = code.value;
  } else if (op === 'get')  {
    get_vars[code['var']] = code.value;
  }
  for (var key in code) {
    if (typeof code[key] === 'object') {
      child_vars = _getVariables(code[key]);
      if (child_vars.get_vars) {
        for (var ck in child_vars.get_vars) {
          get_vars[ck] = child_vars.get_vars[ck];
        }
      }
      if (child_vars.set_vars) {
        for (var ck in child_vars.set_vars) {
          set_vars[ck] = child_vars.set_vars[ck];
        }
      }
    }
  }

  return {'get_vars': get_vars, 'set_vars': set_vars};
};

function _getParams(/*object*/ code) /*array*/ {
  var vars = _getVariables(code);
  return Object.keys(vars.set_vars);
}

function _getParamValue(/*object*/ code, /*string*/ var_name) {
  return _getVariables(code).set_vars[var_name];
}

var PlanOutStaticAnalyzer = {
  inputVariables: function(/*object*/ code) /*array*/ {
    var vars = _getVariables(code);
    var input_vars = [];
    for (var v in vars.get_vars) {
      if (!(v in vars.set_vars)) {
        input_vars.push(v);
      }
    }
    return input_vars;
  },

  params: _getParams,

  getLoggedParams: function(/*object*/ code) /*array<string>*/ {
    var loggedParams = _getParamValue(code, 'log');
    // interpret array operators as literal arrays
    if (loggedParams instanceof Object && loggedParams.op == 'array') {
      loggedParams = loggedParams.values;
    }
    if (loggedParams) {
      if (loggedParams instanceof Array) {
        return _.intersection(
          _getParams(code),
          loggedParams.filter(function(x) {return typeof x === 'string';})
        );
      } else {
        console.log(
          'Error: PlanOut variable named log must be an array of strings, ' +
          'but got ', loggedParams, ' instead.'
        );
        return [];
      }
    } else {
      return _getParams(code);
    }
  }
};

module.exports = PlanOutStaticAnalyzer;
