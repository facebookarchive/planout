/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterBoxForm.react
 * @jsx React.DOM
 */

var React = require('react');
var ReactPropTypes = React.PropTypes;

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var TesterStatusCodes = PlanOutEditorConstants.TesterStatusCodes;
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;


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
/*
  renderInputItem: function(label, prop) {
    return (
      <div className="input-group">
      <span className="input-group-addon">{label}</span>
      <input type="text" ref={prop} className="form-control"
       defaultValue={JSON.stringify(this.props[prop])}
       onChange={this._onChange}/>
     </div>
    );
  },
*/
renderInputItem: function(label, prop) {
    return (
      <div className="input-group">
      <span className="input-group-addon">{label}</span>
      <input type="text" ref={prop} className="form-control"
       defaultValue={JSON.stringify(this.props[prop])}
       onChange={this._onChange}/>
     </div>
    );
  },


  // Parses JSON-encoded form element strings and returns object
  // containing each element: inputs, overrides, assertions
  // May be subbed out for other extract
  extractItemData: function() {
    var rawBlob = {
      inputs: this.refs.inputs.getDOMNode().value.trim(),
      overrides: this.refs.overrides.getDOMNode().value.trim()
    };
    if (this.props.type === TesterBoxTypes.TEST) {
      rawBlob.assertions = this.refs.assertions.getDOMNode().value.trim();
    }

    var jsonBlob = {};
    for (var key in rawBlob) {
      if (rawBlob[key] !== "" && rawBlob[key] !== "{}") {
        try {
          jsonBlob[key] = JSON.parse(rawBlob[key]);
        } catch (e) {
          return undefined;
        }
      }
    }
    return jsonBlob;
  },

  _onChange: function() {
    var itemData = this.extractItemData();
    // should probably add more granular checks to make sure
    // input data is given. these checks may not be necessary
    // once we move to better form UI components
    if (itemData) {
      PlanOutTesterActions.updateTester(
        this.props.id,
        itemData.inputs,
        itemData.overrides,
        itemData.assertions
      );
    } else {
      // currently this results in "unknown error" when input field is missing
      PlanOutTesterActions.updateTesterWithInvalidForm(
        this.props.id, TesterStatusCodes.INVALID_FORM);
    }
  }
});

module.exports = PlanOutTesterBoxForm;
