# Best practices

PlanOut makes it easy to implement bug-free code that randomly assigns users (or other units) to parameters. The Experiment and Namespace classes are designed to reduce common errors in deploying and logging experiments. Here are a few tips for running experiments:

* Use auto-exposure logging (link), which is enabled by default.  Auto-exposure logging makes it easier to check that your assignment procedure is working correctly, increases the precision of your experiment, and reduces errors in downstream analysis.
* Avoid changing an experiment while it is running. Instead, either run a follow-up experiment using a namespace (link), or create a new experiment with a different salt to re-randomize the units. These experiments should be analyzed separately from the original experiment.
* Automate the analysis of your experiment. If you are running multiple related experiments, create a pipeline to automatically do the analysis.


There are no hard and fast rules for what kinds of changes are actually a problem, but if you follow the best practices above, you should be in reasonable shape.


## Randomization failures
Experiments are used to test the change of one or more parameters on some average outcome (e.g., messages sent, or clicks on a button). Differences can be safely attributed to a change in parameters if treatments are assigned to users completely at random.

In practice, there are a number of common ways for two groups to not be equivalent (beyond random imbalance):
 - Some units from one group were previously in a different group, while users from the other group were not.
 - Some units in one group were recently added to the experiment.
 - There was a bug in the code for one group but not the other, and that bug recently got fixed.

In these cases, we suggest that you launch a new experiment, either through the use of namespaces (links), or by re-assigning all of the units in your experiment.  This can be done by simply changing the salt of your experiment:

```python
class MyNewExperiment(MyOldExperiment):
  def set_experiment_properties(self):
    self.name = 'new_experiment_name'
    self.salt = 'new_experiment_salt'
```


### Unanticipated consequences from changing experiments
Changes to experiment definitions will generally alter which parameters users are assigned to. For example, consider an experiment that manipulates the label of a button for sharing a link. The main outcome of interest is the effect of this text on how many links users share per day.


```python
class SharingExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.button_text = UniformChoice(
      choices=['OK', 'Share', 'Share with friends'],
      unit=userid
    )
```
Changing the variable name `button_text` changes the assignment, since it is used to salt (link) to assignment procedure (see `Experiment` intro document).

Changing the number of choices for the `button_text` also affects users previously randomized into other conditions.  For example, removing the 'Share' item from the `choices` list, will allocate some users who were previosuly in the 'Share' condition to the 'OK' and 'Share with friends group'. Their outcomes will now be a weighted average of the two, which may decrease the observed difference between 'OK' and 'Share with friends'.

If an additional choice were added to `choices`, some percentage of each prior choice would be allocated to the new choice, whose outcome represents an average of all groups. Comparisons between users still in the old groups (the newly added parameters may be subject to greater novelty effects.

## Detecting problems
If you suspect your experiment might have changed, check the `salt` and `checksum` fields of your log. If either of these items change, it is likely that your assignments have also changed mid-way through the experiment.

## Learn more
[Designing and Deploying Online Field Experiments](http://www-personal.umich.edu/~ebakshy/planout.pdf).  WWW 2014. Eytan Bakshy, Dean Eckles, Michael S. Bernstein.
[Seven Pitfalls to Avoid when Running Controlled Experiments on the Web.](http://www.exp-platform.com/Documents/2009-ExPpitfalls.pdf) KDD 2009. Thomas Crook, Brian Frasca, Ron Kohavi, and Roger Longbotham.
