# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from planout.planoutkit import *
from planout.experiment import SimpleExperiment

class Exp1(SimpleExperiment):
  def assign(self, userid):
    e = PlanOutKitMapper(self.salt)
    e.group_size = UniformChoice(choices=[1, 10], unit=userid);
    e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
    if e.specific_goal:
      e.ratings_per_user_goal = UniformChoice(choices=[8, 16, 32, 64], unit=userid)
      e.ratings_goal = e.group_size * e.ratings_per_user_goal
    return e

class Exp2(SimpleExperiment):
  def assign(self, userid, pageid, liking_friends):
    e = PlanOutKitMapper(self.salt)
    e.num_cues = RandomInteger(
      min=1,
      max=min(len(liking_friends), 3),
      unit=[userid, pageid]
    )
    e.friends_shown = Sample(
      choices=liking_friends,
      draws=e.num_cues,
      unit=[userid, pageid]
    )
    return e

class Exp3(SimpleExperiment):
  def assign(self, userid):
    e = PlanOutKitMapper(self.salt)
    e.has_banner = BernoulliTrial(p=0.97, unit=userid)
    cond_probs = [0.5, 0.95]
    e.has_feed_stories = BernoulliTrial(p=cond_probs[e.has_banner], unit=userid)
    e.button_text = UniformChoice(
      choices=["I'm a voter", "I'm voting"], unit=userid)
    return e


class Exp4(SimpleExperiment):
  def assign(self, sourceid, storyid, viewerid):
    e = PlanOutKitMapper(self.salt)
    e.prob_collapse = RandomFloat(min=0.0, max=1.0, unit=sourceid)
    e.collapse = BernoulliTrial(p=e.prob_collapse, unit=[storyid, viewerid])
    return e

print \
  """ Demoing PlanOutKit implementations of experiments from
  'Designing and Deploying Online Field Experiments'\n"""

print 'Demoing experiment 1 decorator...'
print Exp1(userid=42)

print '\nDemoing experiment 1...'
exp1_runs = [Exp1(userid=i) for i in xrange(10)]
print [(e.get('group_size'), e.get('ratings_goal')) for e in exp1_runs]


print '\nDemoing experiment 2...'
# number of cues and selection of cues depends on userid and pageid
for u in xrange(1,4):
  for p in xrange(1, 4):
    print Exp2(userid=u, pageid=p, liking_friends=['a','b','c','d'])

print '\nDemoing experiment 3...'
for i in xrange(5):
  print Exp3(userid=i)

print '\nDemoing experiment 4...'
for i in xrange(5):
  # probability of collapsing is deterministic on sourceid
  e = Exp4(sourceid=i, storyid=1, viewerid=1)
  # whether or not the story is collapsed depends on the sourceid
  exps = [Exp4(sourceid=i, storyid=1, viewerid=v) for v in xrange(10)]
  print e.get('prob_collapse'), [exp.get('collapse') for exp in exps]
