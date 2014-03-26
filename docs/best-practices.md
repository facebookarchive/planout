# Best practices

PlanOut makes it easy to implement bug-free code that randomly assigns users (or other units) to parameters. The `Assignment` and `Interpreter` object makes your assignment procedure reliable, and by using the `Experiment` class, you are more likely to notice if you did something bad in your experiment. There are a number of other considerations:

* Use the auto-exposure logging (link) functionality provided by the `Experiment` class.  Auto-exposure logging makes it easy to verify that your assignment procedure is working correctly, and makes it easier to track changes to units' assignments to parameters over time.
* Use a namespace (link) if you are planning on running concurrent experiments.
* Avoid changing an experiment while it is running. Instead, either run a second experiment with different units using a namespace, or rename your experiment and rerandomize the units.
* If you suspect your experiment might have changed, check the `salt` and `checksum` fields of your log. If either of these items change, it is likely that your assignments have also changed mid-way through the experiment. (this is kind of redundant with the first point and might be moved into the exposure logging section).
* Automate the analysis of your experiment. If you are running multiple related experiments, create a pipeline to automatically do the analysis.

There are no hard and fast rules for what kinds of changes are actually a problem, but if you follow the best practices above, you should be in reasonable shape.


## Randomization failures
### Non-equivalent groups
Experiments are used to test the change of one or more parameters on some average outcome (e.g., messages sent, or clicks on a button). Differences can be attributed to the experimental treatment (a change in parameter assignments) if the difference between two groups is completely random.

In practice, there are a number of common ways for two groups to not be equivalent:
 - Some users from one group were previously in a different group, while users from the other group were not.
 - Some users in one group were recently added to the experiment.
 - There was a bug in the code for one group but not the other, and things recently got fixed.

In this cases, it is often best to run a new experiment. This can be as easy as just changing the name or salt of your experiment, e.g., by setting:

```python
class MyNewExperiment(MyOldExperiment):
  def set_experiment_properties(self):
    self.name = 'new_experiment_name'
```

### Unanticipated consequences from changing experiments
Changes to experiments can dramatically alter which parameters users are assigned to. For example, consider

```python
class MyExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.button_text = UniformChoice(
      choices=['OK', 'Share', 'Share with friends'],
      unit=userid
    )
```
Changing the variable name `button_text` changes the assignment, since it is used to salt (link) to assignment procedure (see `Experiment` intro document).

Changing the number of choices for the `button_text` also affects users previously randomized into other conditions.  For example, removing the "Share" item from the `choices` list, will allocate some users who were previosuly in the "Share" condition to the "OK" and "Share with friends group". Their outcomes will now be a weighted average of the two, which may decrease the estimated difference between "OK" and "Share with friends".

If an additional choice were added, on the other hand, some percentage of each prior choice would be allocated to the new choice, whose outcome represents an average of all groups. Since those prior groups may have been around a lot longer, the newly added parameters may be subject to greater novelty effects.

## Learn more
Learn more by reading the PlanOut paper or Kohavi's excellent work on experimentation, including...
