from flask import Flask, jsonify, render_template, request, url_for
app = Flask(__name__)
from planout.interpreter import Interpreter
import traceback
import json
import sys

def testPlanOutScript(script, inputs={}, overrides=None, assertions=None):
  payload = {}

  # make sure experiment runs with the given inputs
  i = Interpreter(script, 'demo_salt', inputs)
  if overrides:
    i.set_overrides(overrides)

  try:
    results = dict(i.get_params()) # executes experiment
  except Exception as err:
    #message = "Error running experiment: %s" % traceback.format_exc(0)
    message = "Error running experiment:\n%s" % err
    payload['errors'] = [{
      "error_code": "runtime",
      "message": message
    }]
    return payload

  payload['results'] = results

  # validate if input contains validation code
  validation_errors = []
  if assertions:
    for (key, value) in assertions.iteritems():
      if key not in results:
        validation_errors.append({
          "error_code": "assertion",
          "message": {"param": key}
        })
      else:
        if results[key] != value:
          message = {'param': key, 'expected': value, 'got': results[key]}
          validation_errors.append({
            "error_code": "assertion",
            "message": message
          })
    if validation_errors:
      payload['errors'] = validation_errors

  return payload


@app.route('/run_test')
def run_test():
  # not sure how to change everything to use POST requests
  raw_script = request.args.get('compiled_code', '')
  raw_inputs = request.args.get('inputs', '')
  raw_overrides = request.args.get('overrides', "{}")
  raw_assertions = request.args.get('assertions', "{}")
  id = request.args.get('id')

  script = json.loads(raw_script) if raw_script else {}
  try:
    inputs = json.loads(raw_inputs)
    overrides = json.loads(raw_overrides) if raw_overrides else None
    assertions = json.loads(raw_assertions) if raw_assertions else None
  except:
    return jsonify({
      'errors': [{
        'error_code': "INVALID_FORM",
        'message': 'Invalid form input'
      }],
      'id': id
    })

  t = testPlanOutScript(script, inputs, overrides, assertions)
  t['id'] = id
  return jsonify(t)

@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)
  url_for('static', filename='planoutstyle.css')
