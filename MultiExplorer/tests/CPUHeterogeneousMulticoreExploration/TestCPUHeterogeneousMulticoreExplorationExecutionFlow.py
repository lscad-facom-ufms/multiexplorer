import unittest
from ...src.CPUHeterogeneousMulticoreExploration.CPUHeterogeneousMulticoreExplorationExecutionFlow \
    import CPUHeterogeneousMulticoreExplorationExecutionFlow


class TestCPUHeterogeneousMulticoreExplorationExecutionFlow(unittest.TestCase):

    def test_is_singleton(self):
        flow_a = CPUHeterogeneousMulticoreExplorationExecutionFlow()

        flow_b = CPUHeterogeneousMulticoreExplorationExecutionFlow()

        self.assertTrue(flow_a is flow_b)


if __name__ == '__main__':
    unittest.main()
