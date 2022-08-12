# -*- coding: UTF-8 -*-
"""Module with definition of DS_DSE problem interface"""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../../../')
from ...Individual import Individual
from ...problems import Problem
from ....InOut import InOut
import random
import functools


class DSDSE(Problem):
    """ Definition of DS_DSE problem"""

    def __init__(self, DSEDefinitions, settings):
        super(DSDSE, self).__init__()

        input_nsga = InOut(settings['project_folder'])

        self.dict_entry = input_nsga.make_input_dict()

        self.dse_definitions = DSEDefinitions

        self.max_objectives = [None, None, None]

        self.min_objectives = [None, None, None]

        self.problem_type = None

        self.bd = json.loads(open(settings['bd_path']).read())

        self.restrictions = self.dict_entry["restrictions"]

        print "CONSTRAINTS"

        print '\t Area : ', self.dict_entry["restrictions"]["total_area"]

        print '\t PowerDensity : ', self.dict_entry["restrictions"]["power_density"]

        print "\nOriginal Power Density : ", (float(self.dict_entry["parameters"]["power_orig"][0]) / float(
            self.dict_entry["parameters"]["area_orig"][0]))

        self.n = 6  # numero de caracteristicas do Individuo (no DSDSE sao 6 caracteristicas)

    # features[0] é "amount_original_cores"
    # features[1] é "area_orig"
    # features[2] é "power_orig"
    # features[3] é "performance_orig"
    # features[4] é "amount_ip_cores"
    # features[5] é "ipcore"
    def __dominates__(self, individual2, individual1):
        def calculate_violations(individual):
            area_base = self.restrictions["total_area"]
            densidade_de_referencia = self.restrictions["power_density"]
            individual.violations = {"area": 0}
            individual.violations = {"pow": 0}

            if self.dse_definitions.totalArea(individual) > area_base:
                individual.violations["area"] = self.dse_definitions.totalArea(individual) - area_base
            if self.dse_definitions.totalPower(individual) > densidade_de_referencia:
                individual.violations["pow"] = self.dse_definitions.totalPower(individual) - densidade_de_referencia
            return individual.violations

        individual1.violations = calculate_violations(individual1)
        individual2.violations = calculate_violations(individual2)

        individual1.viable = True
        individual2.viable = True

        for (key, value) in individual1.violations.items():
            if value != 0:
                individual1.viable = False
        for (key, value) in individual2.violations.items():
            if value != 0:
                individual2.viable = False

        if individual1.viable == True and individual2.viable == False:
            return True  # True significa que o individuo 1 domina o 2
        elif individual1.viable == False and individual2.viable == True:
            return False  # individuo 1 não domina individuo 2

        # se os dois individuos não são viáveis
        elif individual1.viable == False and individual2.viable == False:
            if self.dse_definitions.totalArea(individual1) <= self.dse_definitions.totalArea(individual2):
                return True
            if self.dse_definitions.totalArea(individual2) < self.dse_definitions.totalArea(individual1):
                return False
        # se os dois individuos são viaveis
        else:
            pf1 = self.dse_definitions.performance(individual1)
            pf2 = self.dse_definitions.performance(individual2)
            worse_than_other = self.dse_definitions.powerDensity(individual1) <= self.dse_definitions.powerDensity(
                individual2) and pf2 <= pf1
            better_than_other = self.dse_definitions.powerDensity(individual1) < self.dse_definitions.powerDensity(
                individual2) or pf2 < pf1
            return worse_than_other and better_than_other

    def generate_individual(self):
        individual = Individual()

        individual.features = []

        iterDict = self.dict_entry["parameters"]
        #########################
        # caracteristicas do individuos são 6, qtde de core originais, area deste core original, potencia deste core original
        # performance deste core original, qtde de cores ip, e o ip core que irá ser alocado no projeto
        # OBS: este ip core é buscado no banco
        # add amount
        value = random.randint(iterDict["amount_original_cores"][0], iterDict["amount_original_cores"][1])
        individual.features.append(value)
        # add_area
        value = round(random.uniform(iterDict["area_orig"][0], iterDict["area_orig"][1]), 2)
        individual.features.append(value)
        # add power orig
        value = round(random.uniform(iterDict["power_orig"][0], iterDict["power_orig"][1]), 2)
        individual.features.append(value)
        # add performance_orig
        value = round(random.uniform(iterDict["performance_orig"][0], iterDict["performance_orig"][1]), 2)
        individual.features.append(value)
        # add amount_ip_cores
        value = random.randint(iterDict["amount_ip_cores"][0], iterDict["amount_ip_cores"][1])
        individual.features.append(value)

        # add ip_core do banco
        ipcore = random.choice(self.bd["ipcores"])
        individual.features.append(ipcore)

        individual.dominates = functools.partial(self.__dominates__, individual1=individual)
        self.calculate_objectives(individual)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = []
        individual.objectives.append(self.dse_definitions.powerDensity(individual))
        individual.objectives.append(self.dse_definitions.performance(individual))
        for i in range(2):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
