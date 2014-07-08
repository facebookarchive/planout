## Overview
This is a rough implementation of the Experiment / logging infrasture for running PlanOut experiments, with all the random assignment operators available in Python. This port is nearly a line-by-line port, and produces assignments that are completely consistent with those produced by the Python reference implementation.

## How it works

This defines a simple experiment that randomly assigns three variables, foo, bar, and baz.
`foo` and `baz` use `userid` as input, while `bar` uses a pair, namely `userid` combined with the value of `foo` from the prior step.
```Ruby
class MyFirstExp < SimpleExperiment
  def assign(params, userid)
    params[:foo] = UniformChoice.new(
      unit: userid, choices: ['x', 'y'])
    params[:bar] = WeightedChoice.new(
      unit: [userid, params[:foo]],
      choices: ['a','b','c'],
      weights: [0.2, 0.5, 0.3])
    params[:baz] = RandomFloat.new(
      unit:userid, min: 5, max: 20)
  end
end
```

Then, we can examine the assignments produced for a few input userids. Note that since exposure logging is enabled by default, all of the experiments' inputs, configuration information, timestamp, and parameter assignments are pooped out via the Logger class.

```Ruby
class MyFirstExperiment < SimpleExperiment
  def assign(params, userid)
    params[:foo] = UniformChoice.new(
      choices: ['x', 'y'], unit: userid)
    params[:bar] = WeightedChoice.new(
      choices: ['a','b','c'],
      weights: [0.2, 0.5, 0.3],
      unit: [userid, params[:foo]])
    params[:baz] = RandomFloat.new(
      min: 5, max: 20, unit: userid)
  end
end
```

The output of the Ruby script looks something like this...

```
getting assignment for user 1 note: first time triggers a log event
logged data: {"name":"MyFirstExperiment","time":1404834015,"salt":"MyFirstExperiment","inputs":{"userid":1},"params":{"foo":"y","bar":"b","baz":6.545786477076732},"event":"exposure"}
my foo and baz are y and 6.55.

getting assignment for user 2 note: first time triggers a log event
logged data: {"name":"MyFirstExperiment","time":1404834015,"salt":"MyFirstExperiment","inputs":{"userid":2},"params":{"foo":"y","bar":"c","baz":18.514514154012573},"event":"exposure"}
my foo and baz are y and 18.51.
```
