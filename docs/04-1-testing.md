---
id: testing
title: Testing 
layout: docs
permalink: /docs/testing.html
prev: logging.html
next: namespaces.html
---

One challenge of developing complex randomized experiments online is that they
can be difficult to test. PlanOut supports testing through overrides. Overrides
let you "freeze" the value of a variable so that it does not change over time.
This lets you test different user experiences generated by your experiment
without having to modify your experiment definition, or go through a bunch of
random userids until you hit the set of parameters you are looking for.

## An interesting but annoying to test experiment
Consider an experiment from [Using Social Psychology to Motivate Contributions
to Online Communities](http://repository.cmu.edu/cgi/viewcontent.cgi?article=1087&context=hcii).
To examine questions around social loafing and goal-setting, the experiment
first randomly assigns users to different group sizes, and then to receive
either a general or specific goal. If they are assigned to a specific goal,
they are assigned an additional parameter, the goal, expressed in terms of
ratings per user, for each group size:

```python
class Exp1(SimpleExperiment):
  def assign(self, params, userid):
    params.group_size = UniformChoice(choices=[1, 10], unit=userid);
    params.specific_goal = BernoulliTrial(p=0.8, unit=userid);
    if params.specific_goal:
      params.ratings_per_user_goal = UniformChoice(
        choices=[8, 16, 32, 64], unit=userid)
      params.ratings_goal = params.group_size * params.ratings_per_user_goal
    return e
```

##

```python
e = Exp1(userid=4)
print e.get_params()
```

```
{'group_size': 10, 'specific_goal': 1, 'ratings_goal': 320,  'ratings_per_user_goal': 32}
```

```python
e = Exp1(userid=4)
e.set_overrides({'specific_goal': 0})
print e.get_params()
```

```
{'group_size': 10, 'specific_goal': 0}
```

```python
e = Exp1(userid=session['userid'])
e.set_overrites('specific_goal': 0)
print e.get_params()
```



```json
{
  "inputs": {
    "userid": 9
  },
  "name": "Exp1",
  "checksum": "2b0c4cfb",
  "params": {
    "group_size": 1,
    "specific_goal": 0
  },
  "time": 1396513178,
  "salt": "Exp1",
  "event": "exposure"
}
```

In addition, a `checksum` field is attached. This is part of an MD5 checksum of
your code, so that analysts can keep track of when an experiments' assignments
have potentially changed: whenever the checksum changes, the assignment
procedure code is different, and whenever the salt changes, the assignments
will be completely different.

`SimpleExperiment` computes checksums from the code contained in your class'
`assign()` method.  Because of the way the Python interpreter works, this
checksum can only be computed when Python is running in non-interactive mode,
so if you are following along this tutorial via the Python shell, you won't
see a checksum in your log file.

## Types of logs

### Auto-exposure logging
By default, exposures are logged once per instance of an experiment object when you first get a parameter. This is called auto-exposure logging. It is recommended for most situations, since you will want to track whenever a unit is exposed to your experiment. Generally, any unit for which a parameter has been retrieved should be counted as exposed, unless you wish to make further assumptions.

### Manual exposure logging
In some cases, you might want to choose exactly when exposures are logged. You can disable auto-exposure logging  with the `set_auto_exposure_logging` method and instead choose to directly call `log_exposure` to keep track of exposures.

Why might you want to do this? You might be adding experimental assignment information to other existing logs of outcome data, but many of the users who have outcome observations may not actually have been exposed. Other cases occur when some advance preparation of some components (e.g., UI) or data are required, but you can assume that parameter values set at this stage do not yet affect the user.

### Logging other events
You want to see how the parameters you are manipulating affect outcomes, conversions, or other events.
In many cases, you may do this analysis by later combining your exposure logs and other behavioral logs by joining on the relevant unit ID (e.g., userid). Especially for more real-time analysis, it can be useful to log outcome data with assignment data.

It can also be convenient to log these events along with assignment information. You can do this by calling the `log_event()` method directly, specifying an event name and a dictionary of any additional data to log.

Alternatively, you may have existing logging procedures for many of these events that you don't want to be part of your experiment definition. In this case, you could add experimental assignment information to these logs by instantiating an experiment, turning off auto-exposure logging for that instance, and adding parameter information to your logs.