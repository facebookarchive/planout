# Logging

You will usually want to log which units (e.g., users) are exposed to your experiment.

Logging this information enables monitoring your experiment and improving your analysis of the results. In particular, many experiments only change your service for the small portion of users that use a particular part of the service; keeping track of these users will make your analysis more precise.

PlanOut provides hooks for your logging code so that you can log whenever a unit is exposed to an experiment.

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

### Auto exposure logging

### Manual exposure logging

### Conversion logging.

## Extending logging functionality
this belongs in a separate md file
### Overloading the log configuration method

### Overriding the `log` method
To log exposures using your existing logging system, just override the `log` method when extending the `Experiment` abstract class. For example, if you write to your logs with `XXX`, then you might create a class as follows.
```python

  def log(self, data):
    MyLogger.log(data)
    TODO

```

### Adding caching
By default, each instance of an Experiment class will only write to your logs once. But this can still result in a lot of writing when there are many instances created in a single request. So you may want to add some caching to prevent lots of unnecessary logging. Perhaps your logging system already handles this. Otherwise, you can add a key to a cache in the `log` method and check it before actually logging.
