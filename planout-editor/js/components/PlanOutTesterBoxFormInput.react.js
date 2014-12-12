/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterBoxFormInput.react
 * @jsx React.DOM
 */


var React = require('react');
var ReactPropTypes = React.PropTypes;
var Input = require('react-bootstrap/Input');

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');

var PlanOutTesterBoxFormInput = React.createClass({
  propTypes: {
    json: React.PropTypes.object,
    fieldName: React.PropTypes.string.isRequired,
    id: React.PropTypes.string.isRequired,
    label: React.PropTypes.string.isRequired
  },

  getInitialState: function() {
    // value can take on any value users types into the textarea
    // json only gets updated when this value is valid JSON
    return {
      isValid: true,
      inFocusValue: JSON.stringify(this.props.json || {}, null, ' '),
      inFocus: false
    };
  },

  _onChange: function(event) {
    var value = event.target.value;
    try {
      var payload = {};
      payload[this.props.fieldName] = JSON.parse(value);
      this.setState({isValid: true, inFocusValue: value});
      PlanOutTesterActions.updateTester(
         this.props.id,
         payload
      );
    } catch (e) {
      this.setState({isValid: false, inFocusValue: value});
    }
  },

  getDisplayedValue: function() {
    if (this.state.inFocus) {
      return this.state.inFocusValue;
    }
    if (!this.state.isValid) {
      return this.state.inFocusValue;
    }
    return JSON.stringify(this.props.json, null, " ");
  },

  _onBlur: function () {
    var payload = {inFocus: false};
    if (this.state.isValid) {
      payload.inFocusValue = JSON.stringify(this.props.json, null, " ");
    }
    this.setState(payload);
  },

  _onFocus: function () {
    var payload = {inFocus: true};
    if (this.state.isValid) {
      payload.inFocusValue = JSON.stringify(this.props.json, null, " ");
    }
    this.setState(payload);
  },

  jsonHeight: function() {
    return 20 + 20 * ((this.getDisplayedValue() || '').split('\n').length);
  },

  render: function() {
    return (
      <Input type="textarea"
       value={this.getDisplayedValue()}
       addonBefore={this.props.label}
       onChange={this._onChange}
       bsStyle={this.state.isValid ? "success" : "error"}
       onBlur={this._onBlur}
       onFocus={this._onFocus}
       help={this.state.isValid ? null : "Invalid JSON"}
       style={{height: this.jsonHeight()}}/>
    );
  }
});

module.exports = PlanOutTesterBoxFormInput;
