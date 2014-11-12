---
layout: default
title: A framework for online field experiments
id: home
hero: true
---

PlanOut is a framework for online field experiments. It was created to make it easy to run and iterate on sophisticated experiments in a statistically sound manner
while satisfying the constraints of deployed Internet services.

Developers implement experiments using PlanOut by providing a high-level
specification for how _units_ (e.g., users, cookie IDs) should be mapped to
parameters that control the user experience.
For example, to create a 2x2 factorial experiment that randomizes both the color
and the text on a button, using the Python-based framework, one can simply
create a class like this:

```python
class MyExperiment(SimpleExperiment):
  def assign(self, params, userid):
    params.button_color = UniformChoice(choices=['#ff0000', '#00ff00'],
      unit=userid)
    params.button_text = UniformChoice(choices=['I voted', 'I am a voter'],
      unit=userid)
```

Then, in the application code, instead of just using a constant (e.g., '#ff00000'),
you query an instance of the class to find out what
values should be used for the current user:

```python
my_exp = MyExperiment(userid=42)
color = my_exp.get('button_color')
text = my_exp.get('button_text')
```

PlanOut takes care of correctly randomizing each ``userid`` to parameter values.
It does so by determnisitcally hashing the input, so each ``userid`` will always map onto the
same parameter values for that experiment. As soon as you access any of the parameters,
core parts of the data you need to analyze your experiment are automatically
logged.

The PlanOut framework includes:

  * Extensible classes for [implementing](getting-started.html) and [testing](testing.html) experiments, which [automatically log](logging.html)
  important data.

  * A system for managing and deploying multiple mutually exclusive experiments, called [namespaces](namespaces.html)

  * The [PlanOut language](interpreter.html), which lets you define,
  serialize, store, and execute experiment definitions in a platform-independent way.

### Who is PlanOut for?
PlanOut is for researchers, businesses, and students wanting to run experiments.
It's designed to be easy to get up and running with for first-time experimenters,
and extensible for those wanting to use it in a large production environments.
This open source implementation shares many of the key design decisions of Facebook's
experimentation stack, which is used to conduct experiments with hundreds of
millions of people.


### Learn more
Learn more about PlanOut and experimentation practices at Facebook by reading the PlanOut paper, [Designing and Deploying Online Field Experiments](https://www.facebook.com/download/255785951270811/planout.pdf).

If you are publishing research using PlanOut, here is some bibtex for you:

```
@inproceedings{bakshy2014www,
	Author = {Bakshy, E. and Eckles, D. and Bernstein, M. S.},
	Booktitle = {Proceedings of the 23rd ACM conference on the World Wide Web},
	Organization = {ACM},
	Title = {Designing and Deploying Online Field Experiments},
	Year = {2014}}
```
