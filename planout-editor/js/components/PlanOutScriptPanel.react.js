/**
 * Copyright 2014 Facebook, Inc.
 *
 * @providesModule PlanOutScriptPanel.react
 * @jsx React.DOM
 */

var React = require('react');

var PlanOutExperimentActions = require('../actions/PlanOutExperimentActions');
var PlanOutExperimentStore = require('../stores/PlanOutExperimentStore');


function getStateFromStores() {
  return {
    compilerMessage: PlanOutExperimentStore.getCompilerMessage(),
    doesCompile: PlanOutExperimentStore.doesCompile(),
    inputVariables: PlanOutExperimentStore.getInputVariables(),
    json: PlanOutExperimentStore.getJSON(),
    params: PlanOutExperimentStore.getParams(),
    script: PlanOutExperimentStore.getScript()
  };
}

var PlanOutScriptPanel = React.createClass({

  getInitialState: function() /*object*/ {
    var state_data = getStateFromStores();
    state_data.showCompiledBlock = false;
    return state_data;
  },

  componentDidMount: function() {
    PlanOutExperimentStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    PlanOutExperimentStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    this.setState(getStateFromStores());
  },


  render: function() {
    return (
      <div>
        {this.renderCodeBlock()}
        <div className="disabled">
          <a href="#" onClick={this._toggleShowCompiled}>
            {this.state.showCompiledBlock ? 'Hide' : 'Show'} serialized code
          </a>
        </div>
        {this.renderScriptStatus()}
        <input type="hidden" name="qe_planout_compiled"
          value={JSON.stringify(this.state.json, false, " ")}/>
      </div>
    );
  },

  renderCodeBlock: function() {
    if (this.state.showCompiledBlock) {
      return this.renderCompiledBlock();
    } else {
      return this.renderScriptInputBlock();
    }
  },

  renderScriptStatus: function() {
    return (
      <dl className="dl">
        <dt className="fields">Compilation status</dt>
        <dd>{this.renderCompileStatus()}</dd>
        <dt className="fields">Input units</dt>
        <dd>{this.state.inputVariables.join(', ')}</dd>
        <dt className="fields">Parameters</dt>
        <dd>{this.state.params.join(', ')}</dd>
      </dl>
    );
  },

  /**
   * This could be swapped out with various open-source components.
   */
  renderScriptInputBlock: function() {
    return (
      <textarea
        id="qe_planout_source" ref="qe_planout_source"
        name="qe_planout_source"
        spellCheck="false"
        value={this.state.script}
        onChange={this._onCodeChange}
      />
    );
  },

  renderCompileStatus: function() {
    return (
      <pre className={this.state.doesCompile ? "correct" : "error"}>
        {this.state.compilerMessage}
      </pre>
    );
  },

  renderCompiledBlock: function() {
    if (!this.state.showCompiledBlock) {
      return null;
    }
    return (
      <div ref="compiledBlock">
        <textarea lang="json"
          value={JSON.stringify(this.state.json, false, " ")}
          readOnly={true}
        />
      </div>
    );
  },

  /**
   *  Toggles whether compiled JSON code gets shown.
   */
  _toggleShowCompiled: function(event) {
    this.setState({showCompiledBlock: !this.state.showCompiledBlock});
    return false;
  },

  _onCodeChange: function() {
    var script = this.refs.qe_planout_source.getDOMNode().value;
    PlanOutExperimentActions.compile(script);
  }
});

module.exports = PlanOutScriptPanel;
