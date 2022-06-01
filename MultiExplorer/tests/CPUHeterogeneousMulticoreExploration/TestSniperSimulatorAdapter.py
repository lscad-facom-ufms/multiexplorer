import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import SniperSimulatorAdapter


class TestSniperSimulatorAdapter(unittest.TestCase):

    def test_is_instantiable(self):
        simulator_adapter = SniperSimulatorAdapter()

        self.assertTrue(isinstance(simulator_adapter, SniperSimulatorAdapter))

    def set_values_from_file(self):
        simulator_adapter = SniperSimulatorAdapter()

        simulator_adapter.set_values_from_file("/home/ufms/projetos/multiexplorer/input-examples/quark.json")

if __name__ == '__main__':
    unittest.main()
