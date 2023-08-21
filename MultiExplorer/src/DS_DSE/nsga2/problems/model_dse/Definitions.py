# -*- coding: UTF-8 -*-
import math
from ....nsga2 import seq
from ...problems.ProblemDefinitions import ProblemDefinitions
from ....PerformancePredictor import PerformancePredictor

class Definitions(ProblemDefinitions):

    def __init__(self):
        self.n = 10
        self.performancePreditor = PerformancePredictor("ARM_A53_22nm", "1", "1")
        self.contador = 0

    #para
    #features[0] é "amount_original_cores"
    #features[1] é "area_orig"
    #features[2] é "power_orig"
    #features[3] é "performance_orig" 
    #features[4] é "amount_ip_cores"
    #features[5] é o ipcore, um dicionário {"id","pow","area","perf"}

    #objective
    def powerDensity(self, individual):
        total_power= individual.features[0]*individual.features[2] + individual.features[4]*individual.features[5]["pow"]
        total_area=individual.features[0]* individual.features[1] + individual.features[4]*individual.features[5]["area"]
        try:
            return total_power/total_area
        except Exception:
            print "Exception: Individual with zero parameters" + str(individual.features)
            return total_power/2

    def performance(self, individual):#performance com preditor
        performancePred = 0
        self.contador = self.contador + 1
        if(self.contador%10000 == 0):
            print("SVR Counter Performance: { " + str(self.contador) + " }\n")
        self.performancePreditor.setProcessor(individual.features[5]["id"])
        performancePred = float(self.performancePreditor.getResultsL(individual.features[4], individual.features[0]))
        performancePred = int(performancePred)
        return performancePred

    def performanceOld(self, individual):#performance ingenua
        self.contador = self.contador + 1
        if(self.contador%1000000 == 0):
            print("Counter Performance: { " + str(self.contador) + " }\n")
        #print "Gerou indivíduo com parâmetros" + str(individual.features)
            return (individual.features[3]*individual.features[0]+individual.features[5]["perf"]*individual.features[4])

    #restriction
    def totalArea(self, individual):
        return individual.features[0]* individual.features[1] + individual.features[4]*individual.features[5]["area"]
    def totalPower(self, individual):
        t_power= individual.features[0]*individual.features[2] + individual.features[4]*individual.features[5]["pow"]
        t_area=individual.features[0]* individual.features[1] + individual.features[4]*individual.features[5]["area"]
        return t_power/t_area

    def perfect_pareto_front(self):
        pass
