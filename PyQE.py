from logging import *
import PyPlanOut
import PlanOutExperiment

class PyQE:
  def __init__(self, exp, exp_name, logger=logging.info):
    self.exp = exp
    self.exp_name = exp_name
    self.logger = logger

  def __getattr__(self, name):
    logger.info(exp.get_params())
    return exp.name

e = PlanOutExperiment('first')
e.x = UniformChoice(values=[1,2,3], unit=1)
qe = PyQE(e)
print qe.x
