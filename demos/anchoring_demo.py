import random
from uuid import uuid4
from flask import (
  Flask, 
  session,
  request, 
  redirect,
  url_for, 
  render_template_string
)
app = Flask(__name__)

app.config.update(dict(
  DEBUG=True,
  SECRET_KEY='3.14159', # shhhhh
))

from planout.experiment import SimpleExperiment
from planout.ops.random import *

class AnchoringExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.use_round_number = BernoulliTrial(p=0.5, unit=userid)
    if params.use_round_number:
      params.price = UniformChoice(choices=[100000, 110000, 120000],
        unit=userid)
    else:
      params.price = RandomInteger(min=100000, max=120000, unit=userid)
    print params

@app.route('/')
def main():
    # if no userid is defined make one up
    if 'userid' not in session:
        session['userid'] = str(uuid4())

    anchoring_exp = AnchoringExperiment(userid=session['userid'])
    price = anchoring_exp.get('price')
    
    # need to add a text box and button to submit a bid.
    return render_template_string("""
    <html>
      <head>
        <title>Let's buy a house!</title>
      </head>
      <body>
        <p>
        A lovely new home is going on the market for ${{ price }}. <br>
        What will be your first offer?
        </p>
      <form method="POST" action="/reset">
      <input type="submit" value="Reset my ID">
      </body>
    </html>
    """, price=price)

@app.route('/reset', methods=['POST'])
def reset():
  session.clear()
  return redirect(url_for('main'))

@app.route('/bid', methods=['POST'])
def bid():
  anchoring_exp = AnchoringExperiment(userid=session['userid'])
  anchoring_exp.log_conversion('whatevertheysubmitted')
  # do something
  return ""


if __name__ == '__main__':
    app.run()
