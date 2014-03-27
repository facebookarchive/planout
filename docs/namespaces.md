# Namespaces

Namespaces are used to manage multiple related experiments which manipulate the same parameter. These experiments might be run sequentially (over time) or in parallel.  When conducted in parallel, these experiments need to be "exclusive" or "non-overlapping".


Namespaces are similar to models called "layers" (at Google) and "universes" (at Facebook).
Each namespace is centered around a primary unit (e.g., users) so that each primary unit is in only one experiment that manipulates parameters in that namespace.

### How do namespaces work?
Under the hood, primary units are mapped to one of a large number (e.g., 10,000) of segments.
These segments are allocated to experiments. For any given unit, a namespace manager looks up that unit's segment. If the segment is allocated to an experiment, the input data is passed to the experiment, and random assignment occurs using the regular experimental logic of a vanilla `Experiment` class.

If the primary unit is not mapped to an experiment, or a parameter is requested that is not defined by the experiment, a default experiment or value may be used.

TODO: add API - segment - parameter diagram

Rather than requesting a parameter from an experiment, you simply request a parameter from a namespace, which then handles identifying the experiment (if there is one) that that unit is part of.


In sophisticated experimentation environments or large organizations, your namespace implementation will likely involve a database managing allocation of segements of primary units to experiments -- and other aspects of experiment management. You can do this by implementing the abstract `Namespace` class or extending the `SimpleNamespace` class.

For simpler settings and as a starting point, PlanOut provides a basic implementation of namespaces in `SimpleNamespace`.

## SimpleNamespace

`SimpleNamespace` provides namespace functionality without being backed by a database or involving a larger experimentation management system. For both organizational and performance reasons, it is not recommended for namespaces that would be used to run many (e.g., thousands) experiments, but it should be sufficient for smaller-scale experiments.

Similar to the `SimpleExperiment` class, one defines new namespaces through subclassing. The two required methods are `setup_attributes()`, which sets the namespace's name, and the primary unit. The primary unit is the input unit that gets mapped to segments, which are allocated to experiments.  The `setup_experiments()` method allocates and deallocates experiments.

```python
class ButtonNamespace(SimpleNamespace):
  def setup_attributes(self):
    self.name = 'my_demo'
    self.primary_unit = 'userid'
    self.num_segments = 1000

  def setup_experiments():
    # create and remove experiments here
```
In the example above

### Allocating and deallocating segments to experiments
When you extend `SimpleExperiment`, implement the `setup_experiments` method. This specifies a series of allocations and deallocations of segments to experiments.

When creating your first experiment in a new namespace, this method would be
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
```
where 'first experiment' is the name of your experiment, `MyFirstExperiment` is your experiment class, and 10 is the number of segements you are allocating to that experiment.

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
