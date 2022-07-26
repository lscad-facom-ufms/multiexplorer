import unittest

from MultiExplorer.test.src.CPUHeterogeneousMulticoreExploration.TestMcPATAdapter import TestMcPATAdapter


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMcPATAdapter)

    return suite
