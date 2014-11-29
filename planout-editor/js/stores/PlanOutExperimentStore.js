/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * PlanOutExperimentStore
 */

var _ = require('underscore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var PlanOutAsyncRequests = require('../utils/PlanOutAsyncRequests');
var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var PlanOutEditorDispatcher = require('../dispatcher/PlanOutEditorDispatcher');
var ActionTypes = PlanOutEditorConstants.ActionTypes;
var PlanOutStaticAnalyzer = require('../utils/PlanOutStaticAnalyzer');

var CHANGE_EVENT = 'change';

var _script = '';
var _json = {};
var _compilation_status = 'success';


var PlanOutExperimentStore = assign({}, EventEmitter.prototype, {
  getScript: function() /*string*/ {
    return _script;
  },

  getJSON: function() /*object*/ {
    return _json;
  },

  getInputVariables: function() /*array*/ {
    return PlanOutStaticAnalyzer.inputVariables(_json);
  },

  getParams: function() /*array*/ {
    return PlanOutStaticAnalyzer.params(_json);
  },

  getCompilerMessage: function() /*string*/ {
    return _compilation_status === 'success' ?
      'Compilation successful!' : _compilation_status;
  },

  doesCompile: function() /*bool*/ {
    return _compilation_status === 'success';
  },

  emitChange: function() {
    this.emit(CHANGE_EVENT);
  },

  /**
   * @param {function} callback
   */
  addChangeListener: function(/*function*/ callback) {
    this.addListener(CHANGE_EVENT, callback);
  },

  /**
   * @param {function} callback
   */
  removeChangeListener: function(/*function*/ callback) {
    this.removeListener(CHANGE_EVENT, callback);
  },

  dispatchToken: PlanOutEditorDispatcher.register(
    function(/*object*/ payload)
  {
    var action = payload.action;

    switch(action.actionType) {
      case ActionTypes.EDITOR_COMPILE_SCRIPT:
        _script = action.script;
        if (action.script.trim() === "") {
          _json = {};
          _compilation_status = 'success';
          break;
        }
        PlanOutAsyncRequests.compileScript(action.script);
        break;

      case ActionTypes.EDITOR_LOAD_SCRIPT:
        _script = action.script;
        PlanOutAsyncRequests.compileScript(action.script);
        break;

      case ActionTypes.EDITOR_UPDATE_COMPILED_CODE:
        _json = action.json;
        _compilation_status = action.status;
        break;

      default:
        // no change needed to emit
        return true;
    }

    PlanOutExperimentStore.emitChange();
    return true;
  })
});

module.exports = PlanOutExperimentStore;
