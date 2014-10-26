---
id: random-operators
title: Random assignment operators
layout: docs
permalink: /docs/random-operators.html
prev: how-planout-works.html
next: logging.html
---

PlanOut comes built in with several built-in random assignment operators that
map units to randomized values. All operators require
one to specify an input `unit`, and and optionally allow one to specify a salt.
For more details on how randomization works, see the [how PlanOut works](how-planout-works.html) page.

### UniformChoice
`UniformChoice` takes an argument `choices` and selects among these choices with uniform probability.

```python
params.x = UniformChoice(choices=['a', 'b'], unit=userid)
params.y = UniformChoice(choices=['a', 'b', 'c'], unit=userid)
```

In the code above, `x` will take on the values 'a' and 'b' a 1/2 probability each, and `y` will take on the values 'a', 'b', and 'c' with a 1/3 probability each.

### WeightedChoice
`WeightedChoice` selects among multiple choices (`choices`) with a given set of weights (`weights`).

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
`WeightedChoice` flips a coin that lands on `1` with probability `p`, and `0`
with probability 1-`p`.

```python
params.x = BernoulliTrial(p=0.0, unit=userid)
params.y = BernoulliTrial(p=0.2, unit=userid)
```

In the code above, `x` will always be `0`, and `y` will be `1` 20% of the time.

### RandomFloat
`RandomFloat` generates a random floating point number between `min` and `max`.

```python
params.x = RandomFloat(min=0.0, max=10.0), unit=userid)
```

### RandomInteger
`RandomInteger` generates a random integer between `min` and `max`, inclusive.

```python
params.x = RandomFloat(min=0, max=10), unit=userid)
```

### Sample
Sample samples from a list without replacement. It has one required parameter,
`choices`, and an optional parameter, `num_draws`. If
`num_draws` is not specified, then Sample will simply shuffle the input array.

```python
params.x = Sample(choices=['a','b','c'])
params.y = Sample(choices=['a','b','c'], num_draws=2)
```

In the code above, `x` will be a three element list, containing 'a', 'b', and
'c', exactly once, in a random order, and `y` be a two-element subset of
`['a','b', 'c']`.
