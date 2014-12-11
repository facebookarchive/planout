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
    defaultJSON: React.PropTypes.object,
    fieldName: React.PropTypes.string.isRequired,
    id: React.PropTypes.string.isRequired,
    label: React.PropTypes.string.isRequired
  },

  getInitialState: function() {
    // value can take on any value users types into the textarea
    // json only gets updated when this value is valid JSON
    return {
      isValidJSON: true,
      json: this.props.defaultJSON || {},
      value: JSON.stringify(this.props.defaultJSON || {}, null, ' '),
    };
  },

  _updateJSON: function(event) {
     var value = event.target.value;
     try {
      this.setState({
        isValidJSON: true,
        json: JSON.parse(value),
        value: value
      });
      var payload = {};
      payload[this.props.fieldName] = JSON.parse(value);
      PlanOutTesterActions.updateTester(
        this.props.id,
        payload
      );
    } catch (e) {
      this.setState({
        isValidJSON: false,
        json: null,
        value: value
      });
    }
  },

  getJSON: function() {
    return this.state.json;
  },

  getIsCurrentlyValidJSON: function() {
    return this.state.isValidJSON;
  },

  _onMouseLeave: function () {
    if (this.state.json) {
      this.setState({"value": JSON.stringify(this.state.json, null, " ")});
    }
  },
 
  render: function() {
    return (
      <Input type="textarea" 
       value={this.state.value}
       addonBefore={this.props.label}
       onChange={this._updateJSON}
       bsStyle={this.state.json ? "success" : "error"}
       onBlur={this._onMouseLeave}
       help={this.state.json ? null : "Invalid JSON"}/>
    );
  }
});

module.exports = PlanOutTesterBoxFormInput;
