# Namespaces

Namespaces are used to manage related experiments that manipulate the same parameter. These experiments might be run sequentially (over time) or in parallel. When experiments are conducted in parallel, namespaces can be used to keep experiments "exclusive" or "non-overlapping".


Namespaces and similar to models such as Google's "layers" and Facebook's "universes" which solve the overlapping experiment problem by centering experiments around a primary unit, such as user IDs.  Within a given namespace, each userid belongs to at most one experiment. Namespace objects, such as the ones included with PlanOut (link to SimpleNamespace page), manage this kind of functionality.


### How do namespaces work?
Under the hood, primary units are mapped to one of a large number of segments (e.g., 10,000).
These segments are allocated to experiments. For any given unit, a namespace manager looks up that unit's segment. If the segment is allocated to an experiment, the input data is passed to the experiment, and random assignment occurs using the regular experimental logic of a vanilla `Experiment` class.

If the primary unit is not mapped to an experiment, or a parameter is requested that is not defined by the experiment, a default experiment or value may be used.
 This allows experimenters to configure default values for parameters on the fly in a way that does not interfere with currently running experiments.


Rather than requesting a parameter from an experiment, you simply request a parameter from a namespace, which then handles identifying the experiment (if there is one) that that unit is part of.

### When do I need to use a namespace?
Namespaces are useful whenever there is at least one variable in your code base that you would like to experiment with, either over time or simultaneously.


For simpler settings and as a starting point, PlanOut provides a basic implementation of namespaces in `SimpleNamespace`.
