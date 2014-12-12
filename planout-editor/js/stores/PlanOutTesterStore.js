/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * PlanOutTesterStore
 * @jsx
 */

var _ = require('underscore');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var PlanOutAsyncRequests = require('../utils/PlanOutAsyncRequests');
var PlanOutEditorDispatcher = require('../dispatcher/PlanOutEditorDispatcher');
var PlanOutExperimentStore = require('../stores/PlanOutExperimentStore');

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var ActionTypes = PlanOutEditorConstants.ActionTypes;
var TesterStatusCodes = PlanOutEditorConstants.TesterStatusCodes;
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;


var CHANGE_EVENT = 'change';
var DEFAULT_INPUTS = {'userid': 4}; // default when units cannot be inferred


var _tests = {};      // indexed set of tests
var _test_ids = [];   // ids giving the order of tests


function _createTestBox(testType) {
  PlanOutEditorDispatcher.waitFor([PlanOutExperimentStore.dispatchToken]);
  if (PlanOutExperimentStore.doesCompile()) {

    // generate input blob with reasonable random defaults based on which
    // variables are used but not set by the PlanOut script
    var inferred_input_variables = PlanOutExperimentStore.getInputVariables();

    var input_dict = {};
    /*
    if (inferred_input_variables.length > 0) {
      for(var i = 0; i < inferred_input_variables.length; i++) {
        input_dict[inferred_input_variables[i]] =
          Math.floor((Math.random() * 1000));
      }
    } else {
      input_dict = _.clone(DEFAULT_INPUTS);
    }
    */

    // note that action.assertions may be undefined when you have a playground
    var id = 'test-' + Date.now();
    _tests[id] = {
      id: id,
      inputs: input_dict,
      overrides: undefined,
      assertions: {},
      status: TesterStatusCodes.PENDING,
      errors: undefined,
      results: undefined,
      type: testType,
      run: PlanOutAsyncRequests.genRunner(id)
    };
    _test_ids.push(id);
    _refreshTest(id);
  }
}

function _createPlayground() {
  _createTestBox(TesterBoxTypes.PLAYGROUND);
}

function _createTest() {
  _createTestBox(TesterBoxTypes.TEST);
}

/**
 * Update a TESTER item.
 * @param  {string} id
 * @param {object} updates An object literal containing only the data to be
 *     updated.
 */
function _update(/*string*/ id, /*object*/ updates) {
  _tests[id] = assign({}, _tests[id], updates);
}

/**
 * Delete a TEST item.
 * @param  {string} id
 */
function _destroy(/*string*/ id) {
  _test_ids = _test_ids.filter(function(x) {return x !== id;});
  delete _tests[id];
}

function _getScrubbedInputs(/*string*/ id) {
  var input_variables = PlanOutExperimentStore.getInputVariables();
  var inputs = _tests[id].inputs || {};
  for (var key in inputs) {
    if (inputs[key] === null) {
      delete inputs[key];
    }
  }
  input_variables.forEach(function(key) {
    if (!inputs.hasOwnProperty(key)) {
      inputs[key] = null;
    }
  });
  return inputs;
}

function _refreshTest(/*string*/ id) {
  if (PlanOutExperimentStore.doesCompile()) {
    var request = assign({},
      _tests[id],
      {compiled_code: PlanOutExperimentStore.getJSON()}
    );
    _tests[id].inputs = _getScrubbedInputs(id);
    _tests[id].run(request);
  }
}

function _refreshAllTests() {
  for (var id in _tests) {
    _refreshTest(id);
  }
}

function _getTestArray() /*array*/ {
    return _test_ids.map(function(id) {return _tests[id];});
}

var PlanOutTesterStore = assign({}, EventEmitter.prototype, {

  getAllTests: function() /*array*/ {
    return _getTestArray();
  },

  getSerializedTests: function() /*array*/ {
    return _getTestArray().map(
      function(x) {
        return _.pick(x, ['id', 'inputs', 'overrides', 'assertions', 'type']);
      }
    );
  },

  /**
   * Tests whether all the remaining TESTER items are marked as completed.
   * @return {booleam}
   */
  areAllPassing: function() /*bool*/ {
    for (var id in _tests) {
      if (_tests[id].status !== TesterStatusCodes.SUCCESS) {
        return false;
      }
    }
    return true;
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
  }
});

// Register to handle all updates
PlanOutTesterStore.dispatchToken =
  PlanOutEditorDispatcher.register(function(/*object*/ payload) {
  var action = payload.action;

  switch(action.actionType) {
    case ActionTypes.INIT_TESTER_PANEL:
      _createPlayground();
      break;

    case ActionTypes.TESTER_CREATE:
      _createTest();
      break;

    /**
     * Add multiple existing tests into TestStore.
     * @param {test} object containing tester data
     */
    case ActionTypes.LOAD_SERIALIZED_TESTERS:
      _tests = {};
      _test_ids = [];
      for (var i = 0; i < action.tests.length; i++)  {
        var test = action.tests[i];
        var id = test.id;
        _tests[id] = {
          id: test.id,
          inputs: test.inputs,
          overrides: test.overrides,
          assertions: test.assertions,
          status: TesterStatusCodes.PENDING,
          type: test.type,
          run: PlanOutAsyncRequests.genRunner(id)
        };
        _test_ids.push(id);
      }
      break;

    case ActionTypes.TESTER_USER_UPDATE_TEST:
      _update(action.id, action.fieldsToUpdate);
      PlanOutEditorDispatcher.waitFor([PlanOutExperimentStore.dispatchToken]);
      _refreshTest(action.id);
      break;

    // callback from server
    case ActionTypes.TESTER_SERVER_UPDATE_TEST:
      _update(action.id, {
        status: (action.errors && action.errors.length > 0) ?
                  TesterStatusCodes.FAILURE : TesterStatusCodes.SUCCESS,
        errors: action.errors,
        results: action.results
      });
      break;

    // User enters invalid input into form. Might be deprecated with better UI
    // components
    case ActionTypes.TESTER_INVALID_TEST_FORM:
      _update(action.id, {
        status: action.status
      });
      break;

    case ActionTypes.TESTER_DESTROY:
      _destroy(action.id);
      break;

    case ActionTypes.EDITOR_UPDATE_COMPILED_CODE:
    case ActionTypes.TESTER_REFRESH_ALL_TESTS:
      PlanOutEditorDispatcher.waitFor([PlanOutExperimentStore.dispatchToken]);
      _refreshAllTests();
      break;

    default:
      // no change needed to emit
      return true;
  }

  PlanOutTesterStore.emitChange();
  return true; // No errors.  Needed by promise in Dispatcher.
});


module.exports = PlanOutTesterStore;
