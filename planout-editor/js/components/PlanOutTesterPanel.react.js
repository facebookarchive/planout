/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterPanel.react
 * @jsx React.DOM
 */

var React = require('react');

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');
var PlanOutTesterBox = require('./PlanOutTesterBox.react');
var PlanOutTesterStore = require('../stores/PlanOutTesterStore');

//var Bootstrap = require('react-bootstrap');
//var Accordion = Bootstrap.Accordion;


function getStateFromStores() {
  // will ventually also get data from PlanOutExperimentStore
  return {
    tests: PlanOutTesterStore.getAllTests()
  };
}

var PlanOutTesterPanel = React.createClass({

  getInitialState: function() {
    PlanOutTesterActions.init();
    var state_data = getStateFromStores();
    //state_data.expandedTest = Object.keys(state_data)[0];
    return state_data;
  },

  componentDidMount: function() {
    PlanOutTesterStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    PlanOutTesterStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    this.setState(getStateFromStores());
  },

  render: function() {
    var boxes = this.state.tests.map(function(test) {
      return (
        <PlanOutTesterBox
          url="tester"
          key={test.id}
          id={test.id}
          inputs={test.inputs}
          overrides={test.overrides}
          status={test.status}
          assertions={test.assertions}
          results={test.results}
          errors={test.errors}
          type={test.type}
        />
      );
    }, this);

    return (
      <div>
        <div className="panel-group" id="accordion">
          {boxes}
        </div>
        <button type="button" className="btn btn-default"
          id="#addTest"
          onClick={this._onAddPlanOutTesterBoxEvent}>
          Add test
        </button>
        <input
          type="hidden"
          name="serialized_tests"
          value={JSON.stringify(PlanOutTesterStore.getAllTests())}
        />
      </div>
    );
  },

  _onAddPlanOutTesterBoxEvent: function() {
    PlanOutTesterActions.create();
  },
});


module.exports = PlanOutTesterPanel;
