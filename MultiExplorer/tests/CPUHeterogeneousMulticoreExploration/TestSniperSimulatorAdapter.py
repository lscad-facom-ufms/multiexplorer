import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import SniperSimulatorAdapter


class TestSniperSimulatorAdapter(unittest.TestCase):

    def test_is_instantiable(self):
        simulator_adapter = SniperSimulatorAdapter()

        self.assertTrue(isinstance(simulator_adapter, SniperSimulatorAdapter))


if __name__ == '__main__':
    unittest.main()
