A/B tests and other randomized experiments are widely used as part of continually improving Web and mobile apps and services. PlanOut makes it easy to run both simple and complex experiments.

## Focus on parameters

PlanOut is all about providing randomized values of parameters that control your service. Instead of using a constant, just use PlanOut to determine these parameters (e.g., text size or color, the presence of a new feature, the number of items in a list). Now you have an experiment.

## From simple to complex

It is easy to implement an A/B test in PlanOut, or other simple experiments like those involving a factorial design. But is not much harder to implement more complex designs. Multiple types of units (e.g., users, pieces of content) can be randomly assigned to parameter values in the same experiment. Experiments can also involve directly randomizing other inputs, such as randomly selecting which three friends to display to a user.

## Automatic logging
You will often want to keep track of which users (or other units) have been exposed to your experiment. This can make subsequent analysis more precise and prevent common errors in analysis. PlanOut calls your logging code whenever a parameter value is checked.


## Advanced features

We created PlanOut to meet requirements from running experiments at Facebook, which gives rise to some of its more advanced features.

### Serialization
Experiments can also be specified through JSON code. This can enable separate review processes for changes to the experiment, support multi-platform execution, and restrict the range of operations that should occur during experimental assignment (for reasons of, e.g., performance, correctness, static analysis). It also allows developers to implement their own tools to specify experiments without writing any code at all.

### Domain-specific language
PlanOut experiments can be specified through the PlanOut language, which concisely describes an experiment using a set of primitive operations.  PlanOut language code is compiled into the JSON serialization, which can be executed by the PlanOut interpreter as needed.

### Iterative experimentation
The PlanOut library includes a basic namespace class (link) for managing multiple, iterative experiments that run concurrently.
