---
id: getting-started
title: Getting started with PlanOut
layout: docs
permalink: /docs/getting-started.html
prev: why-planout.html
next: sample-web-app.html
---

In this tutorial we will guide you through installing PlanOut and explain how
to implement basic experiments.

## Quick install
You can install PlanOut using Easy Install:

```
sudo easy_install planout
```

Or you can checkout and download the software from github:

```
sudo python setup.py install
```
It has been tested on Mac OS X and Linux.

## Your first experiment

### Defining an experiment
To create your first experiment, you will define a subclass of the
`SimpleExperiment` object. *Experiment objects* come with all the low-level
stuff you generally don't want to worry about while setting up experiments,
like making sure different experiments assign parameters (variables that
control your site), independently of one another, or log to the right
places at the right time.

For all of the examples we use in the documentation, we will use the
`SimpleExperiment` class, which includes enough basic logging functionality to
get you started.

Consider a hypothetical get out the vote experiment where we randomize
individuals into different button colors and different button phrasings,
similar to what some people on Facebook might have seen on [Election Day in 2012](http://newsroom.fb.com/news/2012/11/election-day-2012-on-facebook/).

```python
from planout.experiment import SimpleExperiment
from planout.ops.random import *

class VotingExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.button_color = UniformChoice(choices=["#ff0000", "#00ff00"],
      unit=userid)
    params.button_text = UniformChoice(choices=["I'm voting", "I'm a voter"],
      unit=userid)
```

The first line imports the `SimpleExperiment` class. The second line says to
import all the randomization operators.  *Operators* are special kinds of
objects which (with the help of Experiment objects), deterministically map
inputs to randomized values [through hashing](how-planout-works.html).

The next block of code says to create a child class of `SimpleExperiment`,
called `VotingExperiment`. All experiments which subclass `SimpleExperiment` must
implement an `assign()` method, which takes an, which we call
it `params` by convention, along with whatever input variables are expected by
your experiment.  Here, the only argument is `userid`.

The next two lines set the parameters, `button_color` and `button_text` to
randomized values, based on the input unit, `userid`. `UniformChoice` is one
of several [random assignment operator](random-operators.html) objects.
It tells PlanOut to select among
one of several items of a list with equal probability.
When you call `params.varname = x`, and `x` is a random operator object, PlanOut
will automatically evaluate `x`, and (unless otherwise specified), will use
the variable name to ensure that the assignment of each parameter is
deterministic.

### Getting a random assignment
To get the parameter assignment for a given input, you simply create an instance of the
class, and and call the `get()` method for the desired parameter.

```python
exp = VotingExperiment(userid=14)
call_to_action_color = exp.get('button_color')
call_to_action = exp.get('button_text')
```

This would get the assignment for an individual whose account identifier is 14.
(In practice, instead of this magic number, you would use some variable or method
that gives the user ID of the person viewing the page.)

### Logging treatment assignment
When `get()` is called, an exposure event is automatically logged.  This
data contains a complete log of the treatment receipt, including a timestamp,
input data, and treatment assignment.

In this example, we are extending SimpleExperiment, which uses the standard
Python `logger` module and records log data as rows of JSON.
Since we are not configuring any additional variables, the data is logged to a
file named after the class: "VotingExperiment.log".
An example row (expanded for readability) would look like


```javascript
{
  "inputs": {
    "userid": 14
  },
  "name": "VotingExperiment",
  "params": {
    "button_color": "#ff0000",
    "button_text": "I'm voting"
  },
  "time": 1396487778,
  "salt": "VotingExperiment",
  "event": "exposure"
}
```

Here, we can see a few main keys that are logged by default:

 * `inputs`: a dictionary of all inputs given to the experiment instance.

 * `name`: the name of the experiment. By default this is the same as the name

 of the class.
 * `params`: all the parameters assigned by the experiment.

 * `time`: a unix-formatted timestamp of the event.

 * `salt`: the (experiment-level salt)[how-planout-works.html] used for randomization.

 * `event`: the type of event.


### Logging an action
On the endpoint that records button clicks, we can log the outcome using the
experiment class:

```python
exp = VotingExperiment(userid=clicking_user)
exp.log_event('button_click')
```

Here is what the log would look like

```json
{
  "inputs": {
    "userid": 14
  },
  "name": "VotingExperiment",
  "params": {
    "button_color": "#ff0000",
    "button_text": "I'm voting"
  },
  "time": 1396507677,
  "salt": "VotingExperiment",
  "event": "button_click"
}
```

You now have a working experiment.
