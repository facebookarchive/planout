# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from planout.experiment import SimpleExperiment
from planout.ops.random import *

class Exp1(SimpleExperiment):
  def assign(self, e, userid):
    e.group_size = UniformChoice(choices=[1, 10], unit=userid);
    e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
    if e.specific_goal:
      e.ratings_per_user_goal = UniformChoice(
        choices=[8, 16, 32, 64], unit=userid)
      e.ratings_goal = e.group_size * e.ratings_per_user_goal
    return e

class Exp2(SimpleExperiment):
  def assign(self, params, userid, pageid, liking_friends):
    params.num_cues = RandomInteger(
      min=1,
      max=min(len(liking_friends), 3),
      unit=[userid, pageid]
    )
    params.friends_shown = Sample(
      choices=liking_friends,
      draws=params.num_cues,
      unit=[userid, pageid]
    )

class Exp3(SimpleExperiment):
  def assign(self, e, userid):
    e.has_banner = BernoulliTrial(p=0.97, unit=userid)
    cond_probs = [0.5, 0.95]
    e.has_feed_stories = BernoulliTrial(p=cond_probs[e.has_banner], unit=userid)
    e.button_text = UniformChoice(
      choices=["I'm a voter", "I'm voting"], unit=userid)


class Exp4(SimpleExperiment):
  def assign(self, e, sourceid, storyid, viewerid):
    e.prob_collapse = RandomFloat(min=0.0, max=1.0, unit=sourceid)
    e.collapse = BernoulliTrial(p=e.prob_collapse, unit=[storyid, viewerid])
    return e
