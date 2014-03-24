# PlanOut

PlanOut is a language for online field experimentation. It lets you implement both simple and complex experiments with only a few lines of code. PlanOut defines a number of operators for assigning values to parameters --- for example, for randomly assigning users to a parameter controlling the color of a button. An experimental design is defined by using one or more of these operators to set parameters that control your Internet service.

For relatively simple environments, the experimental design can be specified by defining a Python method that uses these operators directly. For more complex environments, the design can be specified in a serialized representation of the calls to these operators, which is then interpreted and executed on demand.

PlanOut was created to make it easy to run more sophisticated experiment and to quickly iterate on these experiments, while satisfying the constraints of running as part of a large Internet service.

This release currently includes
  * The reference implementation of the PlanOut interpreter. This reads serialized PlanOut scripts and executes them. It is intended to be used as part of a large experimentation platform, potentially including such tools as a GUI for creating experiments. It requires a compiler to convert from the PlanOut domain-specific language (see PlanOut paper) to the serialization; a JavaScript implemention is provided.
  * PlanOutKit, an easy-to-use library for implementing PlanOut experiments in Python without the hassle of serializing experiments. It is recommended for students, those first learning how to implement experiments, and environments without the need for serialization.
  * An Experiment class / framework for implementing and logging experiments that works with both PlanOut language and PlanOutKit experiments.

## PlanOutKit

Here is an example of how to use PlanOutKit. To create a PlanOutKit experiment, you subclass an ``Experiment`` object, and implement an assignment method that includes all of your experiments inputs. Then, you construct a ``PlanOutKitMapper`` object that takes care of random assignment.  You can use PlanOut's random assignment operators by setting ``e.varname``, where ``e`` is the name of ``PlanOutKitMapper`` instance, and ``varname`` is the name of the variable you are setting.  Because we are using the ``SimpleExperiment`` class in the example below, the name of the experiment, ``FirstExperiment``, variable name, and the input data (``userid``) are used to perform the random assignment.  Parameter assignments and inputs are automatically logged into a file called ``firstexperiment.log'``.

```python

from planoutkit import *

class FirstExperiment(SimpleExperiment):
  def assign(self, userid):
    e = PlanOutKitMapper(self.salt)
    e.button_color = UniformChoice(choices=['#ff0000', '#00ff00'], unit=userid)
    e.button_text = WeightedChoice(
        choices=['Join now!', 'Sign up.'],
        weights=[0.3, 0.7], unit=userid)
    return e

my_exp = FirstExperiment(userid=12)
# parameters may be accessed via the . operator
print my_exp.get('button_text'), my_exp.get('button_color')

# experiment objects include all input data
for i in xrange(6):
  print FirstExperiment(userid=i)
```

which outputs (update this):

```
Sign up. #ff0000
{'inputs': {'userid': 0}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#00ff00', 'button_text': 'Sign up.'}}
{'inputs': {'userid': 1}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#ff0000', 'button_text': 'Join now!'}}
{'inputs': {'userid': 2}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#00ff00', 'button_text': 'Sign up.'}}
{'inputs': {'userid': 3}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#ff0000', 'button_text': 'Sign up.'}}
{'inputs': {'userid': 4}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#ff0000', 'button_text': 'Sign up.'}}
{'inputs': {'userid': 5}, 'salt': 'firstexperiment', 'name': 'firstexperiment', 'params': {'button_color': '#00ff00', 'button_text': 'Join now!'}}
```

### Learn more
Learn more about PlanOut by [reading the PlanOut paper](http://www-personal.umich.edu/~ebakshy/planout.pdf). You can cite PlanOut as "Designing and Deploying Online Field Experiments". Eytan Bakshy, Dean Eckles, Michael S. Bernstein. WWW '14. April 7–11, 2014, Seoul, Korea.
