import DbSelector
from predictors.PerformancePredictor import\
    PerformancePredictor
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
        performance_predictor = PerformancePredictor(
            processor=self.settings['processor'],
            nbr_ip_cores=self.settings['nbr_ip_cores'],
            nbr_orig_cores=self.settings['nbr_orig_cores'],
        )

        dse_definitions = Definitions(performance_predictor)

        problem = DSDSE(dse_definitions, {
            'project_folder': self.settings['project_folder'],
            'bd_path': DbSelector.DbSelector.select_db(
                bench=self.settings['bench'],
                app=self.settings['app'],
                tech=self.settings['tech'],
            ),
        })

        evolution = Evolution(problem, 100, 10)

        evolution.register_on_new_generation(self.print_generation)

        pareto_front = evolution.evolve()

        output = InOut(self.settings)

        output.print_results(pareto_front)

    @staticmethod
    def print_generation(population, generation_num):
        if generation_num % 100 == 0:
            print("Generation: {}".format(generation_num))
