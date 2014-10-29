/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * PlanOutExperimentActions
 */

var PlanOutEditorDispatcher = require('../dispatcher/PlanOutEditorDispatcher');
var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var ActionTypes = PlanOutEditorConstants.ActionTypes;


var PlanOutExperimentActions = {
  loadScript: function(/*string*/ script) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.EDITOR_LOAD_SCRIPT,
      script: script
    });
  },

  compile: function(/*string*/ script) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.EDITOR_COMPILE_SCRIPT,
      script: script
    });
  },

  updateCompiledCode: function(/*string*/ script, /*string*/ status, /*object*/ json) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.EDITOR_UPDATE_COMPILED_CODE,
      script: script,
      status: status,
      json: json
    });
  }
};

module.exports = PlanOutExperimentActions;
