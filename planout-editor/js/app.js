/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * @jsx React.DOM
 */

var React = require('react');

var PlanOutTesterPanel = require('./components/PlanOutTesterPanel.react');
var PlanOutScriptPanel = require('./components/PlanOutScriptPanel.react');
var PlanOutEditorButtons = require('./components/PlanOutEditorButtons.react');
var PlanOutExperimentActions = require('./actions/PlanOutExperimentActions');
var DemoData = require('./utils/DemoData');

React.render(
      <div className="container">
      <div className="page-header">
        <h1>PlanOut Experiment Editor</h1>
      </div>
      <div className="row">
        <div className="col-md-5"><PlanOutScriptPanel/></div>
        <div className="col-md-5"><PlanOutTesterPanel/></div>
      </div>
      <br/>
      <PlanOutEditorButtons/>
      <br/>
      <p><a href="http://facebook.github.io/planout/docs/planout-language.html">
        Learn more about the PlanOut language
      </a></p>
    </div>,
  document.getElementById('planouteditor')
);

PlanOutExperimentActions.loadScript(DemoData.getDemoScript());
