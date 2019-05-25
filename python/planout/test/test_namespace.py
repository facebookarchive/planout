import unittest

from planout.namespace import SimpleNamespace
from planout.experiment import DefaultExperiment


class VanillaExperiment(DefaultExperiment):
    def setup(self):
        self.name = 'test_name'

    def assign(self, params, i):
        params.foo = 'bar'


class DefaultExperiment(DefaultExperiment):
    def get_default_params(self):
        return {'foo': 'default'}


class NamespaceTest(unittest.TestCase):
    def test_namespace_remove_experiment(self):
        class TestVanillaNamespace(SimpleNamespace):
            def setup(self):
                self.name = 'test_namespace'
                self.primary_unit = 'i'
                self.num_segments = 100
                self.default_experiment_class = DefaultExperiment

            def setup_experiments(self):
                self.add_experiment('test_name', VanillaExperiment, 100)
                self.remove_experiment('test_name')

        assert TestVanillaNamespace(i=1).get('foo') == 'default'

    def test_namespace_add_experiment(self):
        class TestVanillaNamespace(SimpleNamespace):
            def setup(self):
                self.name = 'test_namespace'
                self.primary_unit = 'i'
                self.num_segments = 100
                self.default_experiment_class = DefaultExperiment

            def setup_experiments(self):
                self.add_experiment('test_name', VanillaExperiment, 100)

        assert TestVanillaNamespace(i=1).get('foo') == 'bar'


if __name__ == '__main__':
    unittest.main()
