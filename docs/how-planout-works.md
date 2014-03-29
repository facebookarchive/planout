# How PlanOut works

PlanOut works by hashing input data into numbers, and using these numbers to generate what are effectively pseudo-random values to pick numbers.

## Pseudo-random assignment through hashing
Consider the following experiment:
```python
class SharingExperiment(SimpleExperiment):
  def set_attributes(self):
    self.name = 'sharing_name'
    self.salt = 'sharing_salt'

  def assign(self, params, userid):
    params.button_text = UniformChoice(
      choices=['OK', 'Share', 'Share with friends'],
      unit=userid
    )
```
We specify a randomized parameter, `button_text`. We generate the assignment by first generating a string composed of the experiment-level salt, `sharing_salt`, the variable name, `button_text`, and the input unit. For example, if we were to get the parameter for `userid` = 4, as in ``SharingExperiment(userid=4).get('button_text')``, PlanOut would compute the SHA1 checksum for:
```
sharing_salt.button_text.4
```
and then the last few digits of this checksum to index into the given list of `choices`.  Since SHA1 is cryptographically safe, even minor changes to the hashing string (e.g., considering `userid=41` instead of `4` will result in a totally different number).

All PlanOut operators include basic unit tests (link) to verify that assignments are fairly random.

## Specifying salts
Experiment-level salts can be set manually. If experiment-level salts are not specified manually in the set_attributes() method, then the experiment name is used as the salt. The default name for an experiment is just the name of the class.

You can also specify salts for individual variables. This lets you change the name of the variable you are logging without changing the assignment. Use variable level salts with caution, since they might lead to failures in randomization (link).

## Interaction with namespaces
The name of the namespace is automatically appended to the SHA1 string, so that experiments with the same names and parameters have independent random assignments.
