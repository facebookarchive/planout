/** Copyright (c) 2014, Facebook, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

var _ = require('underscore');

var PlanOutCompiler = require('./planout_compiler');
var FileSaver = require('./FileSaver');

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');
var PlanOutExperimentActions = require('../actions/PlanOutExperimentActions');

var PlanOutEditorDispatcher = require('../dispatcher/PlanOutEditorDispatcher');
var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;

var ASYNC_DELAY = 250;


// NOTE: need to update python endpoint to return test id
function _runTest(/*string*/ id, /*object*/ updateBlob) /*bool*/  {
  var stringBlob = {};
  for (var key in updateBlob) {
    stringBlob[key] = JSON.stringify(updateBlob[key]);
  }
  $.ajax({
    url: 'run_test',
    dataType: 'json',
    data: stringBlob,
    success: function(data) {
      PlanOutTesterActions.updateTesterOutput(
        id,
        data.errors,
        data.results
      );
    }.bind(this),
    error: function(xhr, status, err) {
      console.error(this.props.url, status, err.toString());
      return false;
    }.bind(this)
  });
  return true;
}

module.exports = {

  getDemoTests: function() /*array*/  {
    // this will eventually come from the server
    var defaultTests = [
      {
        "id": "playground",
        "inputs": {"userid": 42},
        "type": TesterBoxTypes.PLAYGROUND
      },
      {
        "id": "test3",
        "inputs":{"userid":5243},
        "overrides": {},
        "assertions": {"ratings_goal":640},
        "type": TesterBoxTypes.TEST
      },
      {
        "id": "test2",
        "inputs":{"userid":52433},
        "overrides": {"group_size":10},
        "assertions": {"ratings_goal": 200},
        "type": TesterBoxTypes.TEST
      },
    ];
    return defaultTests;
    //at some point we should call something to update all tester output
  },

  getDemoScript: function() /*string*/  {
    return [
     "group_size = uniformChoice(choices=[1, 10], unit=userid);",
     "specific_goal = bernoulliTrial(p=0.8, unit=userid);",
     "if (specific_goal) {",
     "  ratings_per_user_goal = uniformChoice(",
     "    choices=[8, 16, 32, 64], unit=userid);",
     "  ratings_goal = group_size * ratings_per_user_goal;",
     "}"
    ].join('\n');
  },

  saveState: function(/*object*/ data, /*string*/ filename) {
    var blob = new Blob(
      [JSON.stringify(data, false, " ")],
      {type: "text/plain;charset=utf-8"}
    );
    FileSaver(blob, filename);
  },

  genRunner: function(/*string*/ id) /*function*/  {
    // generates a throttled function for each test id
    return _.throttle(
      function(updateBlob) {
        _runTest(id, updateBlob);
      },
      ASYNC_DELAY
    );
  },

  compilerCallback: function(/*string*/ script) {
    try {
      // this can be subbed out for a callback if using server-side compilation
      var json = PlanOutCompiler.parse(script);
      PlanOutExperimentActions.updateCompiledCode(script, "success", json);
    } catch (err) {
      PlanOutExperimentActions.updateCompiledCode(script, err.message, {});
    }
  },

  compileScript: _.throttle(function(/*string*/ script) {
    setTimeout((function() {
      this.compilerCallback(script);
    }).bind(this), 1);
  }, ASYNC_DELAY)
};
