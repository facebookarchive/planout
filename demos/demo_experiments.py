import interpreter_experiment_examples as interpreter
import simple_experiment_examples as simple_experiment

def demo_experiment1(module):
  print 'using %s...' % module.__name__
  exp1_runs = [module.Exp1(userid=i) for i in xrange(10)]
  print [(e.get('group_size'), e.get('ratings_goal')) for e in exp1_runs]

def demo_experiment2(module):
  print 'using %s...' % module.__name__
  # number of cues and selection of cues depends on userid and pageid
  for u in xrange(1,4):
    for p in xrange(1, 4):
      print module.Exp2(userid=u, pageid=p, liking_friends=['a','b','c','d'])

def demo_experiment3(module):
  print 'using %s...' % module.__name__
  for i in xrange(5):
    print module.Exp3(userid=i)

def demo_experiment4(module):
  print 'using %s...' % module.__name__
  for i in xrange(5):
    # probability of collapsing is deterministic on sourceid
    e = module.Exp4(sourceid=i, storyid=1, viewerid=1)
    # whether or not the story is collapsed depends on the sourceid
    exps = [module.Exp4(sourceid=i, storyid=1, viewerid=v) for v in xrange(10)]
    print e.get('prob_collapse'), [exp.get('collapse') for exp in exps]

if __name__ == '__main__':
  # run each experiment implemented using SimpleExperiment (simple_experiment)
  # or using the interpreter
  print '\nDemoing experiment 1...'
  demo_experiment1(simple_experiment)
  demo_experiment1(interpreter)

  print '\nDemoing experiment 2...'
  demo_experiment2(simple_experiment)
  demo_experiment2(interpreter)

  print '\nDemoing experiment 3...'
  demo_experiment3(simple_experiment)
  demo_experiment3(interpreter)

  print '\nDemoing experiment 4...'
  demo_experiment4(simple_experiment)
  demo_experiment4(interpreter)
