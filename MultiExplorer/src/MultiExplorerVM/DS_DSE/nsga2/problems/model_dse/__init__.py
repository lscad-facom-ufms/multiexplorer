# -*- coding: UTF-8 -*-
"""Module with definition of DS_DSE problem interface"""
import sys, os, json, math
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../../')
from MultiExplorer.src.MultiExplorerVM.DS_DSE.nsga2.Individual import Individual
from MultiExplorer.src.MultiExplorerVM.DS_DSE.nsga2.problems import Problem
from MultiExplorer.src.MultiExplorerVM.DS_DSE.InOutVM import InOut
from MultiExplorer.src.MultiExplorerVM.DS_DSE.DbSelector import DbSelector
import random
import functools

class DS_DSE(Problem):
    """ Definition of DS_DSE problem"""
    def __init__(self, DSEDefinitions, projectFolder, path_db = DbSelector(inputName=sys.argv[1]).select_db()):
        inputNsga= InOut(projectFolder)
        self.dict_entry= inputNsga.makeInputDict()
        self.dse_definitions = DSEDefinitions
        self.max_objectives = [None, None, None]
        self.min_objectives = [None, None, None]
        self.problem_type = None
        self.bd=json.loads(open(path_db).read())
        self.restrictions= self.dict_entry["restrictions"]
        print "CONSTRAINTS"
        print '\t  Time (h): ', self.dict_entry["restrictions"]["total_time"]
        print '\t  Cost (USD): ', self.dict_entry["restrictions"]["total_cost"]


        self.n = 6 #numero de caracteristicas do Individuo (no DS_DSE sao 6 caracteristicas)


    #features[0] é "amount_original_cores"
    #features[1] é "area_orig"
    #features[2] é "power_orig"
    #features[3] é "performance_orig"
    #features[4] é "amount_ip_cores"
    #features[5] é "ipcore"


    #features[0] é "amount_original_vm"
    #features[1] é "amount_sup_vm"
    #features[2] é "instructions"
    #features[3] é "corescloudlet"
    #features[4] é "orig_vm"
    #features[5] é "ipcore"

  
    def __dominates(self, individual2, individual1):
	#print "INDIVIDUAL1", individual1.features[0], individual1.features[1], individual1.features[5]["id"]
	#print "INDIVIDUAL2", individual2.features[0], individual2.features[1], individual2.features[5]["id"]
        def calculateViolations(individual):
            cost_base= self.restrictions["total_cost"]
            time_base= self.restrictions["total_time"]
            individual.violations={"cost":0}
            individual.violations={"time":0}

            if self.dse_definitions.totalCost(individual)>cost_base:
                individual.violations["cost"]=  self.dse_definitions.totalCost(individual)- cost_base
            if self.dse_definitions.totalTime(individual)>time_base:
                individual.violations["time"]=  self.dse_definitions.totalTime(individual)- time_base
            return individual.violations

        individual1.violations= calculateViolations(individual1)
        individual2.violations= calculateViolations(individual2)

        individual1.viable= True
        individual2.viable= True

        for (key, value) in individual1.violations.items():
            if value!=0:
                individual1.viable= False
        for (key, value) in individual2.violations.items():
            if value!=0:
                individual2.viable= False

        if individual1.viable==True and individual2.viable== False:
            return True #True significa que o individuo 1 domina o 2
        elif  individual1.viable==False and individual2.viable== True:
            return False #individuo 1 não domina individuo 2

        #se os dois individuos não são viáveis
        elif  individual1.viable==False and individual2.viable== False:
            if self.dse_definitions.totalCost(individual1)<=self.dse_definitions.totalCost(individual2):
                return True
            if self.dse_definitions.totalCost(individual2)<self.dse_definitions.totalCost(individual1):
                return False

        # se os dois individuos são viaveis
        else:	
            pf1 = self.dse_definitions.totalTime(individual1)	
            pf2 = self.dse_definitions.totalTime(individual2)	
            worse_than_other = self.dse_definitions.totalCost(individual1) >= self.dse_definitions.totalCost(individual2) and pf1 >= pf2
            better_than_other = self.dse_definitions.totalCost(individual1) < self.dse_definitions.totalCost(individual2) or pf1 < pf2
            return worse_than_other and better_than_other


    def generateIndividual(self):
        individual = Individual()
        individual.features = []

        iterDict=self.dict_entry["parameters"]
        #########################
        #caracteristicas do individuos são 6, qtde de core originais, area deste core original, potencia deste core original
        #performance deste core original, qtde de cores ip, e o ip core que irá ser alocado no projeto
        # OBS: este ip core é buscado no banco
        #add amount
        value= random.randint(iterDict["amount_original_vm"][0], iterDict["amount_original_vm"][1])
        individual.features.append(value)
        #add_area
       # value= round(random.uniform(iterDict["time_orig"][0], iterDict["time_orig"][1]), 2)
       # individual.features.append(value)
        #add power orig
        #value= round(random.uniform(iterDict["cost_orig"][0], iterDict["cost_orig"][1]), 2)
       # individual.features.append(value)
        #add performance_orig
        #value= round(random.uniform(iterDict["performance_orig"][0], iterDict["performance_orig"][1]), 2)
        #individual.features.append(value)
        #add amount_ip_cores
        value= random.randint(iterDict["amount_sup_vm"][0], iterDict["amount_sup_vm"][1])
        individual.features.append(value)

        value= random.randint(iterDict["instructions"],iterDict["instructions"])
        individual.features.append(value)
        value= random.randint(iterDict["corescloudlet"],iterDict["corescloudlet"])
        individual.features.append(value)
	dic_orig_vm = {"mips":iterDict["mips"], "coresVM":iterDict["coresVM"], "price_orig":iterDict["price_orig"], "name":iterDict["model_name"]}
	#orig_vm = random.choice(dic_orig_vm)
        individual.features.append(dic_orig_vm)
        

        #add ip_core do banco
        ipcore= random.choice(self.bd["ipcores"])
	#print ipcore
	#print dic_orig_vm
        individual.features.append(ipcore)

        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        self.calculate_objectives(individual)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = []
        individual.objectives.append(self.dse_definitions.totalCost(individual))
        individual.objectives.append(self.dse_definitions.totalTime(individual))
        for i in range(2):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
