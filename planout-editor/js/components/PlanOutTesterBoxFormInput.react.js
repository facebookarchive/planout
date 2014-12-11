/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterBoxFormInput.react
 * @jsx React.DOM
 */


var React = require('react');
var ReactPropTypes = React.PropTypes;
var Input = require('react-bootstrap/Input');

var PlanOutTesterBoxFormInput = React.createClass({
  propTypes: {
    defaultJSON: React.PropTypes.object,
    id: React.PropTypes.string
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

 
  render: function() {
    return (
      <Input type="textarea" 
       value={this.state.value}
       addonBefore={this.props.label}
       onChange={this._updateJSON}
       bsStyle={this.state.json ? "success" : "error"}
       help={this.state.json ? null : "Invalid JSON"}/>

    );
  }
});

module.exports = PlanOutTesterBoxFormInput;
