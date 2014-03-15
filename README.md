# PlanOut

PlanOut is a language for online field experimentation. It lets you implement both simple and complex experiments with only a few lines of code.

This release currently includes

  * The reference implementation of the PlanOut interpreter. This reads serialized PlanOut code and executes it. It's intended to be ported and run on top of an experimentation Platform. Currently it requires a compiler to convert from the PlanOut domain-specific language (see PlanOut paper).
  * PlanOutKit, an easy-to-use library for designing simple PlanOut experiments in python without the hassle of serializing experiments. It is recommended for students and those first learning how to implement experiments

## PlanOutKit

Here is an example of how to use PyPlanOut. To create a PlanOutKit experiment, you define a function where the first parameter is the experiment object, and the parameters are the names of the inputs.  The decorator ``@experiment(experiment_salt)`` specifies that the function is an experiment, and the experiment's salt is ``experiment_salt``.  You can use PlanOut's random assignment operators by setting ``exp.varname``, where ``exp`` is the name of the experiment argument (passed in as the first argument to the function), and ``varname`` is the name of the variable you are setting.  The experiment-level salt and the variable name are used to salt the random assignment.

```python

from planoutkit import *

class firstExperiment(SimpleExperiment):
  def execute(self, userid):
    e = PlanOutKitMapper(self.salt)
    e.button_color = UniformChoice(choices=['#ff0000', '#00ff00'], unit=userid)
    e.button_text = WeightedChoice(
        choices=['Join now!', 'Sign up.'],
        weights=[0.2, 0.8], unit=userid)
    return e

my_exp = firstExperiment(userid=12)
# parameters may be accessed via the . operator
print firstExperiment.get('button_text'), firstExperiment.get('button_color')

# experiment objects include all input data
for i in xrange(4):
  print firstExperiment(userid=i)
```

which outputs (update this):

```
Sign up. #ff0000
{'button_color': '#00ff00', 'input': {'userid': 0}, 'button_text': 'Join now!'}
{'button_color': '#00ff00', 'input': {'userid': 1}, 'button_text': 'Join now!'}
{'button_color': '#ff0000', 'input': {'userid': 2}, 'button_text': 'Join now!'}
{'button_color': '#ff0000', 'input': {'userid': 3}, 'button_text': 'Sign up.'}
```
