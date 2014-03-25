from planout.interpreter import *
from planout.experiment import SimpleExperiment
import json

class SimpleInterpretedExperiment(SimpleExperiment):
  """Simple class for loading a file-based PlanOut interpreter experiment"""
  filename = None

  def assign(self, params, **kwargs):
    procedure = Interpreter(
      json.load(open(self.filename)),
      self.salt,
      kwargs
      )
    params.update(procedure.get_params())

class Exp1(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp1.json"

class Exp2(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp2.json"

class Exp3(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp3.json"

class Exp4(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp4.json"
