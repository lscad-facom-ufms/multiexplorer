import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Steps import CPUSimulationStep


class TestCPUSimulationStep(unittest.TestCase):

    def test_is_singleton(self):
        step_a = CPUSimulationStep()

        step_b = CPUSimulationStep()

        self.assertTrue(step_a is step_b)

    def test_has_inputs(self):
        step_c = CPUSimulationStep()

        inputs = step_c.get_inputs()

        self.assertTrue('Preferences' in inputs)

        self.assertTrue('General Modeling' in inputs)

        self.assertTrue('Design Space Exploration' in inputs)


if __name__ == '__main__':
    unittest.main()
