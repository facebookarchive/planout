# Extending PlanOut

Experiments
- Logging
- Assignment scheme
- Salt
- Uses a mapper

Assignment schemes
- Mappers are helpers for doing deterministic pseudorandom assignment

Mappers:
 - One where you code in python
 - 

## Core concepts
An *Experiment* object takes inputs and maps it to parameter assignments.  Experiment objects also handle logging and caching.

*Mappers* are execution environments used to implement experiments. They execute *operators* which are functions that perform basic operations, including deterministic random assignment.


## Mappers
A mapper translates inputs to parameter assignments.
There are two main types of PlanOut mappers: `PlanOutKitMapper`, which is useful for many (ad hoc) experimentation needs, and `PlanOutInterpreterMapper`, which reads in serialized experiment definitions and is suitable for use in production environments when experiments are centrally managed via a Web interface. ``PlanOutInterpreterMapper``

## Experiment class

The experiment class implements core functionality associated with each experiment. In particular, every experiment has a:
 - name
 - experiment-level salt
 - an assignment scheme using a PlanOut mapper that translates inputs to parameter values.
 - logging, which by default maintains an "exposure log" of when inputs (e.g., userids) get mapped to parameter. This makes it easier to keep track of who was in your experiment, and restrict your analysis to the experiment.

To define a new experiment, one subclasses the Experiment class. By default, the name of the experiment will be the name of the subclass, and the experiment-level salt will be the name of the experiment.
