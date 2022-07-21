import unittest
from xml.etree import ElementTree

from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Adapters import McPATAdapter
from bs4 import BeautifulSoup


class TestMcPATAdapter(unittest.TestCase):
    def test_generate_xml_from_sniper_simulation(self):
        adapter = McPATAdapter()

        adapter.generate_xml_from_sniper_simulation()

        print(BeautifulSoup(ElementTree.tostring(adapter.input_xml, encoding="utf8"), "xml").prettify())


if __name__ == '__main__':
    unittest.main()
