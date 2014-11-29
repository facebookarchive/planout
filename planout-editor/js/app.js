/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * @jsx React.DOM
 */

var React = require('react');

var PlanOutTesterPanel = require('./components/PlanOutTesterPanel.react');
var PlanOutScriptPanel = require('./components/PlanOutScriptPanel.react');
var PlanOutEditorButtons = require('./components/PlanOutEditorButtons.react');

React.render(
      <div className="container">
      <div className="page-header">
        <h1>PlanOut Editor</h1>
      </div>
      <div className="row">
        <div className="col-md-5"><PlanOutScriptPanel/></div>
        <div className="col-md-5"><PlanOutTesterPanel/></div>
      </div>
      <br/>
      <PlanOutEditorButtons/>
      <br/>
      <p><a href="https://facebook.github.io/planout/docs/interpreter.html">
        Learn more about the PlanOut language
      </a></p>
    </div>,
  document.getElementById('planouteditor')
);
