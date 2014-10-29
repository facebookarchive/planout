from planout.experiment import SimpleInterpretedExperiment
import json

class Exp1(SimpleInterpretedExperiment):
  def loadScript(self):
    self.script = json.loads(open("sample_scripts/exp1.json").read())

class Exp2(SimpleInterpretedExperiment):
  def loadScript(self):
    self.script = json.loads(open("sample_scripts/exp2.json").read())

class Exp3(SimpleInterpretedExperiment):
  def loadScript(self):
    self.script = json.loads(open("sample_scripts/exp3.json").read())

class Exp4(SimpleInterpretedExperiment):
  def loadScript(self):
    self.script = json.loads(open("sample_scripts/exp4.json").read())
