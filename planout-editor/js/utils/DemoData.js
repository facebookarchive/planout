/**
 * Copyright 2013-2014 Facebook, Inc.
 *
 * DemoData
 */

var PlanOutEditorConstants = require('../constants/PlanOutEditorConstants');
var TesterBoxTypes = PlanOutEditorConstants.TesterBoxTypes;

module.exports = {
  getDemoTests: function() {
    // this will eventually come from the server
    var defaultTests = [
      {
        "id": "playground",
        "inputs": {"userid": 42},
        "type": TesterBoxTypes.PLAYGROUND
      },
      {
        "id": "test3",
        "inputs":{"userid":5243},
        "overrides": {},
        "assertions": {"ratings_goal":640},
        "type": TesterBoxTypes.TEST
      },
      {
        "id": "test2",
        "inputs":{"userid":52433},
        "overrides": {"group_size":10},
        "assertions": {"ratings_goal": 200},
        "type": TesterBoxTypes.TEST
      },
    ];
    return defaultTests;
  },

  getDemoScript: function() {
    return [
     "group_size = uniformChoice(choices=[1, 10], unit=userid);",
     "specific_goal = bernoulliTrial(p=0.8, unit=userid);",
     "if (specific_goal) {",
     "  ratings_per_user_goal = uniformChoice(",
     "    choices=[8, 16, 32, 64], unit=userid);",
     "  ratings_goal = group_size * ratings_per_user_goal;",
     "}"
    ].join('\n');
  }
};
