# PlanOut

PlanOut is a language for online field experimentation. It lets you implement both simple and complex experiments with only a few lines of code.

This release currently includes

  * The reference implementation of the PlanOut interpreter. This reads serialized PlanOut code and executes it. It's intended to be ported and run on top of an experimentation Platform. Currently it requires a compiler to convert from the PlanOut domain-specific language (see PlanOut paper).
  * PlanOutKit, an easy-to-use library for designing simple PlanOut experiments in python without the hassle of serializing experiments. It is recommended for students and those first learning how to implement experiments

## PlanOutKit

Here is an example of how to use PyPlanOut. To create a PlanOutKit experiment, you define a function where the first parameter is the experiment object, and the parameters are the names of the inputs.  The decorator ``@experiment(experiment_salt)`` specifies that the function is an experiment, and the experiment's salt is ``experiment_salt``.  You can use PlanOut's random assignment operators by setting ``exp.varname``, where ``exp`` is the name of the experiment argument (passed in as the first argument to the function), and ``varname`` is the name of the variable you are setting.  The experiment-level salt and the variable name are used to salt the random assignment.

```python

from planoutkit import *

@experiment('demo_experiment')
def myExperiment(exp, userid, country):
  exp.button_color = ['#ff0000', '#00ff00']
  if country == 'US':
    exp.button_text = 'signup now!'
  else:
    exp.button_text = 'sorry!'
  return exp

my_exp = myExperiment(userid=1212, country='US')
print my_exp.button_text, my_exp.button_color
print my_exp

```

which outputs:

```
signup now! ['#ff0000', '#00ff00']
{'button_color': ['#ff0000', '#00ff00'], 'input': {'country': 'US', 'userid': 1212}, 'button_text': 'signup now!'}
```
