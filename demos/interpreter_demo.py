from planout.interpreter import *
from planout.experiment import SimpleExperiment
import json
import hashlib

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

  def checksum(self):
    # src doesn't count first line of code, which includes function name
    src = open(self.filename).read()
    return hashlib.sha1(src).hexdigest()[:8]

class Exp1(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp1.json"

class Exp2(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp2.json"

class Exp3(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp3.json"

class Exp4(SimpleInterpretedExperiment):
  filename = "sample_scripts/exp4.json"
