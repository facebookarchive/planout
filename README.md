# PlanOut

PlanOut is a language for online field experimentation. It lets you implement both simple and complex experiments with only a few lines of code.

This release currently includes

  * The reference implementation of the PlanOut interpreter. This reads serialized PlanOut code and executes it. It's intended to be ported and run on top of an experimentation Platform. Currently it requires a compiler to convert from the PlanOut domain-specific language (see PlanOut paper).
  * PyPlanOut, an easy-to-use library for designing simple PlanOut experiments in python without the hassle of serializing experiments. It is recommended for students and those first learning how to implement experiments

## PyPlanOut

Here is an example of how to use PyPlanOut.
```python

def myExperiment(userid, country):
  input_data = locals()
  my_exp = PyPlanOutExperiment('exp_name')
  my_exp.button_color = ['#ff0000', '#00ff00']
  if country == 'US':
    my_exp.button_text = 'signup'
  else:
    my_exp.button_text = 'sorry!'
  return my_exp

my_exp = myExperiment(1212, 'US')
print my_exp.button_text, my_exp.button_color

```
