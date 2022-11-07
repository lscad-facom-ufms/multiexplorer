# -*- coding: UTF-8 -*-
import json
from typing import List
from JsonToCSV import JsonToCSV
from DbSelector import DbSelector
from PerformancePredictor import PerformancePredictor
from nsga2.Individual import Individual


class InOut(object):
    """ This class makes the interface between user entry and input of nsga, and also, makes the output of the nsga
    algorithm.
    """

    def __init__(self, settings):
        self.project_folder = settings['project_folder']

        self.mcpat_results = settings['mcpat_results']

        self.sniper_results = settings['sniper_results']

        self.output_file_name = None  # type: str # File name, without extension, for writing outputs

        self.dse_settings = settings['dse']

        self.input_dict = {}

        self.population = {}

    # método que imprime em um json e em uma planilha todos os indivíduos gerados no nsga
    def print_results(self, population):
        # type: (List[Individual]) -> None
        num = 0

        for individual in population:
            self.insert_in_result_population_dict(individual, num)

            num += 1

        self.write_results()

        JsonToCSV(
            self.project_folder,
            self.get_output_file_name() + ".json",
            self.get_output_file_name() + ".csv",
        ).convertJSONToCSV()

    def get_output_file_name(self):
        if self.output_file_name is None:
            return "population_results"

        return self.output_file_name.split(".")[0]

    # método responsável por criar um dicionário de saída, com as características dos indivíduos gerados pelo nsga
    def insert_in_result_population_dict(self, individual, num):
        # type: (Individual, int) -> None
        self.population[num] = {}
        # inserction of features
        self.population[num]["amount_original_cores"] = individual.features[0]
        self.population[num]["area_orig"] = individual.features[1]
        self.population[num]["power_orig"] = individual.features[2]
        self.population[num]["performance_orig"] = individual.features[3]
        self.population[num]["amount_ip_cores"] = individual.features[4]
        self.population[num]["core_ip"] = individual.features[5]

        # metrics
        self.population[num]["Results"] = {}
        # insertion of power_density and total_area
        self.population[num]["Results"]["total_power_density"] = (
            individual.features[2] * individual.features[0]
            + individual.features[5]["pow"] * individual.features[4]
        ) / (
            individual.features[1] * individual.features[0]
            + individual.features[5]["area"] * individual.features[4]
        )

        self.population[num]["Results"]["total_area"] = (
                individual.features[0] * individual.features[1]
                + individual.features[4] * individual.features[5]["area"]
        )

        self.population[num]["Results"]["total_performance"] = (
                individual.features[3] * individual.features[0]
                + individual.features[5]["perf"] * individual.features[4]
        )

        processor = individual.features[5]["id"]

        self.population[num]["Results"]["performance_pred"] = PerformancePredictor({
                'ip_processor': processor,
                'ip_core_nbr': individual.features[4],
                'orig_processor': self.dse_settings['processor'] + "_" + self.dse_settings['technology'],
                'orig_core_nbr': individual.features[0],
                'orig_frequency': self.dse_settings['frequency'],
        }).get_results()

    def write_results(self):
        json_file = open(self.get_output_json_file_path(), "w")

        json_file.write(json.dumps(self.population, indent=4, sort_keys=True))

        json_file.close()

    def get_output_json_file_path(self):
        return self.project_folder + "/" + self.get_output_file_name() + ".json"

    # faz o interfaceamento entre a Descrição de DSE passada pelo usuário, e o dicionário de entrada do algoritmo
    def make_input_dict(self):
        # Este método, ao final retornará um dicionário que será a entrada do nsga, como no modelo abaixo:
        #
        # {
        #    "parameters":{
        #        "amount_original_cores":[-,-],
        #        "area_orig":[-,-],
        #        "power_orig":[-,-],
        #        "performance_orig":[-,-],
        #        "amount_ip_cores":[-,-]
        #    },
        #    "restrictions":
        #    {
        #        "total_area":[-,-],
        #        "power_density":[-,-]
        #    }
        # }
        #
        # amount original cores --> é a quantidade de cores originais que serão explorador no nsga area_orig --> é o
        # tamanho de área do core original (este intervalo não vai variar, por exemplo se tivermos um processador com
        # 100mm2 de área, o intervalo será de [100, 100]) power_orig --> é a potência do core original
        # performance_orig --> é a performance do core original, obtida através de algum simulador de performance,
        # por exemplo, sniper ou multi2sim amount_ip_cores --> é a quantidade de cores ip, que serão acrescentados no
        # projeto (cores ip, são cores diferentes do original)
        parameters = {}

        restriction = {}

        min_orig_core = self.dse_settings['original_cores_for_design'][0]

        max_orig_core = self.dse_settings['original_cores_for_design'][1]

        parameters["amount_original_cores"] = [min_orig_core, max_orig_core]

        parameters["area_orig"] = [
            self.mcpat_results['processor']['area'][0],
            self.mcpat_results['processor']['area'][0]
        ]

        parameters["power_orig"] = [
            self.mcpat_results['processor']['peak_power'][0],
            self.mcpat_results['processor']['peak_power'][0]
        ]

        # performance = DbSelector.get_performance_in_db(
        #     model_name=self.dse_settings['processor'],
        #     bench=self.dse_settings['benchmark'],
        #     app=self.dse_settings['application'],
        #     tech=self.dse_settings['technology'],
        # )

        performance = self.dse_settings['original_performance'][0]

        parameters["performance_orig"] = [performance, performance]

        min_ip_core = self.dse_settings['ip_cores_for_design'][0]

        max_ip_core = self.dse_settings['ip_cores_for_design'][1]

        parameters["amount_ip_cores"] = [min_ip_core, max_ip_core]

        restriction["total_area"] = self.dse_settings['maximum_area']

        restriction["power_density"] = self.dse_settings['maximum_power_density']

        self.input_dict["parameters"] = parameters

        self.input_dict["restrictions"] = restriction

        return self.input_dict
