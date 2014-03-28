# Iterating on experiments with `SimpleNamespace`

`SimpleNamespace` provides namespace functionality without being backed by a database or involving a larger experimentation management system. For both organizational and performance reasons, it is not recommended for namespaces that would be used to run many (e.g., thousands) experiments, but it should be sufficient for iterating on smaller-scale experiments.

Similar to how you create experiments with the `SimpleExperiment` class, new namespaces are created through subclassing.  `SimpleNamespace` two requires that developers implement two methods:
 - `setup_attributes()`: this method sets the namespace's name, the primary unit, and number of segments. The primary unit is the input unit that gets mapped to segments, which are allocated to experiments.
 - `setup_experiments()`: this method allocates and deallocates experiments. When used in production, lines of code should only be added to this method.

```python
class ButtonNamespace(SimpleNamespace):
  def setup_attributes(self):
    self.name = 'my_demo'
    self.primary_unit = 'userid'
    self.num_segments = 1000

  def setup_experiments():
    # create and remove experiments here
```

In the example above, the name of the namespace is `my_demo`. This gets used, in addition to the experiment name and variable names, to hash units to experimental conditions. The number of segments is the granularity of the experimental groups.

### Allocating and deallocating segments to experiments
When you extend `SimpleNamespace` class, you implement the `setup_experiments` method. This specifies a series of allocations and deallocations of segments to experiments.

For example, the following setup method:
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 100)
```
would allocate  'first experiment' is the name of your experiment, 100 of 1000 segments, selected at random to be allocated to the `MyFirstExperiment` class. In this example (see demo/demo_namespace.py), `MyFirstExperiment` is a subclass of `SimpleExperiment`.

Adding additional experiments would just involve appending additional lines to the method. For example, you might run a larger follow-up experiment with the same design:
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
  self.add_experiment('first experiment, replication 1', MyFirstExperiment, 40)
```
Or you might run a new experiment with a different design:
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
  self.add_experiment('second experiment', MySecondExperiment, 20)
```
When an experiment is complete and you wish to make its segments available to new experiments, append a call to `remove_experiment`:
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
  self.add_experiment('second experiment', MySecondExperiment, 20)
  self.remove_experiment('first experiment')
  self.add_experiment('third experiment', MyThirdExperiment, 50)
```
Note: In modifying this method, you should only add lines after all previous lines. Inserting calls to `add_experiment` or `remove_experiment` will likely move segments from one experiment to another -- not what you want! This is because there is no stored allocation state (e.g., in a database), so the current allocation is dependent on the full history.
