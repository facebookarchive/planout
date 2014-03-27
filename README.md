# PlanOut

PlanOut is a toolkit and language for online field experimentation. It lets you implement both simple and complex experiments with only a few lines of code.  PlanOut provides methods for assigning values to parameters --- for example, for randomly assigning users to a parameter controlling the color of a button with different probabilities. An experimental design is defined by using one or more *operators* to set parameters that control your Internet service. The parameters each input (e.g., user) is assigned to is completely determnisitic.

For relatively simple environments, the experimental design can be specified by defining a Python class that uses these operators directly. For more complex environments, the design can be specified in a serialized representation of the calls to these operators, which is then interpreted and executed on demand.

PlanOut was created to make it easy to run more sophisticated experiment and to quickly iterate on these experiments, while satisfying the constraints of running as part of a large Internet service.

This release currently includes:
  * An extensible class for defining experiments. This class comes objects that make it easy to implement randomized assignments, and automatically logs key data according to best practices developed at Facebook.
  * 
  * The reference implementation of the PlanOut interpreter. This reads serialized PlanOut scripts and executes them. It is intended to be used as part of a large experimentation platform, potentially including such tools as a GUI for creating experiments. It requires a compiler to convert from the PlanOut domain-specific language (see PlanOut paper) to the serialization; a JavaScript implemention is provided.
  * PlanOutKit, an easy-to-use library for implementing PlanOut experiments in Python without the hassle of serializing experiments. It is recommended for students, those first learning how to implement experiments, and environments without the need for serialization.
  * An Experiment class / framework for implementing and logging experiments that works with both PlanOut language and PlanOutKit experiments.
  
### Who is PlanOut for?
The package can be used as a turn-key solution for students and researchers running or learning how to run experiments. It can also be useful as-as for startups.  The software is also designed to be extended for use in production environments for larger services, such as those run by startups.


### Example

Here is an example of how to use PlanOut. To create a basic PlanOut experiment, you subclass a ``SimpleExperiment`` object, and implement an assignment method. You can use PlanOut's random assignment operators by setting ``e.varname``, where ``params`` is the first argument passed to the ``assign()`` method, and ``varname`` is the name of the variable you are setting.
```python

from planoutkit import *

class FirstExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.button_color = UniformChoice(choices=['#ff0000', '#00ff00'], unit=userid)
    params.button_text = WeightedChoice(
        choices=['Join now!', 'Sign up.'],
        weights=[0.3, 0.7], unit=userid)

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

Because we are using the ``SimpleExperiment`` class, the name of the experiment, ``FirstExperiment``, variable name, and the input data (``userid``) are used to perform the random assignment.  Parameter assignments and inputs are automatically logged into a file called ``firstexperiment.log'``.


### Learn more
Learn more about PlanOut by [reading the PlanOut paper](http://www-personal.umich.edu/~ebakshy/planout.pdf). You can cite PlanOut as "Designing and Deploying Online Field Experiments". Eytan Bakshy, Dean Eckles, Michael S. Bernstein. Proceedings of the 23rd ACM conference on the World Wide Web. April 7–11, 2014, Seoul, Korea, or by copying and pasting the bibtex below:
``` bibtex
@inproceedings{bakshy2014www,
	Author = {Bakshy, E. and Eckles, D. and Bernstein, M.S.},
	Booktitle = {Proceedings of the 23rd ACM conference on the World Wide Web},
	Organization = {ACM},
	Title = {Designing and Deploying Online Field Experiments},
	Year = {2014}}
```
