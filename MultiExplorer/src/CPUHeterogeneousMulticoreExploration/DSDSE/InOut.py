# -*- coding: UTF-8 -*-
import sys
import json
import os
import csv
import re
from glob import glob
from datetime import datetime
from pprint import pprint
import shutil

from JsonToCSV import JsonToCSV
from DbSelector import DbSelector

from PerformancePredictor import PerformancePredictor

class InOut(object):
    """ This class makes the interface between user entry and input of nsga, and also, makes de output of algorithm nsga.
    """
    def __init__(self, projectFolder):

        self.projectFolder = projectFolder
        self.inputPathForMCPATFile = str(projectFolder)+"/MCPATPhysicalResults.txt"        
        self.inputPathForSNIPERFile = str(projectFolder)+"/simplePerformanceValue"
        self.outputPath = ""
        self.inputName = sys.argv[1]
        self.outputName = str(projectFolder)+"/populationResults.json"
        self.jsonFile = None
        self.objDict = {}
        self.inputDict = {}

        self.selector= DbSelector(self.inputName)
        

    #método que imprime em um json e em uma planilha todos os indivíduos gerados no nsga
    def printResults(self, population):
        num = 0
        for individual in population:
            self.inserctInDict(individual, num)
            num = num+1
        self.writeResults()
        JsonToCSV(self.projectFolder).convertJSONToCSV()
    
    #método responsável por criar um dicionário de saída, com as características dos indivíduos gerados pelo nsga 
    def inserctInDict(self, individual, num):
        self.objDict[num]={}
        #inserction of features
        self.objDict[num]["amount_original_cores"]= individual.features[0]
        self.objDict[num]["area_orig"]= individual.features[1]
        self.objDict[num]["power_orig"]= individual.features[2]
        self.objDict[num]["performance_orig"]= individual.features[3]
        self.objDict[num]["amount_ip_cores"]= individual.features[4]
        self.objDict[num]["core_ip"]= individual.features[5]

        #metrics
        self.objDict[num]["Results"]={}
        #inserction of power_density and total_area
        self.objDict[num]["Results"]["total_power_density"]= (individual.features[2]*individual.features[0]+individual.features[5]["pow"]*individual.features[4])/(individual.features[1]*individual.features[0]+individual.features[5]["area"]*individual.features[4])
        self.objDict[num]["Results"]["total_area"]= individual.features[0]*individual.features[1]+individual.features[4]*individual.features[5]["area"]
        self.objDict[num]["Results"]["total_performance"]= (individual.features[3]*individual.features[0]+individual.features[5]["perf"]*individual.features[4])
        
	processor = individual.features[5]["id"]
        #processor = ""
        #if individual.features[5]["id"] == "ARM_A53_22nm":
        #    processor = "arm53"
        #if individual.features[5]["id"] == "ARM_A57_22nm":
        #    processor = "arm57"
        #if individual.features[5]["id"] == "Atom_Silvermont_22nm":
        #    processor = "atom"
        #if individual.features[5]["id"] == "Quark_x1000_32nm":
        #    processor = "quark"
        #if individual.features[5]["id"] == "Smithfield_90nm":
        #    processor = "smithfield"
        

        # processor, amountIpCore, amountOriginalCore
        #PerformancePredictor(individual.features[5]["id"], individual.features[4], individual.features[0])
        self.objDict[num]["Results"]["performance_pred"] = PerformancePredictor(processor, individual.features[4], individual.features[0]).getResults()
        


    def writeResults(self):
        jsonFile = open(self.outputPath+self.outputName, "w")

        jsonFile.write(json.dumps(self.objDict, indent= 4, sort_keys=True))
        jsonFile.close()
    
    #método responsável por extrair resultados de simulação uteis do desempenho como
    #power density
    #area core
    #peak dynamic
    #core amount
    def readInputFromMcpat(self):
        mcpatDict = {}
        contArea = 0
        contPeakDynamic = 0
        contSubthresholdLeakage= 0
        contGateLeakage= 0
        linesMCPATFile = []

        with open(self.inputPathForMCPATFile) as inFile:
            for line in inFile:
                linesMCPATFile.append(line)

        for line in linesMCPATFile:
            if '*Power Density' in line:
                power_density_orig = line.split()[3]
               
            if 'Total Cores' in line:
                amount_original_cores = line.split()[2]

            if 'Core:' in line:
                area_orig = linesMCPATFile[linesMCPATFile.index(line)+1].split()[2]
                peak_dynamic = linesMCPATFile[linesMCPATFile.index(line)+2].split()[3]
                subthreshold_leakage = linesMCPATFile[linesMCPATFile.index(line)+3].split()[3]
                gate_leakage = linesMCPATFile[linesMCPATFile.index(line)+5].split()[3]


        mcpatDict["power_density_orig"] = round(float(power_density_orig), 3)
        mcpatDict["amount_original_cores"] = int(amount_original_cores)
        mcpatDict["area_orig"] = float(area_orig)
        mcpatDict["power_orig"] = round(float(peak_dynamic )+float(subthreshold_leakage)+float(gate_leakage), 3)
        mcpatDict["power_density_orig"] = round(float(0.0475), 3)
        # #mcpatDict["amount_original_cores"] = int(amount_original_cores)
        # mcpatDict["amount_original_cores"] = 2
        #mcpatDict["area_orig"] = 9.32
        # mcpatDict["power_orig"] = 26.9923 + 6.39321 + 0.398515
        #mcpatDict["power_orig"] = 8.91
        return mcpatDict

        # with open(self.inputPathForMCPATFile) as inFile:
        #     for line in inFile:
        #         if '*Power Density' in line:
        #             aux = line.split()
        #             power_density_orig = aux[3]
        #         if 'Total Cores' in line:
        #             aux = line.split()
        #             amount_original_cores = aux[2]
        #         if 'Area' in line:
        #             contArea += 1
        #             if contArea == 2:
        #                 aux = line.split()
        #                 area_orig = aux[2]
        #         if 'Peak Dynamic' in line:
        #             contPeakDynamic += 1
        #             if contPeakDynamic == 5:
        #                 aux = line.split()
        #                 PeakDynamic = aux[3]
        #         if 'Subthreshold Leakage' in line:
        #             contSubthresholdLeakage += 1
        #             if contSubthresholdLeakage == 9:
        #                 aux = line.split()
        #                 SubthresholdLeakage = aux[3]
        #         if 'Gate Leakage' in line:
        #             contGateLeakage +=1
        #             if contGateLeakage ==5:
        #                 aux = line.split()
        #                 gateLeakage= aux[3]        

        # mcpatDict["power_density_orig"] = round(float(power_density_orig), 2)
        # mcpatDict["amount_original_cores"] = int(amount_original_cores)
        # mcpatDict["area_orig"] = float((float(area_orig))/int(amount_original_cores))
        # mcpatDict["power_orig"] = float((float(PeakDynamic)+float(SubthresholdLeakage)+float(gateLeakage)))



        #return mcpatDict

    def readInputFromPerformanceSim(self):
        
        sniperDict = {}
        # performanceFile = open(self.inputPathForSNIPERFile, 'r')
        # performance = float(performanceFile.readline())
        # sniperDict["performance_orig"] = performance

        sniperDict["performance_orig"] = self.selector.get_performance_in_db()
        return sniperDict

    #faz o interfaceamento entre a Descrição de DSE passada pelo usuário, e o dicionário de entrada do algoritmo
    def makeInputDict(self):
        #Este método, ao final retornará um dicionário que será a entrada do nsga, como no modelo abaixo:
        #
        #{
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
        #}
        #
        #amount original cores --> é a quantidade de cores originais que serão explorador no nsga
        #area_orig --> é o tamanho de área do core original (este intervalo não vai variar, por exemplo se tivermos um processador com 100mm2 de área, o intervalo será de [100, 100])
        #power_orig --> é a potência do core original
        #performance_orig --> é a performance do core original, obtida através de algum simulador de performance, por exemplo, sniper ou multi2sim
        #amount_ip_cores --> é a quantidade de cores ip, que serão acrescentados no projeto (cores ip, são cores diferentes do original)
        def setDefault():
            print "-> default DSE input"
            parameters = {}
            restriction = {}

            mcpat = self.readInputFromMcpat()
            performanceSim = self.readInputFromPerformanceSim()

            parameters["amount_original_cores"] = [1 , mcpat["amount_original_cores"]]
            parameters["area_orig"] = [mcpat["area_orig"], mcpat["area_orig"]]
            parameters["power_orig"] = [mcpat["power_orig"], mcpat["power_orig"]]
            parameters["performance_orig"] = [performanceSim["performance_orig"], performanceSim["performance_orig"]]
            parameters["amount_ip_cores"] = [int(mcpat["amount_original_cores"])/2, int(mcpat["amount_original_cores"])*2]

            restriction["total_area"] = float(mcpat["area_orig"])*float(mcpat["amount_original_cores"])
            restriction["power_density"] = float(mcpat["power_orig"])/float(mcpat["area_orig"])  #para o força bruta

            self.inputDict["parameters"] = parameters
            self.inputDict["restrictions"] = restriction

            return self.inputDict

        def setInputDict(descriptionInput):
            parameters = {}
            restriction = {}

            mcpat = self.readInputFromMcpat()
            performanceSim = self.readInputFromPerformanceSim()

            min_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_cores_for_design"][0]
            max_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_cores_for_design"][1]
            parameters["amount_original_cores"] = [min_orig_core , max_orig_core]

            parameters["area_orig"] = [mcpat["area_orig"], mcpat["area_orig"]]
            parameters["power_orig"] = [mcpat["power_orig"], mcpat["power_orig"]]

            parameters["performance_orig"] = [performanceSim["performance_orig"], performanceSim["performance_orig"]]
            min_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["ip_cores_for_design"][0]
            max_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["ip_cores_for_design"][1]
            parameters["amount_ip_cores"] = [min_ip_core , max_ip_core]

            restriction["total_area"] = descriptionInput["DSE"]["Constraints"]["maximum_area"]
            restriction["power_density"] = descriptionInput["DSE"]["Constraints"]["maximum_powerDensity"] #para o força bruta

            self.inputDict["parameters"] = parameters
            self.inputDict["restrictions"] = restriction

            return self.inputDict

        descriptionInput = json.loads(open(self.inputName).read())
        #verificar se tem chave DSE, caso tenha, criar dicionário com o que o usuário passou no arquivo de entrada
        if descriptionInput.has_key("DSE"):
            return setInputDict(descriptionInput)
        #caso contrário, criar deicionário com os valores defaults(valores defaults são valores baseados apenas nas saídas de simulação de desempenho e física)
        else:
            return setDefault()

if __name__ == "__main__":
    
    obj = InOut()
    obj.readRangeFromIp()
    obj.readInputFromPerformanceSim()
    obj.readInputFromMcpat()
    obj.makeInputDict()
