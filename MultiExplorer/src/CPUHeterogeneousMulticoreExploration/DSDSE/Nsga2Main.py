import DbSelector
from PerformancePredictor import PerformancePredictor
from nsga2.Evolution import Evolution
from nsga2.problems.model_dse import DSDSE
from nsga2.problems.model_dse.Definitions import Definitions
from InOut import InOut
from typing import Dict


class Nsga2Main(object):
    """Main Class"""
    def __init__(self, settings=None):
        # type: (Dict) -> None
        self.settings = settings

    def run(self):
        performance_predictor = PerformancePredictor({
            "ip_core_nbr": self.settings['dse']['ip_cores_for_design'][1],
            "orig_processor": self.settings['dse']['processor'] + "_" + self.settings['dse']['technology'],
            "orig_core_nbr": self.settings['dse']['original_cores_for_design'][1],
            "orig_frequency": self.settings['dse']['frequency'],
        })

        dse_definitions = Definitions(performance_predictor)

        self.settings.update({
            'bd_path': DbSelector.DbSelector.select_db(
                bench=self.settings['dse']['benchmark'],
                app=self.settings['dse']['application'],
                tech=self.settings['dse']['technology'],
            )
        })

        problem = DSDSE(dse_definitions, self.settings)

        evolution = Evolution(problem, 100, 20, self.settings)

        evolution.register_on_new_generation(self.print_generation)

        pareto_front = evolution.evolve()

        output = InOut(self.settings)

        output.print_results(pareto_front)

    @staticmethod
    def print_generation(population, generation_num):
        if generation_num % 100 == 0:
            print("Generation: {}".format(generation_num))
