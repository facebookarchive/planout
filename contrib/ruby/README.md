## Overview
This is a rough implementation of the Experiment / logging infrasture for running PlanOut experiments, with all the random assignment operators available in Python. This port is nearly a line-by-line port, and produces assignments that are completely consistent with those produced by the Python reference implementation.

## How it works

The following Ruby code:
```Ruby
class Exp < SimpleExperiment
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

(1..5).each do |i|
  my_exp = Exp.new(userid:i)
  #my_exp.auto_exposure_log = false
  # toggling the above disables or re-enables auto-logging
  puts "\n\nnew experiment time with userid %s!\n" % i
  puts "first time triggers a log event"
  puts 'my params are...', my_exp.get_params()
  puts 'second time...'
  puts 'my params are...', my_exp.get_params()
end
```

Produces something like this.

```
new experiment time with userid 1!
first time triggers a log event
{"name":"Exp","time":1404802228,"salt":"Exp","inputs":{"userid":1},"params":{"foo":"x","bar":"c","baz":6.123874064902064},"event":"exposure"}
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>6.123874064902064}
second time...
my params are...
{"foo"=>"x", "bar"=>"c", "baz"=>6.123874064902064}
```
