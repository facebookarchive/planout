/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * PlanOutTesterBoxOutput
 *
 * @jsx React.DOM
 */

var React = require('react');
var ReactPropTypes = React.PropTypes;


var PlanOutTesterBoxOutput = React.createClass({
  propTypes: {
    errors: ReactPropTypes.array,
    results: ReactPropTypes.object
  },

  render: function() {
    var renderErrorMessage = function(error_message) {
      if ('expected' in error_message) {
        // expected param value assertion always contains expected_value
        return (
          <span>
            Expecting
            <code>{error_message.param}</code> to be
            <code>{error_message.expected}</code> but got
            <code>{error_message.got}</code> instead.
          </span>
        );
      } else {
        // otherwise we are missing an expected key
        return (
          <span>
            Expecting to see a parameter named <code>{error_message.param}</code>,
            but no such parameter could be found in the output.
          </span>);
      }
    };

    var my_string = JSON.stringify(this.props.results, null, " ");
    var outputObject;
    if (this.props.errors && this.props.errors.length>0) {
      var firstError = this.props.errors[0];
      if(firstError.error_code !== "assertion") {
        outputObject = <pre className="error">{firstError.message}</pre>;
      } else {
        var n = 0;
        var rows = this.props.errors.map(function(row) {
          return (
            <tr key={"error-row-" + n++}>
              <td>{renderErrorMessage(row.message)}</td>
            </tr>
          )
        }.bind(this));
        outputObject = (
          <div>
            <table className="table table-bordered">
            <tbody>
              {rows}
            </tbody>
            </table>
            <pre className="error">{my_string}</pre>
          </div>
        );
      }
    } else {
      outputObject = <pre className="correct">{my_string}</pre>;
    }
    return (
      <div className="outputBox">
        {outputObject}
      </div>
    );
  }
});

module.exports = PlanOutTesterBoxOutput;
