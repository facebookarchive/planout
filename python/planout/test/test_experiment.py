# Copyright (c) 2014, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json
import unittest

from planout.experiment import Experiment, SimpleInterpretedExperiment, ProductionExperiment
from planout.interpreter import Interpreter
from planout.ops.random import UniformChoice

global_log = []


class ExperimentTest(unittest.TestCase):

    def experiment_tester(self, exp_class, in_experiment=True):
        global global_log
        global_log = []

        e = exp_class(i=42)
        e.set_overrides({'bar': 42})
        params = e.get_params()

        self.assertTrue('foo' in params)
        self.assertEqual(params['foo'], 'b')

        # test to make sure overrides work correctly
        self.assertEqual(params['bar'], 42)

        # log should only have one entry, and should contain i as an input
        # and foo and bar as parameters
        if in_experiment:
            self.assertEqual(len(global_log), 1)
            self.validate_log(params, {
                'inputs': {'i': None},
                'params': {'foo': None, 'bar': None}
            })
        else:
            self.assertEqual(len(global_log), 0)

        # test to make sure experiment eligibility works correctly
        self.assertEqual(e.in_experiment, in_experiment)

    def validate_log(self, blob, expected_fields):
        # Expected field is a dictionary containing all of the expected keys
        # in the expected structure. Key values are ignored.
        blob = global_log[0]
        for field in expected_fields:
            self.assertTrue(field in blob)
            if expected_fields[field] is dict:
                self.assertTrue(self.validate_log(
                    blob[field],
                    expected_fields[field]
                ))
            else:
                self.assertTrue(field in blob)

    def test_vanilla_experiment(self):
        class TestVanillaExperiment(Experiment):

            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)

        self.experiment_tester(TestVanillaExperiment)

    def test_vanilla_experiment_disabled(self):
        class TestVanillaExperiment(Experiment):

            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)
                return 0

        self.experiment_tester(TestVanillaExperiment, False)

    # makes sure assignment only happens once
    def test_single_assignment(self):
        class TestSingleAssignment(Experiment):

            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i, counter):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)
                counter['count'] = counter.get('count', 0) + 1

        assignment_count = {'count': 0}
        e = TestSingleAssignment(i=10, counter=assignment_count)
        self.assertEqual(assignment_count['count'], 0)
        e.get('foo')
        self.assertEqual(assignment_count['count'], 1)
        e.get('foo')
        self.assertEqual(assignment_count['count'], 1)

    def test_interpreted_experiment(self):
        class TestInterpretedExperiment(SimpleInterpretedExperiment):

            def log(self, stuff):
                global_log.append(stuff)

            def loadScript(self):
                self.script = json.loads("""
                  {"op":"seq",
                   "seq": [
                    {"op":"set",
                     "var":"foo",
                     "value":{
                       "choices":["a","b"],
                       "op":"uniformChoice",
                       "unit": {"op": "get", "var": "i"}
                       }
                    },
                    {"op":"set",
                     "var":"bar",
                     "value": 41
                    }
                   ]}
                """)

        self.experiment_tester(TestInterpretedExperiment)

    def test_disabled_interpreted_experiment(self):
        class TestInterpretedDisabled(SimpleInterpretedExperiment):
            def log(self, stuff):
                global_log.append(stuff)

            def loadScript(self):
                self.script = json.loads("""
                    {
                     "op": "seq",
                     "seq": [
                      {
                       "op": "set",
                       "var": "foo",
                       "value": "b"
                      },
                      {
                       "op": "return",
                       "value": false
                      }
                     ]
                    }
                    """)

        self.experiment_tester(TestInterpretedDisabled, False)

    def test_short_circuit_exposure_logging(self):
        class TestNoExposure(Experiment):

            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)
                return False
        self.experiment_tester(TestNoExposure, False)

        class TestNoExposure(Experiment):

            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)
                return True
        self.experiment_tester(TestNoExposure, True)

    def test_demo_production_experiment(self):
        class TestDemoProductionExperiment(ProductionExperiment):
            def configure_logger(self):
                pass

            def log(self, stuff):
                global_log.append(stuff)

            def previously_logged(self):
                pass

            def setup(self):
                self.name = 'test_name'

            def assign(self, params, i):
                params.foo = UniformChoice(choices=['a', 'b'], unit=i)

            def get_param_names(self):
                return ['foo']
        
        e = TestDemoProductionExperiment(i=42)
        self.assertEqual(e.get('nobar'), None)
        self.assertEqual(len(global_log), 0)
        self.assertEqual(e.get('foo'), 'b')
        self.assertEqual(len(global_log), 1)

if __name__ == '__main__':
    unittest.main()
