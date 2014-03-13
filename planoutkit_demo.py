from planoutkit import *

def exp1_manual(userid):
  e = PlanOutExperiment('goal_setting')
  e.group_size = UniformChoice(choices=[1, 10], unit=userid);
  e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
  if e.specific_goal:
    e.ratings_per_user_goal = UniformChoice(choices=[8, 16, 32, 64], unit=userid)
    e.ratings_goal = e.group_size * e.ratings_per_user_goal
  return e

@experiment('goal_setting')
def exp1(e, userid):
  e.group_size = UniformChoice(choices=[1, 10], unit=userid);
  e.specific_goal = BernoulliTrial(p=0.8, unit=userid);
  if e.specific_goal:
    e.ratings_per_user_goal = UniformChoice(choices=[8, 16, 32, 64], unit=userid)
    e.ratings_goal = e.group_size * e.ratings_per_user_goal
  return e

@experiment('social_cues_experiment')
def exp2(e, userid, pageid, liking_friends):
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

@experiment('vote_2012')
def exp3(e, userid):
  e.has_banner = BernoulliTrial(p=0.97, unit=userid)
  cond_probs = [0.5, 0.95]
  e.has_feed_stories = BernoulliTrial(p=cond_probs[e.has_banner], unit=userid)
  e.button_text = UniformChoice(
    choices=["I'm a voter", "I'm voting"], unit=userid)
  return e


@experiment('continuous_treatment')
def exp4(e, sourceid, storyid, viewerid):
  e.prob_collapse = RandomFloat(min=0.0, max=1.0, unit=sourceid)
  e.collapse = BernoulliTrial(p=e.prob_collapse, unit=[storyid, viewerid])
  return e


print \
  """ Demoing PlanOutKit implementations of experiments from
  'Designing and Deploying Online Field Experiments'\n"""

print 'Demoing experiment 1 without decorator...'
print exp1_manual(userid=42)
print 'Demoing experiment 1 decorator...'
print exp1(userid=42)

print '\nDemoing experiment 1...'
exp1_runs = [exp1(userid=i) for i in xrange(0,100)]
print [(e.group_size, e.ratings_goal) for e in exp1_runs]

print '\nDemoing experiment 2...'
# number of cues and selection of cues depends on userid and pageid
for u in xrange(1,4):
  for p in xrange(1, 4):
    print exp2(userid=u, pageid=p, liking_friends=['a','b','c','d'])

print '\nDemoing experiment 3...'
for i in xrange(5):
  print exp3(userid=i)

print '\nDemoing experiment 4...'
for i in xrange(5):
  # probability of collapsing is deterministic on sourceid
  e = exp4(sourceid=i, storyid=1, viewerid=1)
  # whether or not the story is collapsed depends on the sourceid
  exps = [exp4(sourceid=i, storyid=1, viewerid=v) for v in xrange(10)]
  print e.prob_collapse, [exp.collapse for exp in exps]
