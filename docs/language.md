# The PlanOut Language
The PlanOut language is a way to concisely define experiments.
PlanOut language code is compiled into JSON.  The language is very basic: it contains basic logical operators, conditional execution, and arrays, but does not include things like loops and function definitions. This makes it easier to statically analyze experiments, and prevents users from shooting themselves in the foot. The syntax mostly resembles JavaScript.

All variables set by PlanOut code are passed back via `Interpreter.get_params()` and by default, are automatically logged when used in conjunction with `SimpleInterpretedExperiment`.

## Overview
* Lines are terminated with a `;`
* Arrays are defined like `[1,2,3]`, and are indexed starting at `0`.
* Random assignment operators (e.g., `uniformChoice`, `weightedChoice`, `bernoulliTrial`) require named parameters, and the ordering of parameter is arbitrary.
* `True` and `False` values are equivalent to `1` and `0`.
* `#`s are used to write comments
* You can use the `PlanOutLanguageInspector` class to validate whether all PlanOut operators use the required and optional methods.

## Compiling PlanOut code
PlanOut code can be compiled via the [Web-based compiler interface](http://facebook.github.io/planout/demo/planout-compiler.html) or using  the node.js script in the `compiler/` directory of the PlanOut github repository:

```
node compiler/planout.js planoutscriptname
```

## Built-in operators

### Random assignment operators
The operators described in [...] can be used similar to how they are used in Python, except are lower case. The variable named given on the left hand side of an assignment operation is used as the `salt' given random assignment operators if no salt is specified manually.

```
colors = ['#aa2200', '#22aa00', '#0022aa'];
x = uniformChoice(choices=colors, unit=userid); # 'x' used as salt
y = uniformChoice(choices=colors, unit=userid); # 'y' used as salt, generally != x
z = uniformChoice(choices=colors, unit=userid, salt='x'); # same value as x
```


### Array operators
Arrays can include constants and variables, and can be arbitrarily nested, and can contain arbitrary types.

```
a = [4, 5, 'foo'];
b = [a, 2, 3];      # evaluates to [[1,2,'foo'], 2,3]
x = a[0];           # evaluates to 4
y = b[0][2]         # evaluates to 'foo'
l = length(b);      # evaluates to 3
```

### Logical operators
Logical operators include *and* (`&&`), *or* (`||`), *not* (`!`), as in:

```
  a = 1; b = 0; c = 1;
  x = a && b;       # evaluates to False
  y = a || b || c;  # evaluates to True
  y = !b;           # evaluates to True
```

### Control flow
PlanOut supports if / else if / else.
```
if (country == 'US') {
  p = 0.2;
} else if (country == 'UK') {
  p = 0.4;
} else {
  p = 0.1;
}
```

### Arithmetic
Current arithmetic operators supported in the PlanOut language are: addition, subtraction, modulo, multiplication, and division.
```
 a = 2 + 3 + 4;  # 9
 b = 2 * 3 * 4;  # 24
 c = -2;         # -2
 d = 2 + 3 - 4;  # 1
 e = 4 % 2;      # 0
 f = 4 / 2;      # 2.0
```

### Other operators
Other operators that are part of the core language include `min` and `max`:
```
x = min(1, 2, -4);   # -4
y = min([1, 2, -4])  # -4
y = max(1, 2, -4)    # 2
```
