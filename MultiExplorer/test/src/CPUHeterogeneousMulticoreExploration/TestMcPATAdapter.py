import json
import unittest
import os
from xml.etree import ElementTree
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import McPATAdapter
from bs4 import BeautifulSoup


DATA_PATH = os.path.dirname(os.path.abspath(__file__))+"/data"


class TestMcPATAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = McPATAdapter()

        self.adapter.set_output_path(DATA_PATH)

    def test_generate_xml_from_sniper_simulation(self):
        self.adapter.generate_xml_from_sniper_simulation()

        self.adapter.write_input_xml_to_file()

        print(BeautifulSoup(ElementTree.tostring(self.adapter.input_xml.getroot(), encoding="utf8"), "xml").prettify())

    def test_register_results(self):
        self.adapter.register_results()

        # print json.dumps(self.adapter.results, indent=4, sort_keys=True)

        print json.dumps(self.adapter.presentable_results, indent=4, sort_keys=True)


if __name__ == '__main__':
    unittest.main()
