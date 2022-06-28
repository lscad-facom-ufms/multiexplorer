import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import SniperSimulatorAdapter
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.AllowedValues import PredictedCores
from MultiExplorer.src.config import PATH_RUNDIR


class TestSniperSimulatorAdapter(unittest.TestCase):
    def test_is_instantiable(self):
        simulator_adapter = SniperSimulatorAdapter()

        self.assertTrue(isinstance(simulator_adapter, SniperSimulatorAdapter))

    def test_set_values_from_file(self):
        simulator_adapter = SniperSimulatorAdapter()

        simulator_adapter.set_values_from_file("/home/ufms/projetos/multiexplorer/input-examples/quark.json")

    def test_set_values_from_json(self):
        simulator_adapter = SniperSimulatorAdapter()

        simulator_adapter.set_values_from_json("/home/ufms/projetos/multiexplorer/input-examples/quark.json")

    def test_generate_cfg_from_inputs(self):
        simulator_adapter = SniperSimulatorAdapter()

        simulator_adapter.output_path = "/home/ufms/projetos/multiexplorer/rundir"

        total_cores_value = 2
        simulator_adapter.inputs['general_modeling']['total_cores'] = total_cores_value

        simulator_adapter.generate_cfg_from_inputs()

        expected_file_path = simulator_adapter.cfg_path

        with open(expected_file_path, 'r') as fin:
            print(fin.read())

        cfg_file = open(expected_file_path)

        self.assertEqual("#include nehalem\n", cfg_file.readline())

        self.assertEqual("[general]\n", cfg_file.readline())

        self.assertEqual("total_cores="+str(total_cores_value)+"\n", cfg_file.readline())

    def test_get_user_inputs(self):
        simulator_adapter = SniperSimulatorAdapter()

        user_inputs = simulator_adapter.get_user_inputs()

        self.assertEquals(
            user_inputs['general_modeling']['model_name'],
            simulator_adapter.inputs['general_modeling']['model_name']
        )

        user_inputs['general_modeling']['model_name'] = PredictedCores.Quark

        self.assertEqual(simulator_adapter.inputs['general_modeling']['model_name'], PredictedCores.Quark)


if __name__ == '__main__':
    unittest.main()
