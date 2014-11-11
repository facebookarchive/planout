## Extending logging functionality
If you have already adopted some method for logging events, you may want to use that method to log experiment-related events, such as exposures and experiment-specific outcomes. You can do this by extending the `Experiment` abstract class and overriding the `log` method.

### Overriding the `log` method
To log exposures using your existing logging system, just override the `log` method when extending the `Experiment` abstract class. For example, if you write to your logs with `MyLogger`, then you might create a class as follows.
```python

  def log(self, data):
    MyLogger.log(data)

```

### Writing a log configuration method
For some logging frameworks, you may want to have a way to setup your logger once per `Experiment` instance. In this case, you can implement a method to do this setup, which then gets called, as needed, by your `log` method.


### Adding caching
By default, each instance of an Experiment class will only write to your logs once. But this can still result in a lot of writing when there are many instances created in a single request. So you may want to add some caching to prevent lots of unnecessary logging. Perhaps your logging system already handles this. Otherwise, you can add a key to a cache in the `log` method and check it before actually logging.
