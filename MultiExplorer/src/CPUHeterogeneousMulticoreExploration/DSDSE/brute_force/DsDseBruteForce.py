# -*- coding: UTF-8 -*-
import csv
import json
import sys

from ..DbSelector import DbSelector
from ..InOut import InOut
from ..PerformancePredictor import PerformancePredictor


class DsDseBruteForce(object):
    """Main Class"""

    def __init__(self, settings):
        self.settings = settings

        self.input_dict = InOut(settings).make_input_dict()

        path_db = DbSelector.all_cores_path()

        self.db = json.loads(open(path_db).read())

        self.path_all_csv = settings['project_folder'] + "/brute_force_all_solutions.csv"

        self.path_viable_csv = settings['project_folder'] + "/brute_force_viable_solutions.csv"

        self.orig_processor = self.settings['dse']['processor'] + "_" + self.settings['dse']['technology']

        self.performance_predictor = PerformancePredictor({
            "ip_core_nbr": self.settings['dse']['ip_cores_for_design'][1],
            "orig_processor": self.orig_processor,
            "orig_core_nbr": self.settings['dse']['original_cores_for_design'][1],
            "orig_frequency": self.settings['dse']['frequency'],
        })  # type: PerformancePredictor

        self.all_solutions = None

        self.viable_solutions = None

    def run(self):
        self.all_solutions = []

        self.viable_solutions = []

        self.combinations()

        self.viable_solutions = sorted(self.viable_solutions, key=lambda d: d['performance_pred'], reverse=True)

        self.output_csv(self.path_all_csv)

        self.output_csv(self.path_viable_csv, True)

    def is_viable(self, parameters):
        # power density and total area, are restrictions
        if (
                parameters[1] <= self.input_dict["restrictions"]["total_area"]
                and parameters[0] <= self.input_dict["restrictions"]["power_density"]
        ):
            return True
        else:
            return False

    def combinations(self):
        for amount_orig_core in range(self.input_dict["parameters"]["amount_original_cores"][0],
                                      self.input_dict["parameters"]["amount_original_cores"][1] + 1):
            for amount_ip_core in range(self.input_dict["parameters"]["amount_ip_cores"][0],
                                        self.input_dict["parameters"]["amount_ip_cores"][1] + 1):
                for ip_core in self.db["ipcores"]:
                    parameters = self.calculate_parameters(amount_orig_core, amount_ip_core, ip_core)

                    ip_core_db_key = ip_core["id"]

                    self.performance_predictor.set_imported_processor(ip_core_db_key)

                    performance_pred = float(self.performance_predictor.get_results_l(amount_ip_core, amount_orig_core))

                    solution = {
                        "orig_processor": self.orig_processor,
                        "ip_processor": ip_core_db_key,
                        "amount_orig_core": amount_orig_core,
                        "amount_ip_core": amount_ip_core,
                        "ip_core": ip_core,
                        "power_density": parameters[0],
                        "area": parameters[1],
                        "performance": parameters[2],
                        "performance_pred": performance_pred
                    }

                    self.all_solutions.append(solution)

                    if self.is_viable(parameters):
                        self.viable_solutions.append(solution)

    def calculate_parameters(self, amount_original, amount_ip, ip_core):
        orig_power = float(self.input_dict["parameters"]["power_orig"][1])

        orig_area = float(self.input_dict["parameters"]["area_orig"][1])

        orig_perf = float(self.input_dict["parameters"]["performance_orig"][1])

        total_power = float(amount_original * orig_power + amount_ip * ip_core["pow"])

        total_area = float(amount_original * orig_area + amount_ip * ip_core["area"])

        power_density = float(total_power) / float(total_area)

        total_performance = float(amount_original * orig_perf + amount_ip * ip_core["perf"])

        return power_density, total_area, total_performance

    def output_csv(self, path, viable_only=False):
        csv_file = open(path, "w")

        csv_writer = csv.writer(csv_file)

        header = (
            'total_area', 'total_performance', 'performance_pred', 'total_power_density',
            'id_ip_core', 'amount_ip_cores', 'performance ip', 'power ip', 'area_ip',
            'id_orig_core', 'amount_original_cores', 'performance_orig', 'power_orig', 'area orig'
        )

        csv_writer.writerow(header)

        solutions = self.all_solutions

        if viable_only:
            solutions = self.viable_solutions

        for solution in solutions:
            csv_writer.writerow([
                str(round(solution["area"], 2)),
                str(round(solution["performance"], 2)),
                str(round(solution["performance_pred"], 2)),
                str(round(solution["power_density"], 2)),
                solution["ip_core"]["id"],
                solution["amount_ip_core"],
                solution["ip_core"]["perf"],
                solution["ip_core"]["pow"],
                solution["ip_core"]["area"],
                solution["orig_processor"],
                solution["amount_orig_core"],
                self.input_dict["parameters"]["performance_orig"][1],
                self.input_dict["parameters"]["power_orig"][1],
                self.input_dict["parameters"]["area_orig"][1]
            ])

        csv_file.close()
