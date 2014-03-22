# Extending PlanOut

## Core concepts
An *Experiment* object takes inputs and maps it to parameter assignments.  Experiment objects also handle logging and caching.

*Mappers* are execution environments used to implement experiments. They execute *operators* which are functions that perform basic operations, including deterministic random assignment.


## Mappers
A mapper translates inputs to parameter assignments.
There are two main types of PlanOut mappers: `PlanOutKitMapper`, which is useful for many (ad hoc) experimentation needs, and `PlanOutInterpreterMapper`, which reads in serialized experiment definitions and is suitable for use in production environments when experiments are centrally managed via a Web interface. ``PlanOutInterpreterMapper``

## Experiment class

``
hello there
``
