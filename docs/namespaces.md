# Namespaces

Experiments often involve manipulating persistent parameters,
such that multiple experiments, whether conducted serially or in parallel,
manipulate the same parameters.

You can use a namespace model of parameters to support these practices.
Each namespace is centered around a primary unit (e.g., user) such that, at any given time,
each primary unit is only in one experiment that manipulates parameters in that namespace.
These units are assigned to one of a large number (e.g., 10,000) of segments.
These segments are allocated to experiments.

TODO: add API - segment - parameter diagram

Rather than requesting a parameter from an experiment, you simply request a parameter from a namespace, which then handles identifying the experiment (if any) that that unit is part of.

``` python
API example
```

In sophisticated experimentation environments or large organizations, your namespace implementation will likely involve a database managing allocation of segements of primary units to experiments -- and other aspects of experiment management. You can do this by implementing the abstract `Namespace` class or extending the `SimpleNamespace` class.

For simpler settings and as a starting point, PlanOut provides a basic implementation of namespaces in `SimpleNamespace`.

## SimpleNamespace

`SimpleNamespace` provides namespace functionality without being backed by a database or involving a larger experimentation management system. For both organizational and performance reasons, it is not recommended for namespaces that would be used to run many (e.g., thousands) experiments, but it more than sufficient for running several experiments manpulating the same parameters.


### Allocating and deallocating segments to experiments
When you extend `SimpleExperiment`, implement the `setup_experiments` method. This specifies a series of allocations and deallocations of segments to experiments.

When creating your first experiment in a new namespace, this method would be
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
```
where 'first experiment' is the name of your experiment, `MyFirstExperiment` is your experiment class, and 10 is the number of segements you are allocating to that experiment.

Adding additional experiments would just involve adding additional lines to the method. For example, you might run a larger follow-up experiment with the same design:
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
When an experiment is complete and you wish to make its segments available to new experiments, add a call to `remove_experiment`:
```python
def setup_experiments():
  self.add_experiment('first experiment', MyFirstExperiment, 10)
  self.add_experiment('second experiment', MySecondExperiment, 20)
  self.remove('first experiment')
```
In modifying this method, you should only add lines after all previous lines, since there is no database to store the state of allocation and allocation is dependent on past history.




