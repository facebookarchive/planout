from pyplan import *

def exp1(userid):
  e = PlanOutExperiment('goal_setting')
  e.group_size = UniformChoice(choices=[1, 10], unit=userid);
  e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
  if e.specific_goal:
    e.ratings_per_user_goal = UniformChoice(choices=[8, 16, 32, 64], unit=userid)
    e.ratings_goal = e.group_size * e.ratings_per_user_goal
  return e


def exp2(userid, pageid, liking_friends):
  e = PlanOutExperiment('social_cues')
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


def exp3(userid):
  e = PlanOutExperiment('vote_2012')
  e.has_banner = BernoulliTrial(p=0.97, unit=userid)
  cond_probs = [0.5, 0.95]
  e.has_feed_stories = BernoulliTrial(p=cond_probs[e.has_banner], unit=userid)
  e.button_text = UniformChoice(
    choices=["I'm a voter", "I'm voting"], unit=userid)
  return e


def exp4(sourceid, storyid, viewerid):
  e = PlanOutExperiment('continuous_treatment')
  e.prob_collapse = RandomFloat(min=0.0, max=1.0, unit=sourceid)
  e.collapse = BernoulliTrial(p=e.prob_collapse, unit=[storyid, viewerid])
  return e

for u in xrange(1,4):
  for p in xrange(1, 4):
    print exp2(u, p, [1,2,3,4,5,6,7])


print [(e.group_size, e.ratings_goal) for e in map(exp1, xrange(0,100))]

for sourceid in xrange(1,5):
  e = exp4(sourceid, 1, 1)
  exps = [exp4(sourceid, 1, vid).collapse for vid in range(1, 20)]
  print e.prob_collapse, exps

print exp3(4).get_params()
