import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Steps import CPUSimulationStep


class TestCPUSimulationStep(unittest.TestCase):

    def test_is_singleton(self):
        step_a = CPUSimulationStep()

        step_b = CPUSimulationStep()

        self.assertTrue(step_a is step_b)


if __name__ == '__main__':
    unittest.main()
