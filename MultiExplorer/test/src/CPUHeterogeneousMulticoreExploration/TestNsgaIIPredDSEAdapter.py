import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import NsgaIIPredDSEAdapter


class TestMcPATAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = NsgaIIPredDSEAdapter()

    def test_execute(self):
        self.adapter.inputs['exploration_space']['original_cores_for_design'] = (1, 25)

        self.adapter.inputs['exploration_space']['ip_cores_for_design'] = (1, 25)

        self.adapter.execute()


if __name__ == '__main__':
    unittest.main()
