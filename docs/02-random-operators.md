---
id: random-operators
title: Random assignment operators
layout: docs
permalink: /docs/random-operators.html
prev: how-planout-works.html
next: logging.html
---

PlanOut comes built in with a few built-in random assignment operators (or
  random operators, for short).
As described in the [how PlanOut works page](how-planout-works.html),
random operators require that users specify a `unit`, and can optionally take a
salt as an argument.  The documentation below reviews additional required and
optional arguments for each of the built-in random operators.

### UniformChoice
`UniformChoice` selects among multiple choices with uniform probability.
It has one required argument `choices`.

```python
params.x = UniformChoice(choices=['a', 'b'], unit=userid)
params.y = UniformChoice(choices=['a', 'b', 'c'], unit=userid)
```

In the code above, `x` will take on the values 'a' and 'b' with a 1/2 chance
each, and `y` will take on the values 'a', 'b', and 'c' with a 1/3 chance each.

### WeightedChoice
`WeightedChoice` selects among multiple choices with a given set of weights.
It has two required arguments, `choices` and `weights`.

```python
params.x = WeightedChoice(choices=['a', 'b', 'c'], weights=[0.8, 0.1, 0.1],
  unit=userid)
params.y = WeightedChoice(choices=['a', 'b', 'c'], weights=[8, 1, 1],
  unit=userid)
```

Both `x` and `y` will take on the values 'a', 'b', and 'c' with a 80%, 10%, and
10% chance each. Because `x` and `y` have different salts, they will not
necessarily always have the same values for a given `userid`
(link to how-planout-works #salt section).

### BernoulliTrial
`WeightedChoice` flips a coin that lands on `1` with probability p, and `0`
with probability 1-p. It has one required argument, `p`.

```python
params.x = BernoulliTrial(p=0.0, unit=userid)
params.y = BernoulliTrial(p=0.2, unit=userid)
```

In the code above, `x` will always be `0`, and `y` will be `1` 20% of the time.

### RandomFloat
`RandomFloat` generates a random floating point number. 
It has two required arguments, `min` and `max`.

```python
params.x = RandomFloat(min=0.0, max=10.0), unit=userid)
```

### RandomInteger
`RandomInteger` generates a random integer between a min and max value, inclusive. 
It has two required arguments, `min` and `max`.

```python
params.x = RandomFloat(min=0, max=10), unit=userid)
```

### Sample
Sample samples from a list without replacement. It has one required parameter,
`choices`, and an optional parameter, `num_draws` (need to check this). If
`num_draws` is not specified, then Sample will simply shuffle the input array.
