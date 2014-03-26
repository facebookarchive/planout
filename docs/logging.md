# Logging

You will usually want to log which units (e.g., users) are exposed to your experiment.

Logging this information enables monitoring your experiment and improving your analysis of the results. In particular, many experiments only change your service for the small portion of users that use a particular part of the service; keeping track of these users will make your analysis more precise.

The `SimpleExperiment` class providing functionality for logging data to a file using Python's `logger` module. Additionally, you can extend `Experiment` to call your logging code instead (link to extending-logging).

## Anatomy of a log
Consider Experiment 1 from the PlanOut paper (link):
```
class Exp1(SimpleExperiment):
  def assign(self, e, userid):
    e.group_size = UniformChoice(choices=[1, 10], unit=userid);
    e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
    if e.specific_goal:
      e.ratings_per_user_goal = UniformChoice(
        choices=[8, 16, 32, 64], unit=userid)
      e.ratings_goal = e.group_size * e.ratings_per_user_goal
    return e
```
It takes a `userid` as input, and assigns three paramers, `group_size`, `specific_goal`, and `ratings goal`. It does not specify a custom salt (link) or experiment name, so the experiment salt and name are automatically set to the class name `Exp3`. The default logger in `SimpleExperiment` log all of these fields:

```
{'inputs': {'userid': 3}, 'checksum': '4b80881d', 'salt': 'Exp1', 'name': 'Exp1', 'params': {'specific_goal': 1, 'ratings_goal': 160, 'group_size': 10, 'ratings_per_user_goal': 16}}
```

In addition, a `checksum` field is attached. This is part of an MD5 checksum of your code, so that analysts can keep track of when an experiments' assignments have potentially changed: whenever the checksum changes, the assignment procedure code is different, and whenever the salt changes, the assignments will be completely different.

TODO: exposure-log logs should have a field that specifies its an exposure. This payload should also include a timestamp.

## Types of logs

### Auto-exposure logging
By default, exposures are logged once per instance of an experiment object when you get a parameter. This is auto-exposure logging. It is recommended for most situations, since you will want to track whenever a unit is exposed to your experiment. Generally, any unit for which a parameter has been retrieved should be counted as exposed, unless you wish to make further assumptions.

### Manual exposure logging
In some cases, you might want to choose exactly when exposures are logged. You can disable auto-exposure logging  with the `set_auto_exposure_logging` method and instead choose to directly call `log_exposure` to keep track of exposures.

Why might you want to do this? You might be adding experimental assignment information to other existing logs of outcome data, but many of the users who have outcome observations may not actually have been exposed. Other cases occur when some advance preparation of some components (e.g., UI) or data are required, but you can assume that parameter values set at this stage do not yet affect the user.

### Conversion logging
You want to see how the parameters you are manipulating affect outcomes or conversion events. It can also be convenient to log these events along with exposures. You can do this by calling the `log_outcome` method.

You may have existing logs for many of these events. In this case, you could add experimental assignment information to these logs by instantiating an experiment, turning off auto-exposure logging for that instance, and adding parameter information to your logs. Alternatively, you can later join exposure and outcome data on unit identifiers (e.g., user IDs).
