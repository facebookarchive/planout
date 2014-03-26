# Namespaces

Experiments often involve manipulating persistent parameters,
such that multiple experiments, whether conducted serially or in parallel,
manipulate the same parameters.

You can use a namespace model of parameters to support these practices.
Each namespace is centered around a primary unit (e.g., user) such that, at any given time,
each primary unit is only in one experiment that manipulates parameters in that namespace.
These units are assigned to one of a large number (e.g., 10,000) of segments.
These segments are allocated to experiments.

TODO: add API - segment - parameter diagram

Rather than requesting a parameter from an experiment, you simply request a parameter from a namespace, which then handles identifying the experiment (if any) that that unit is part of.

``` python
API example
```

In sophisticated experimentation environments or large organizations, your namespace implementation will likely involve a database managing allocation of these primary units to experiments -- and other aspects of experiment managements. You can do this by extending the `Namespace` class.

For simpler settings and as a starting point, PlanOut provides a basic implementation of namespaces in `DemoNamespace`.

## DemoNamespace



