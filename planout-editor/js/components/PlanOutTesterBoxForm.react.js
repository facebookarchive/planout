/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterBoxForm.react
 * @jsx React.DOM
 */

var React = require('react');
var ReactPropTypes = React.PropTypes;
var Input = require('react-bootstrap/Input');

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var TesterStatusCodes = PlanOutEditorConstants.TesterStatusCodes;
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;

var PlanOutTesterBoxFormInput = require('./PlanOutTesterBoxFormInput.react');


var PlanOutTesterBoxForm = React.createClass({
  propTypes: {
   id: ReactPropTypes.string.isRequired,
   assertions: ReactPropTypes.object,
   inputs: ReactPropTypes.object,
   overrides: ReactPropTypes.object,
   type: ReactPropTypes.string.isRequired
  },

  render: function() {
    return (
      <div>
        <div className="input-group">
          {this.renderInputItem("Inputs", "inputs")}
          {this.renderInputItem("Overrides", "overrides")}
          {
            this.props.type === TesterBoxTypes.TEST ?
            this.renderInputItem("Assertions", "assertions") : null
          }
        </div>
      </div>
    );
  },

  renderInputItem: function(label, prop) {
    return (
      <PlanOutTesterBoxFormInput
        json={this.props[prop]}
        label={label}
        id={this.props.id}
        ref={prop}
        fieldName={prop}/>
    );
  },


  // Parses JSON-encoded form element strings and returns object
  // containing each element: inputs, overrides, assertions
  // May be subbed out for other extract
  extractItemData: function() {
    var jsonBlob = {
      inputs: this.refs.inputs.getJSON(),
      overrides: this.refs.overrides.getJSON()
    };
    if (this.props.type === TesterBoxTypes.TEST) {
      jsonBlob.assertions = this.refs.assertions.getJSON();
    }

    for (var key in jsonBlob) {
      if (jsonBlob[key] === null) {
        return null;
      }
    }
    return jsonBlob;
  },

  _updateJSON: function(event, ref) {
    this.refs[ref].updateJSON(event.target.value);
  },

  _onChange: function(event, ref) {
               /*
    var payload = {};
    payload[ref] = this.refs[ref].getJSON();
    if (payload[ref]) {
       PlanOutTesterActions.updateTester(
         this.props.id,
         payload
       );
    }
    */


    var itemData = this.extractItemData();
    // should probably add more granular checks to make sure
    // input data is given. these checks may not be necessary
    // once we move to better form UI components
    if (itemData) {
      PlanOutTesterActions.updateTester(
        this.props.id,
        {
          inputs: itemData.inputs,
          overrides: itemData.overrides,
          assertions: itemData.assertions
        }
      );
    }
  }
});

module.exports = PlanOutTesterBoxForm;
