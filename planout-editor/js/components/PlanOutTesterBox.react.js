/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutTesterBox.react
 * @jsx React.DOM
 */

var React = require('react');
var ReactPropTypes = React.PropTypes;

var PlanOutTesterActions = require('../actions/PlanOutTesterActions');
var PlanOutTesterBoxForm = require('./PlanOutTesterBoxForm.react');
var PlanOutTesterBoxOutput = require('./PlanOutTesterBoxOutput.react');

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;
var TesterStatusCodes = PlanOutEditorConstants.TesterStatusCodes;

//var Bootstrap = require('react-bootstrap');
//var Panel = Bootstrap.Panel;


var PlanOutTesterBox = React.createClass({
  propTypes: {
    id: ReactPropTypes.string.isRequired,
    assertions: ReactPropTypes.object,
    errors: ReactPropTypes.array,
    inputs: ReactPropTypes.object,
    overrides: ReactPropTypes.object,
    results: ReactPropTypes.object,
    status: ReactPropTypes.string.isRequired,
    type: ReactPropTypes.string.isRequired
  },

  getInitialState: function() {
    return {expanded: this.props.type === TesterBoxTypes.PLAYGROUND};
  },

  _toggleExpand: function() {
    this.setState({expanded: !this.state.expanded});
  },

  _destroy: function() {
    PlanOutTesterActions.destroy(this.props.id);
  },

  render: function() {
    var titleBarSettings = this.getTitleBarStrings();

    var collapse_class = "panel-collapse collapse";
    collapse_class += this.state.expanded ? " in" : "";

    return (
      <div>
      <div className={"panel " + titleBarSettings.panel_style}>
      <div className="panel-heading">
        <h4 className="panel-title">
          <a href={'#'+this.props.id} onClick={this._toggleExpand}>
           {titleBarSettings.title}
          </a>
          &nbsp;
          {this.renderDestroy()}
        </h4>
      </div>
      <div id={this.props.id} className={collapse_class}>
        <div className="panel-body">
          {this.renderPlanOutTesterBox()}
        </div>
      </div>
      </div>
      </div>
    );
    /*
      When react-bootstrap becomes more stable, the above will be replaced with

      return (
        <Panel
          header={titleBarSettings.title}
          bsStyle={titleBarSettings.panel_style}
          collapsable={true}
          expanded={this.state.expanded}
          onSelect={this._toggleExpand}>
          {this.renderPlanOutTesterBox()}
        </Panel>
      );
    */
  },

  renderPlanOutTesterBox: function() {
    return (
      <div>
        <PlanOutTesterBoxForm
         id={this.props.id}
         inputs={this.props.inputs}
         overrides={this.props.overrides}
         assertions={this.props.assertions}
         type={this.props.type}
        />
        <PlanOutTesterBoxOutput
         errors={this.props.errors}
         results={this.props.results}
        />
      </div>
    );
  },

  renderDestroy: function() {
    // playground cannot be nuked
    if (this.props.type !== TesterBoxTypes.PLAYGROUND) {
      return <a href="#" title="Delete test" onClick={this._destroy}>[x]</a>;
    } else {
      return;
    }
  },

  // generate strings for accordian panel title
  getTitleBarStrings: function() {
    var title;
    switch(this.props.status) {
      case TesterStatusCodes.INVALID_FORM:
        return {
          panel_style: "panel-warning",
          title: "Invalid JSON input"
        };
      case TesterStatusCodes.PENDING:
        return {
          panel_style: "panel-warning",
          title: "Pending results..."
        }
      case TesterStatusCodes.FAILURE:
        if (this.props.errors[0].error_code === 'runtime') {
          title = "Runtime error";
        } else if (this.props.errors[0].error_code === 'assertion') {
          title = "Failed assertion";
        } else {
          title = "Unknown other error";
          console.log("Unknown errors:", this.props.errors);
        }
        return {
          panel_style: "panel-danger",
          title: "Test status: " + title
        };
      case TesterStatusCodes.SUCCESS:
        if (this.props.type === TesterBoxTypes.TEST) {
          return {
            panel_style: "panel-success",
            title: "Test status: Success"};
        } else {
          return {
            panel_style: "panel-default",
            title: "Playground"
          };
        }
      default:
        console.log("Unknown status code:", this.props.status);
    }
  }
});


module.exports = PlanOutTesterBox;
