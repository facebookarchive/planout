import assignment_demo
import interpreter_demo

def demo_runner(exp_type):
  print '\nDemoing experiment 1...'
  exp1_runs = [exp_type.Exp1(userid=i) for i in xrange(10)]
  print [(e.get('group_size'), e.get('ratings_goal')) for e in exp1_runs]

  print '\nDemoing experiment 2...'
  # number of cues and selection of cues depends on userid and pageid
  for u in xrange(1,4):
    for p in xrange(1, 4):
      print exp_type.Exp2(userid=u, pageid=p, liking_friends=['a','b','c','d'])

  print '\nDemoing experiment 3...'
  for i in xrange(5):
    print exp_type.Exp3(userid=i)

  print '\nDemoing experiment 4...'
  for i in xrange(5):
    # probability of collapsing is deterministic on sourceid
    e = exp_type.Exp4(sourceid=i, storyid=1, viewerid=1)
    # whether or not the story is collapsed depends on the sourceid
    exps = [exp_type.Exp4(sourceid=i, storyid=1, viewerid=v) for v in xrange(10)]
    print e.get('prob_collapse'), [exp.get('collapse') for exp in exps]

demo_runner(assignment_demo)
demo_runner(interpreter_demo)
