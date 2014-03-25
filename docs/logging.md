# Logging

You will usually want to log which units (e.g., users) are exposed to your experiment.

Logging this information enables monitoring your experiment and improving your analysis of the results. In particular, many experiments might only change your service for a very small portion of users; keeping track of these users will make your analysis more precise.

PlanOut provides hooks for your logging code so that you can log whenever a unit is exposed to an experiment.

## Overriding the `log` method
To log exposures using your existing logging system, just override the `log` method when extending the `Experiment` abstract class. For example, if you write to your logs with `XXX`, then you might create a class as follows.
```python

  def log(self, data):
    MyLogger.log(data)
    TODO

```

## Adding caching
By default, each instance of an Experiment class will only write to your logs once. But this can still result in a lot of writing when there are many instances created in a single request. So you may want to add some caching to prevent lots of unnecessary logging. Perhaps your logging system already handles this. Otherwise, you can add a key to a cache in the `log` method and check it before actually logging.
