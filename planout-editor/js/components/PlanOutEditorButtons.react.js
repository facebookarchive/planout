/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * @providesModule PlanOutEditorButtons.react
 * @jsx React.DOM
 */

var _ = require('underscore');
var React = require('react/addons');
var ReactPropTypes = React.PropTypes;
var cx = React.addons.classSet;

var PlanOutAsyncRequests = require('../utils/PlanOutAsyncRequests');
var PlanOutExperimentActions = require('../actions/PlanOutExperimentActions');
var PlanOutExperimentStore = require('../stores/PlanOutExperimentStore');
var PlanOutTesterActions = require('../actions/PlanOutTesterActions');
var PlanOutTesterStore = require('../stores/PlanOutTesterStore');

var DemoData = require('../utils/DemoData');


function getStateFromStores() /*object*/ {
  return {
    doesCompile: PlanOutExperimentStore.doesCompile(),
    json: PlanOutExperimentStore.getJSON(),
    passesTests: PlanOutTesterStore.areAllPassing(),
    script: PlanOutExperimentStore.getScript(),
    tests: PlanOutTesterStore.getAllTests()
  };
}

var PlanOutEditorButtons = React.createClass({
  getInitialState: function() /*object*/ {
    return getStateFromStores();
  },

  componentDidMount: function() {
    PlanOutTesterStore.addChangeListener(this._onChange);
    PlanOutExperimentStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    PlanOutTesterStore.removeChangeListener(this._onChange);
    PlanOutExperimentStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    this.setState(getStateFromStores());
  },

  render: function() {
    var cx = React.addons.classSet;
    var buttonClass = cx({
      'btn': true,
      'btn-default': true,
      'disabled': !(this.state.doesCompile && this.state.passesTests)
    });
    return (
      <div>
        <button type="button" className='btn btn-default'
         onClick={this._loadSampleData}
        >
          Load sample experiment
        </button>
        &nbsp;&nbsp;
        <button type="button" className={buttonClass}
          onClick={this._saveAll}>
          Save all
        </button>
        &nbsp;&nbsp;
        <button type="button" className={buttonClass}
         onClick={this._saveJSON}>
          Save JSON
        </button>
      </div>
    );
  },

  _loadSampleData: function() {
    PlanOutExperimentActions.loadScript(DemoData.getDemoScript());
    PlanOutTesterActions.loadTests(DemoData.getDemoTests());
    PlanOutTesterActions.refreshAllTests();
  },

  _saveJSON: function() {
    PlanOutAsyncRequests.saveState(this.state.json, "experiment_code.json");
  },

  _saveAll: function() {
    var all = {
      script: this.state.script,
      json: this.state.json,
      tests: PlanOutTesterStore.getSerializedTests()
    };
    PlanOutAsyncRequests.saveState(all, "experiment_all.json");
  },
});

module.exports = PlanOutEditorButtons;
