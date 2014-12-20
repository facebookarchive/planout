## Overview
This is a rough implementation of the Experiment / logging infrasture for running PlanOut experiments, with all the random assignment operators available in Python. This port is nearly a line-by-line port, and produces assignments that are completely consistent with those produced by the Python reference implementation.

## How it works

This defines a simple experiment that randomly assigns three variables, foo, bar, and baz.
`foo` and `baz` use `userid` as input, while `bar` uses a pair, namely `userid` combined with the value of `foo` from the prior step.
```Ruby
class VotingExperiment < SimpleExperiment
  # all assign() methods take params and an inputs array
  def assign(params, **inputs)
    userid = inputs[:userid]
    params[:button_color] = UniformChoice.new(
      choices: ['ff0000', '#00ff00'], unit: userid)
    params[:button_text] = UniformChoice.new(
      choices: ["I'm voting", "I'm a voter"], unit: userid, salt:'x')
  end
end
```

Then, we can examine the assignments produced for a few input userids. Note that since exposure logging is enabled by default, all of the experiments' inputs, configuration information, timestamp, and parameter assignments are pooped out via the Logger class.

```Ruby
my_exp = VotingExperiment.new(userid:14)
my_button_color = my_exp.get(:button_color)
button_text = my_exp.get(:button_text)
puts "button color is %s and button text is %s." % [my_button_color,button_text]
```

The output of the Ruby script looks something like this...

```
logged data: {"name":"VotingExperiment","time":1404944726,"salt":"VotingExperiment","inputs":{"userid":14},"params":{"button_color":"ff0000","button_text":"I'm a voter"},"event":"exposure"}

button color is ff0000 and button text is I'm a voter.
```

## Running the tests
Make sure you're in the ruby implementation directory of PlanOut and run `rake` or `rake test` to run the entire test suite.

If you wish to run a specific test, run `rake test TEST=test/testname.rb` or even better `ruby test/testname.rb`
