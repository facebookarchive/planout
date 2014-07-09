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

```
(155..156).each do |i|
  my_exp = VotingExperiment.new(userid:i)
  #my_exp.auto_exposure_log = false
  # toggling the above disables or re-enables auto-logging
  puts "\ngetting assignment for user %s note: first time triggers a log event" % i
  puts "button color is %s and button text is %s" %
    [my_exp.get(:button_color), my_exp.get(:button_text)]
end
```

The output of the Ruby script looks something like this...

```
getting assignment for user 155 note: first time triggers a log event
logged data: {"name":"VotingExperiment","time":1404894056,"salt":"VotingExperiment","inputs":{"userid":155},"params":{"button_color":"#00ff00","button_text":"I'm voting"},"event":"exposure"}
button color is #00ff00 and button text is I'm voting

getting assignment for user 156 note: first time triggers a log event
logged data: {"name":"VotingExperiment","time":1404894056,"salt":"VotingExperiment","inputs":{"userid":156},"params":{"button_color":"#00ff00","button_text":"I'm voting"},"event":"exposure"}
button color is #00ff00 and button text is I'm voting
my foo and baz are y and 18.51.
```
