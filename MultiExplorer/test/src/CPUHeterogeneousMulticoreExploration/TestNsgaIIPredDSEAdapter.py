import unittest
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import NsgaIIPredDSEAdapter


class TestMcPATAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = NsgaIIPredDSEAdapter()

    def test_execute(self):
        self.adapter.execute()


if __name__ == '__main__':
    unittest.main()
