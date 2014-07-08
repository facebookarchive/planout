## Overview
This is a rough implementation of the Experiment / logging infrasture for running PlanOut experiments, with all the random assignment operators available in Python. This port is nearly a line-by-line port, and produces assignments that are completely consistent with those produced by the Python reference implementation.

## How it works

This defines a simple experiment that randomly assigns three variables, foo, bar, and baz.
`foo` and `baz` use `userid` as input, while `bar` uses a pair, namely `userid` combined with the value of `foo` from the prior step.
```Ruby
class MyFirstExp < SimpleExperiment
  def assign(params, userid)
    params.set('foo', UniformChoice.new(
      unit: userid, choices: ['x', 'y']
    ))
    params.set('bar', WeightedChoice.new(
      unit: [userid, params.get('foo')],
      choices: ['a','b','c'],
      weights: [0.2, 0.5, 0.3])
    )
    params.set('baz', RandomFloat.new(
      unit:userid, min: 5, max: 20))
  end
end
```

Then, we can examine the assignments produced for a few input userids. Note that since exposure logging is enabled by default, all of the experiments' inputs, configuration information, timestamp, and parameter assignments are pooped out via the Logger class.

```Ruby
(1..5).each do |i|
  my_exp = MyFirstExp.new(userid:i)
  puts "\n\nnew experiment time with userid %s!\n" % i
  puts "first time triggers a log event"
  puts 'my params are...', my_exp.get_params()
  puts 'second time...'
  puts 'my params are...', my_exp.get_params()
end
```

The output of the Ruby script looks something like this...

```
new experiment time with userid 1!
first time triggers a log event
{"name":"MyFirstExp","time":1404830928,"salt":"MyFirstExp","inputs":{"userid":1},"params":{"foo":"x","bar":"c","baz":16.362308463262522},"event":"exposure"}
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>16.362308463262522}
second time...
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>16.362308463262522}


new experiment time with userid 2!
first time triggers a log event
{"name":"MyFirstExp","time":1404830928,"salt":"MyFirstExp","inputs":{"userid":2},"params":{"foo":"x","bar":"c","baz":16.637518156498846},"event":"exposure"}
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>16.637518156498846}
second time...
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>16.637518156498846}
```
