# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from planout.interpreter import PlanOutInterpreterMapper


def runPlan(config, init, overrides={}):
  print '\n====== SETTING UP NEW EXPERIMENT ======'
  experiment = PlanOutInterpreterMapper(config)
  print 'using %s as input.' % init
  experiment.setEnv(init)
  if(overrides):
    print 'applying overrides: %s.' % overrides
    experiment.setOverrides(overrides)
  print 'validating experiment...'
  if experiment.validate():
    print 'success!'
    print '=== printing experiment in human ==='
    print experiment.pretty()
    print '=== experiment results ==='
    print experiment.getParams()
  else:
    print "experiment is invalid!"
    print "=== dump of broken experiment ==="
    print config


def demoInvalidPlanOut():
  # this code has one valid set randomFloat
  # one set that uses
  invalid_config = {"op":"seq",
  "seq": [
    {"op":"set", "var":"prob_show", "value":
      {"op":"randomFloat", "min":0.0,
        "unit":{"op": "get", "var": "userid"},
        "salt":"prob_show"}
    },
    {"op":"set",
     "var":"show_friend",
     "value": {
       "op":"bernoulliTrial",
       "p": {
         "op":"get",
         "var": "prob_show"},
       "unit": {
         "op":"array",
         "values": [{"op":"get", "var": "userid"}, {"op":"get", "var": "pageid"} ]},
       "salt":"show_friend",
       "bob":"2"
      }
    },
    {"op":"set",
     "var":"filtered_friends",
     "value": {
       "op": "bernoulliFilter",
       "p" : {"op":"get", "var": "prob_show"},
       "choices": [1,2,3,4,5,6,7,9],
       "unit": {"op":"get", "var":"userid"},
       "saltx": "show_friend"
      }
    }
  ]}
  print 'demoing invalid PlanOut code...'
  runPlan(invalid_config, {"userid": 5, "pageid": 9})

if __name__ == "__main__":
  valid_config = {"op":"seq",
  "seq": [
    {"op":"set", "var":"unit", "value": {"op": "get", "var": "userid"}},
    {"op":"set", "var":"prob_show", "value":
      {"op":"randomFloat", "min":0.0, "max":1.0,
        "unit":{"op": "get", "var": "userid"},
        "salt":"prob_show"}
    },
    {"op":"set",
     "var":"show_friend",
     "value": {
       "op":"bernoulliTrial",
       "p": {
         "op":"get",
         "var": "prob_show"},
       "unit": {
         "op":"array",
         "values": [{"op":"get", "var": "userid"}, {"op":"get", "var": "pageid"} ]},
       "salt":"show_friend",
      }
    },
    {"op":"set",
     "var":"filtered_friends",
     "value": {
       "op": "bernoulliFilter",
       "p" : {"op":"get", "var": "prob_show"},
       "choices": [1,2,3,4,5,6,7,9],
       "unit": {"op":"get", "var":"userid"},
       "salt": "show_friend"
      },
     },
     {"op":"set",
      "var":"friend_shown",
      "value": {"op": "equals", "left":{"op":"get", "var": "show_friend"}, "right":1}
      },
     {"op":"set",
      "var":"black_button",
      "value": {"op": "index", "base":[1,2,3], "index":1}
      }

  ]}

  demoInvalidPlanOut()
  runPlan(valid_config, {"userid": 21, "pageid": 9})
  runPlan(valid_config, {"userid": 21, "pageid": 9}, {'prob_show': 0.8})
  runPlan(valid_config, {"userid": 4, "pageid": 9}, {'prob_show': 0.8})

