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
        <div className="input-group" onChange={this._onChange} onMouseMove={this._onChange}>
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
        defaultJSON={this.props[prop]}
        label={label}
        ref={prop} />
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
    } else {
      // currently this results in "unknown error" when input field is missing
      PlanOutTesterActions.updateTesterWithInvalidForm(
        this.props.id, TesterStatusCodes.INVALID_FORM);
    }
  }
});

module.exports = PlanOutTesterBoxForm;
