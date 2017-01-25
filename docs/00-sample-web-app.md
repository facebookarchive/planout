---
id: sample-web-app
title: Sample Web app using PlanOut
layout: docs
permalink: /docs/sample-web-app.html
prev: getting-started.html
next: about-planout.html
---

This tutorial will show you how to make a Python-based PlanOut experiment
using [Flask](http://flask.pocoo.org), a simple framework for building websites.
We assume that you have Python, PlanOut, and Flask already installed.

We will explain the very basics of Flask to give you a sense of how PlanOut fits
in with standard Web frameworks, and note that the process of integrating PlanOut
with other frameworks such as Django are quite similar.


Our sample experiment is inspired by a [series of behavioral economics
experiments](http://warrington.ufl.edu/departments/mkt/docs/janiszewski/Anchor.pdf)
by Chris Janiszewksi and Day Uy on how the precision of an [anchor](http://en.wikipedia.org/wiki/Anchoring)
can affect adjustment.
In this experiment, subjects are given either a round number or a precise
number for the price of a house, and then they are asked to give a bid price.

The full code is available in [`anchoring_demo.py`](https://github.com/facebook/planout/blob/master/demos/anchoring_demo.py)
in the [`demos/`](https://github.com/facebook/planout/blob/master/demos)
directory of the github repository. It can be run by typing `python anchoring_demo.py`.

## Try it
Don't yet have PlanOut running? Try the [experiment on Heroku](http://planoutdemo.herokuapp.com).

## Defining the experiment
Here is our experiment.

```python
class AnchoringExperiment(SimpleExperiment):
  def setup(self):
    self.set_log_file('anchoring_webapp.log')

  def assign(self, params, userid):
    params.use_round_number = BernoulliTrial(p=0.5, unit=userid)
    if params.use_round_number:
      params.price = UniformChoice(choices=[240000, 250000, 260000],
        unit=userid)
    else:
      params.price = RandomInteger(min=240000, max=260000, unit=userid)
```

The first method we define is the `setup()` method. This method gets called
before any assignment occurs and is used to configure the experiment. One of
the main uses for this method is to set up extra features of the experiment,
like where you'd like to record your log data or what you would like to name your
experiment when you call the logging functions.

We use `setup()` to call `set_log_file()`, a method that comes with
`SimpleExperiment` that tells the logger where to put your data. Here,
we tell PlanOut to log the data into a file named 'anchoring_webapp.log', located
in the same directory as where the demo script was run from.
If we didn't set the file name manually, the name of the
experiment would be used instead.

The assignment procedure works as follows:
first, users are assigned to either a round-numbered price, or a precise-numbered
price, with equal probability (p = 0.5). If the user is in the round
number condition, they are randomly assigned to see $240k, $250k, or $260k,
with equal probability, as the starting price. If the user is in the precise
number condition, the price is instead a random integer chosen between
$240k and $260k.


## Defining the main page handler
We tell Flask that all traffic to the path '/' (as in
`http://localhost:5000/` when debugging locally) to render the main page:

{% raw %}
```python
@app.route('/')
def main():
    # if no userid is defined make one up
    if 'userid' not in session:
        session['userid'] = str(uuid4())

    anchoring_exp = AnchoringExperiment(userid=session['userid'])
    price = anchoring_exp.get('price')

    return render_template_string("""
    <html>
      <head>
        <title>Let's buy a house!</title>
      </head>
      <body>
        <h3>
          A lovely new home is going on the market for {{ price }}. <br>
        </h3>
        <p>
          What will be your first offer?
        </p>
        <form action="/bid" method="GET">
          $<input type="text" length="10" name="bid"></input>
          <input type="submit"></input>
        </form>
      <br>
      <p><a href="/">Reload without resetting my session ID. I'll get the same offer when I come back.</a></p>
      <p><a href="/reset">Reset my session ID so I get re-randomized into a new treatment.</a></p>
      </body>
    </html>
    """, price=money_format(price))
```
{% endraw %}

This code first checks to see if the browser session has a random
`userid` yet. If not, we generate one using `uuid4()`. In your web framework,
likely you have a middleware package that assigns session ids for you. We're
doing it manually here.

Next, we use PlanOut to instantiate an AnchoringExperiment object for that
``userid``. This experiment object can tell us what parameter values the user
should get in this experiment via `anchoring_exp.get('parametername')`. We
use this to get the `price` parameter, then render it into the web page
using Flask's `render_template_string()` method, and a function we've defined
elsewhere to render big numbers as dollar amounts (`money_format()`).

The user can submit a number in the textbox.

## Logging outcomes
When the user submits the form, it calls the `/bid` endpoint. This endpoint
looks at the bid, then logs the bid amount by calling
`log_event('bid', {'bid_amount': their_bid})`,
which logs the userid along, the event type 'bid', and the bid amount.

{% raw %}
```python
@app.route('/bid')
def bid():
  bid_string = request.args.get('bid')
  bid_string = bid_string.replace(',', '') # get rid of commas
  try:
    bid_amount = int(bid_string)

    anchoring_exp = AnchoringExperiment(userid=session['userid'])
    anchoring_exp.log_event('bid', {'bid_amount': bid_amount})

    return render_template_string("""
      <html>
        <head>
          <title>Nice bid!</title>
        </head>
        <body>
          <p>You bid {{ bid }}. We'll be in touch if they accept your offer!</p>
          <p><a href="/">Back</a></p>
        </body>
      </html>
      """, bid=money_format(bid_amount))
  except ValueError:
    return render_template_string("""
      <html>
        <head>
          <title>Bad bid!</title>
        </head>
        <body>
          <p>You bid {{ bid }}. That's not a number, so we probably won't be accepting your bid.</p>
          <p><a href="/">Back</a></p>
        </body>
      </html>
      """, bid=bid_string)
```
{% endraw %}

### Examining log data
Data is logged to `anchoring_webapp.log`. Here is some sample log data:

```json
{"inputs": {"userid": "8444f55e-0d79-45e1-8660-9ca46a9a54ce"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 249999, "use_round_number": 0}, "time": 1396508171, "salt": "AnchoringExperiment", "event": "exposure"}
{"inputs": {"userid": "8444f55e-0d79-45e1-8660-9ca46a9a54ce"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 249999, "use_round_number": 0}, "time": 1396508178, "salt": "AnchoringExperiment", "event": "exposure"}
{"inputs": {"userid": "d2d73446-302e-4605-834c-e547d5c7a7aa"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 247796, "use_round_number": 0}, "time": 1396508182, "salt": "AnchoringExperiment", "event": "exposure"}
{"inputs": {"userid": "4fa255a1-8bd9-48ab-a8c2-4ecd5b15559c"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 250906, "use_round_number": 0}, "time": 1396508184, "salt": "AnchoringExperiment", "event": "exposure"}
{"inputs": {"userid": "d4f235a6-bc76-435e-8a4c-f56f1caf0770"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 260000, "use_round_number": 1}, "time": 1396508187, "salt": "AnchoringExperiment", "event": "exposure"}
{"inputs": {"userid": "d4f235a6-bc76-435e-8a4c-f56f1caf0770"}, "name": "AnchoringExperiment", "checksum": "3467a5ec", "params": {"price": 260000, "use_round_number": 1}, "time": 1396508205, "extra_data": {"bid_amount": 250000}, "salt": "AnchoringExperiment", "event": "bid"}
```

The first few lines correspond to exposures. We visited the page once, triggering
the first exposure. Then we re-loaded the page, which triggers another exposure
log with the same userid. We then clicked reset id three times -- which is why
you see four distinct userids.  Finally, for the last "user", we placed a bid
for $250,000.


Looking at the first line more closely,

```json
{
  "inputs": {
    "userid": "8444f55e-0d79-45e1-8660-9ca46a9a54ce"
  },
  "name": "AnchoringExperiment",
  "checksum": "3467a5ec",
  "params": {
    "price": 249999,
    "use_round_number": 0
  },
  "time": 1396485310,
  "salt": "AnchoringExperiment",
  "event": "exposure"
}
```

we can see that the user was assigned to have a precise (not round) number,
and that the price they received was 249999 (which got rendered as $249,999.00),
and that the event type was an "exposure".

The last row is similar in format but contains some additional information,

```json
{
  "inputs": {
    "userid": "d4f235a6-bc76-435e-8a4c-f56f1caf0770"
  },
  "name": "AnchoringExperiment",
  "checksum": "3467a5ec",
  "params": {
    "price": 260000,
    "use_round_number": 1
  },
  "time": 1396508205,
  "extra_data": {
    "bid_amount": 250000
  },
  "salt": "AnchoringExperiment",
  "event": "bid"
}
```

This user was given a round number -- $260,000, and we recorded a "bid" event.
This row has an additional key, "extra_data", which contains a dictionary of
extra data, namely, the bid amount, $250,000.


## Getting re-hashed into a new condition
If you click the link "Reset my session ID so I get re-randomized into a new treatment" on the main page, Flask will generate a new `uuid4()` for the session. The effect is that PlanOut will likely hash the new number into a different treatment for the experiment. So, every time you reload the page without clicking that link, you will always see the same condition. Likewise, the same user will always get hashed into the same condition. If you change the user id (for example manually, as we do here), you get re-randomized.
