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

from PerformancePredictorVM import PerformancePredictor

import math
from decimal import Decimal


class InOut(object):
    """ This class makes the interface between user entry and input of nsga, and also, makes de output of algorithm nsga.
    """
    def __init__(self, projectFolder):

        self.projectFolder = projectFolder
        #self.inputPathForMCPATFile = str(projectFolder)+"/MCPATPhysicalResults.txt"        
        #self.inputPathForSNIPERFile = str(projectFolder)+"/simplePerformanceValue"
        self.outputPath = ""
        self.inputName = sys.argv[1]
        self.outputName = str(projectFolder)+"/populationResults.json"
        self.jsonFile = None
        self.objDict = {}
        self.inputDict = {}

        self.selector= DbSelector(self.inputName)
	
	self.menorTempo = 0
	self.menorCusto = 0
	self.tempo = 0
	self.custo = 0
	
	self.qntorig1 = 0
	self.qntsup1 = 0
	self.inst1 = 0
	self.cc1 = 0
	self.orig1 = 0
	self.sup1 = 0
	
	self.qntorig2 = 0
	self.qntsup2 = 0
	self.inst2 = 0
	self.cc2 = 0
	self.orig2 = 0
	self.sup2 = 0


    def totalTime(self, individual):
	amount_orig_vm = individual.features[0]
	amount_sup_vm = individual.features[1]

	instructions = individual.features[2]
	corescloudlet = individual.features[3]

	mips_orig = individual.features[4]["mips"]
	coresvm_orig = individual.features[4]["coresVM"]

	mips_sup = individual.features[5]["mips"]
	coresvm_sup = individual.features[5]["coresVM"]
	

	cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
	cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

	instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
	instructions_sup = instructions - instructions_orig

	time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600

	time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

	if time_vm_orig > time_vm_sup:
		totalTime = time_vm_orig
	else:
		totalTime = time_vm_sup

        return totalTime
    def totalCost(self, individual):
	amount_orig_vm = individual.features[0]
	amount_sup_vm = individual.features[1]

	instructions = individual.features[2]
	corescloudlet = individual.features[3]

	mips_orig = individual.features[4]["mips"]
	coresvm_orig = individual.features[4]["coresVM"]
	price_orig = individual.features[4]["price_orig"]

	mips_sup = individual.features[5]["mips"]
	coresvm_sup = individual.features[5]["coresVM"]
	price_sup = individual.features[5]["price"]
	

	cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
	cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

	instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
	instructions_sup = instructions - instructions_orig

	time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600
	if math.ceil(time_vm_orig) == 0:
		cost_vm_orig = 1*price_orig*amount_orig_vm
	else:
		cost_vm_orig = math.ceil(time_vm_orig)*price_orig*amount_orig_vm


	time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

	if math.ceil(time_vm_sup) == 0:
		cost_vm_sup = 1*price_sup*amount_sup_vm
	else:
		cost_vm_sup = math.ceil(time_vm_sup)*price_sup*amount_sup_vm

	totalCost = cost_vm_orig + cost_vm_sup

        return totalCost
        

    #método que imprime em um json e em uma planilha todos os indivíduos gerados no nsga
    def printResults(self, population):
        num = 0
        for individual in population:
            self.inserctInDict(individual, num)
            num = num+1
        self.writeResults()
        JsonToCSV(self.projectFolder).convertJSONToCSV()
	var2 = "/home/danillo/MultiExplorer/multiexplorer-develop/rundir/RESULTADOSSIMULACAO.csv"
        csv_data = open(var2, 'a')
        csvWriter = csv.writer(csv_data)
	result = str(self.menorTempo)
	list = []
	list.append(self.menorTempo)
	list.append(self.custo)
	list.append(self.qntorig1)
	list.append(self.orig1)
	list.append(self.qntsup1)
	list.append(self.sup1)
	list.append(self.inst1)
	list.append(self.cc1)
	
	csvWriter.writerow(list)
	
	list = []
	list.append(self.tempo)
	list.append(self.menorCusto)
	list.append(self.qntorig2)
	list.append(self.orig2)
	list.append(self.qntsup2)
	list.append(self.sup2)
	list.append(self.inst2)
	list.append(self.cc2)
	
	csvWriter.writerow(list)
	csv_data.close()
    
    #método responsável por criar um dicionário de saída, com as características dos indivíduos gerados pelo nsga 
    def inserctInDict(self, individual, num):
        self.objDict[num]={}
        #inserction of features
        self.objDict[num]["amount_original_vm"]= individual.features[0]
        self.objDict[num]["amount_sup_vm"]= individual.features[1]
        self.objDict[num]["instructions"]= individual.features[2]
        self.objDict[num]["corescloudlet"]= individual.features[3]
        self.objDict[num]["orig_vm"]= individual.features[4]
        self.objDict[num]["core_ip"]= individual.features[5]

        #metrics
        self.objDict[num]["Results"]={}
        #inserction of power_density and total_area
	time = self.totalTime(individual)
        self.objDict[num]["Results"]["total_time"]= time

	cost = self.totalCost(individual)
        self.objDict[num]["Results"]["total_cost"]= cost


	if self.menorTempo == 0:
		self.menorTempo = time
		self.custo = cost
		self.qntorig1 = individual.features[0]
		self.qntsup1 = individual.features[1]
		self.inst1 = individual.features[2]
		self.cc1 = individual.features[3]
		self.orig1 = individual.features[4]["name"]
		self.sup1 = individual.features[5]["id"]
	if self.menorTempo > time:
		self.menorTempo = time
		self.custo = cost
		self.qntorig1 = individual.features[0]
		self.qntsup1 = individual.features[1]
		self.inst1 = individual.features[2]
		self.cc1 = individual.features[3]
		self.orig1 = individual.features[4]["name"]
		self.sup1 = individual.features[5]["id"]
	if self.menorCusto == 0:
		self.menorCusto = cost
		self.tempo = time
		self.qntorig2 = individual.features[0]
		self.qntsup2 = individual.features[1]
		self.inst2 = individual.features[2]
		self.cc2 = individual.features[3]
		self.orig2 = individual.features[4]["name"]
		self.sup2 = individual.features[5]["id"]
	if self.menorCusto > cost:
		self.menorCusto = cost
		self.tempo = time
		self.qntorig2 = individual.features[0]
		self.qntsup2 = individual.features[1]
		self.inst2 = individual.features[2]
		self.cc2 = individual.features[3]
		self.orig2 = individual.features[4]["name"]
		self.sup2 = individual.features[5]["id"]
		

        
	processor = individual.features[5]["id"]
  
        


        #PerformancePredictor(individual.features[5]["id"], individual.features[4], individual.features[0])
        self.objDict[num]["Results"]["time_pred"] = 444
	#PerformancePredictor(processor, individual.features[4], individual.features[0]).getResults()
        self.objDict[num]["Results"]["cost_pred"] = 444


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

	    parameters["model_name"]=descriptionInput["General_Modeling"]["model_name"]
	    parameters["mips"]=descriptionInput["General_Modeling"]["mips"]
	    parameters["coresVM"]=descriptionInput["General_Modeling"]["coresVM"]
	    parameters["price_orig"]=descriptionInput["General_Modeling"]["price"]

	    
	    time_orig = 0
	    cost_orig = math.ceil(time_orig)*descriptionInput["General_Modeling"]["price"]
	    #print parameters["time_orig"], parameters["cost_orig"]

	    parameters["time_orig"]=[float(time_orig), float(time_orig)]
	    parameters["cost_orig"]=[float(cost_orig), float(cost_orig)]

	    parameters["instructions"]= descriptionInput["DSE"]["ExplorationSpace"]["instructions_for_design"]
	    parameters["corescloudlet"]= descriptionInput["DSE"]["ExplorationSpace"]["corescloudlet_for_design"]

            min_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["sup_vm_for_design"][0]
            max_ip_core=descriptionInput["DSE"]["ExplorationSpace"]["sup_vm_for_design"][1]
            parameters["amount_sup_vm"] = [min_ip_core , max_ip_core]


	    min_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_vm_for_design"][0]
            max_orig_core=descriptionInput["DSE"]["ExplorationSpace"]["original_vm_for_design"][1]
            parameters["amount_original_vm"] = [min_orig_core , max_orig_core]
	    

            restriction["total_cost"] = descriptionInput["DSE"]["Constraints"]["maximum_cost"]
            restriction["total_time"] = descriptionInput["DSE"]["Constraints"]["maximum_time"] #para o força bruta

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
