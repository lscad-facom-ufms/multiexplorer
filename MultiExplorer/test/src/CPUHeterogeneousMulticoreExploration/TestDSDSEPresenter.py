import json
import os
import unittest
from matplotlib import pyplot

from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Presenters import DSDSEPresenter


DATA_PATH = os.path.dirname(os.path.abspath(__file__))+"/data"


class TestDSDSEPresenter(unittest.TestCase):
    def setUp(self):
        self.presenter = DSDSEPresenter()

    def testPlotPopulation(self):
        fig = self.presenter.plot_population(
            json.load(open(DATA_PATH+"/dsdse_presentable_results.json"))['solutions'],
            (76.70, 's^-1'),
            (0.97, 'W/mm^2')
        )

        dummy = pyplot.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = fig
        fig.set_canvas(new_manager.canvas)
        fig.savefig('data/plot')


if __name__ == '__main__':
    unittest.main()
