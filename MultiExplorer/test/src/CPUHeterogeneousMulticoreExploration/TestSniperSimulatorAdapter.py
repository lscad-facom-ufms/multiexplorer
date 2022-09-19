import json
import unittest
import os
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import SniperSimulatorAdapter
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.AllowedValues import PredictedCores


DATA_PATH = os.path.dirname(os.path.abspath(__file__))+"/data"


class TestSniperSimulatorAdapter(unittest.TestCase):
    def setUp(self):
        self.simulator_adapter = SniperSimulatorAdapter()

        self.simulator_adapter.set_output_path(DATA_PATH)

    def test_set_values_from_json(self):
        self.simulator_adapter.set_values_from_json(DATA_PATH+"/sniper_adapter_input.json")

        self.simulator_adapter.generate_cfg_from_inputs()

        expected_file_path = self.simulator_adapter.cfg_path

        with open(expected_file_path, 'r') as fin:
            print(fin.read())

    def test_generate_cfg_from_inputs(self):
        total_cores_value = 2

        self.simulator_adapter.inputs['general_modeling']['total_cores'] = total_cores_value

        self.simulator_adapter.generate_cfg_from_inputs()

        expected_file_path = self.simulator_adapter.cfg_path

        with open(expected_file_path, 'r') as fin:
            print(fin.read())

        cfg_file = open(expected_file_path)

        self.assertEqual("#include nehalem\n", cfg_file.readline())

        self.assertEqual("[general]\n", cfg_file.readline())

        self.assertEqual("total_cores="+str(total_cores_value)+"\n", cfg_file.readline())

    def test_get_user_inputs(self):
        user_inputs = self.simulator_adapter.get_user_inputs()

        self.assertEquals(
            user_inputs['general_modeling']['model_name'],
            self.simulator_adapter.inputs['general_modeling']['model_name']
        )

        user_inputs['general_modeling']['model_name'] = PredictedCores.Quark

        self.assertEqual(self.simulator_adapter.inputs['general_modeling']['model_name'], PredictedCores.Quark)

    def test_register_results(self):
        self.simulator_adapter.register_results()

        print json.dumps(self.simulator_adapter.presentable_results, indent=4)


if __name__ == '__main__':
    unittest.main()
