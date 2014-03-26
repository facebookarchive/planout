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
