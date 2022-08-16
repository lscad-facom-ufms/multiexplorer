import json
import unittest
from xml.etree import ElementTree
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import McPATAdapter
from bs4 import BeautifulSoup


class TestMcPATAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = McPATAdapter()

    def test_generate_xml_from_sniper_simulation(self):
        self.adapter.generate_xml_from_sniper_simulation()

        self.adapter.write_input_xml_to_file()

        print(BeautifulSoup(ElementTree.tostring(self.adapter.input_xml.getroot(), encoding="utf8"), "xml").prettify())

    def test_register_results(self):
        self.adapter.register_results()

        print json.dumps(self.adapter.results, indent=4, sort_keys=True)


if __name__ == '__main__':
    unittest.main()
