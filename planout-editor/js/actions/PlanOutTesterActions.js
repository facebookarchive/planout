/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * PlanOutTesterActions
 */

var PlanOutEditorDispatcher = require('../dispatcher/PlanOutEditorDispatcher');

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var ActionTypes = PlanOutEditorConstants.ActionTypes;


var PlanOutTesterActions = {
  init: function() {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.INIT_TESTER_PANEL
    });
  },

  create: function() {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_CREATE
    });
  },

  /**
   * @param  {objects} tests to initialize PlanOutTesterPanel
   */
  loadTests: function(/*object*/ tests) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.LOAD_SERIALIZED_TESTERS,
      tests: tests
    });
  },

  /**
   * Re-runs all tests
   */
  refreshAllTests: function() {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_REFRESH_ALL_TESTS
    });
  },

  /**
   * @param  {string} id The ID of the tester item
   * @param  {string} inputs Unvalidated JSON blob representing input units
   * @param  {string} overrides Unvalidated JSON blob representing overrides
   * @param  {string} assertions Unvalidated JSON blob representing assertions
   */
  updateTester: function(
      /*string*/ id,
      /*string*/ inputs,
      /*string*/ overrides,
      /*string*/ assertions)
  {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_USER_UPDATE_TEST,
      id: id,
      inputs: inputs,
      overrides: overrides,
      assertions: assertions
    });
  },

  // Eventually this might be handled by a UI component that has users enter the
  // data as structured data using some nice form, so we won't need to handle
  // this exception.
  // This is separate from updateTesterOutput because we don't want to keep the
  // output and errors fixed while the user is editing the JSON field
  updateTesterWithInvalidForm: function(/*string*/ id, /*string*/ status) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_INVALID_TEST_FORM,
      id: id,
      status: status
    });
  },

  updateTesterOutput: function(/*string*/ id, /*array*/ errors, /*object*/ results) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_SERVER_UPDATE_TEST,
      id: id,
      errors: errors,
      results: results
    });
  },

  /**
   * @param  {string} id
   */
  destroy: function(/*string*/ id) {
    PlanOutEditorDispatcher.handleViewAction({
      actionType: ActionTypes.TESTER_DESTROY,
      id: id
    });
  }
};

module.exports = PlanOutTesterActions;
