#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json
import re
import math

# Set path to Sniper
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '../../config.py')
from config import PATH_SNIPER

# Set path to the superclass SimulationTool and the path class tools at
# Sniper Simulator
sys.path.append(PATH_SNIPER+'/tools')
import sniper_lib
from SimulationTool import SimulationTool

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from createOutputMultiExplorer import outputConvert
import prepareMemory

# Set path to the output
SIM_OUT = os.getcwd()


class Sniper(SimulationTool):
    """
        This class makes the interface between MultiExplorer and Sniper
    """

    def __init__(self, jsonFile="input.json", benchmark="splash2-fft", path=PATH_SNIPER + "/benchmarks/", size="test", file_config="processor_config.cfg", directory_out=SIM_OUT, tool=" ", paramMap="param_map.txt", outJson="out.json"):
        super(Sniper, self).__init__(jsonFile, paramMap, outJson)
        self.path = path
        self.file_config = file_config
        self.dir_out = directory_out
        self.jsonFile = jsonFile
        # self.outputJson = None
        # read json file as object, and extracts the number of cores
        config = json.loads(open(jsonFile).read())
        self.processor = config["General_Modeling"]["total_cores"]
        #################################################################

        # set possible configuration, from the file
        if config["Preferences"]["sim_tool"] == "sniper":
            self.benchmark = config["Preferences"]["application"]
        else:
            self.benchmark = benchmark
        self.size_benchmark = size

        self.tool = tool

    # This method takes the results of simulations at Sniper and McPAT, then
    # return a json with all results
    def getResults(self):

        try:
            results = sniper_lib.get_results(resultsdir=self.dir_out)
            #jsonFile = open(self.dir_out + "FileResults.json", "w")
            #jsonFile.write(json.dumps(results, indent=4, sort_keys=True))
            #jsonFile.close()

            #MATHEUS######
            #adicionei estas linha pq aqui eu pego o tempo global da simulação e 
            #coloco em um arquivo com este valor da performanceFile
            #é necessário criar este arquivo pq o nsga usará este resultado para as 
            #otimizações.
            global_time_ns= results["results"]["barrier.global_time"][0]/1000000
            perf= 100000000000/global_time_ns
            performanceFile = open(self.dir_out+"/simplePerformanceValue", "w")
            performanceFile.write(str(6428))
            varSimulador = "\nSniper"
            performanceFile.write(varSimulador)
            performanceFile.close()
            ##############

            # After write in json, print its content .
            # print "------------------------------RESULTS------------------------------------"
            # pprint(results)

            #return open(self.dir_out + "FileResults.json")
        except IOError:
            print "can't open file, maybe path of directory, not found"

    # this method execute the comand line to sniper.
    def execute(self):
        print "*** Sniper Simulator ***"
        #if (self.processor>1):
        os.system(self.path + "./run-sniper -p " + self.benchmark + " -n " + str(self.processor) + " -i " +
                  self.size_benchmark + " -c " + PATH_SNIPER + "/config/" + self.file_config + " -d " + 
                  self.dir_out + self.tool + "> "+self.dir_out+ "/SniperPerformanceResults.txt")
        #else:
            #os.system(self.path + "./run-sniper -p " + self.benchmark + " -n 2 -i " +
                      #self.size_benchmark + " -c " + PATH_SNIPER + "/config/" + self.file_config + " -d " + self.dir_out + self.tool +
                      #"> "+self.dir_out+ "/SniperPerformanceResults.txt")
        
        self.getResults()
    # This method writes the resultString at a sniper file
    def writeFile(self, resultString):
        print resultString
        sniperFile = open(PATH_SNIPER + "/config/processor_config.cfg", "w")
        sniperFile.write("#include nehalem\n")
        sniperFile.write(resultString)

    def convertResults(self):
        self.outputJson = outputConvert()

    def createReport(self):
        lista = []
        # lendo todas as linhas de sim.out e colocando em texto
        arq = open(SIM_OUT + '/sim.out', 'r')
        textoCompleto = arq.read()
        texto = textoCompleto.split('\n')

        # verificando numero de cores
        linha = texto[0]
        listAux = re.split('\W+', linha)
        # pega o penultimo elemento da lista
        numberOfCores = int(listAux[-2]) + 1

        # print numberOfCores
        ####################################################
        resultString = ""

        OutME = open(SIM_OUT + '/SimulationOutput.txt', 'w')

        resultString += "\n*Performance Results\n"
        resultString += "[General]\n"

        # extraindo informacoes de tempo de simulacao
        linha = texto[4]
        listAux = re.split('\W+', linha)
        resultString += '\t' + 'SimulationTime(ns)= ' + str(listAux[3]) + '\n'

        # extraindo informacoes do total de instruncoes executadas
        linha = texto[1]
        listAux = re.split('\W+', linha)

        instructionExec = 0
        for i in range(2, 2 + numberOfCores):
            instructionExec += int(listAux[i])

        resultString += '\t' + 'Intructions= ' + str(instructionExec) + '\n'

        # Uma lista de Strings cada indice da lista tem uma string que
        # representa os parametros daquele core
        StringCores = []
        for i in range(0, numberOfCores):
            StringCores.append("")

            StringCores[i] += "\t[Core" + str(i) + "]\n"
            # predictionAccuracyRate
            linha = texto[10]
            listAux = re.split('\W{2,}|%', linha)
            # print listAux
            accuracy = 100.0 - float(listAux[2 + i])
            StringCores[i] += "\t\tPredictionAccuracyRate= " + \
                str(accuracy) + "\n"
            StringCores[i] += "\t\tMisPredictionRate= " + \
                str(listAux[2 + i]) + "\n"

            linha = texto[8]
            linha1 = texto[9]
            listAux = re.split('\W{3,}', linha)
            listAux1 = re.split('\W{3,}', linha1)
            StringCores[i] += "\t\tNumBranches= " + \
                str(int(listAux[1 + i]) + int(listAux1[1 + i])) + '\n'

            # Caches
            # analisa a expressao regular sobre todo o texto
            listAux = re.findall('Cache\sL\d.*\n.*\n.*\n.*\n', textoCompleto)
            for cache in listAux:
                linhas = cache.split('\n')
                # para cada linha eu especifico
                for linha in linhas:
                    listWords = re.split('\W{5,}|%', linha)
                    if len(listWords) == 2:
                        StringCores[i] += '\t\t' + \
                            str(listWords[0]) + str(listWords[1]) + '\n'
                    else:
                        # case it don't has type list ['']
                        if len(listWords) != 1:
                            StringCores[
                                i] += '\t\t' + str(listWords[0]) + '=' + str(listWords[i + 1]) + '\n'

                    # print listWords

        for i in range(0, numberOfCores):
            resultString += StringCores[i]

        # buscando num dram accesses
        listAux = re.findall('num dram accesses.*', textoCompleto)
        # separe a linha listAux[0] em varias colunas
        listWords = re.split('\W{3,}', listAux[0])
        numAcessDram = int(listWords[1])

        resultString += '[DRAM]\n'
        resultString += '\tNumAccesses =' + str(numAcessDram) + '\n'

        # print resultString
        OutME.write(resultString)
        OutME.close()
        arq.close()

    def parse(self):
        # open .json file as python object
        config = json.loads(open(self.jsonFile).read())
        resultString = ""

        modules = config["General_Modeling"]

        if modules.has_key("total_cores"):
            resultString += "[general]\n"
            resultString += "total_cores=" + \
                str(modules["total_cores"]).lower() + '\n\n'

        # parser in dicionary with key "core"
        if modules.has_key("core"):
            mod_core = modules["core"].items()
            resultString += "[perf_model/core]\n"

            for attributes in mod_core:
                if attributes[0] != "pipeline" and attributes[0] != "threads":
                    # if it is a parameter global_frequency, we should put
                    # "frequency"
                    if attributes[0] == "global_frequency":
                        resultString += "frequency=" + \
                            str(float(attributes[1]) / 1000) + '\n'
                    # if it is a list
                    elif isinstance(attributes[1], list):
                        if attributes[0] == "frequency":
                            resultString += attributes[0] + "[]="
                            resultString += (''.join(str(float(e) / 1000).lower() +
                                                     ',' for e in attributes[1]))[:-1] + '\n'
                        else:
                            resultString += attributes[0] + "[]="
                            resultString += (''.join(str(e).lower() +
                                                     ',' for e in attributes[1]))[:-1] + '\n'
                    # if it is a number
                    else:
                        resultString += attributes[0] + "="
                        resultString += str(attributes[1]) + '\n'

            resultString += '\n'

        # parser in dicionary with key "memory"
        if modules.has_key("memory"):
            perf_mod = modules["memory"]
            perf_mod = prepareMemory.prepareMemory(
                perf_mod, config["General_Modeling"]["total_cores"])
            # pprint(perf_mod)
            for mod in perf_mod:
                # print mod
                resultString += "[perf_model/" + str(mod) + "]\n"

                dic = perf_mod[mod]
                # This case, add attribute size=
                # int((sets*block_size*associativity)/1000)
                if str(mod) == "itlb" or str(mod) == "dtlb" or str(mod) == "stlb" or str(mod) == "tlb":
                    block_size = dic["block_size"]
                    associativity = dic["associativity"]
                    sets = dic["sets"]
                    penalty = dic["latency"]
                    resultString += "size[]=" + str(int(math.pow(2, int(math.log(
                        ((associativity * sets * block_size) / 1000), 2))))) + '\n'  # use log to approximate
                    resultString += "penalty=" + str(penalty) + '\n'

                dic = perf_mod[mod]
                for x in dic.items():
                    if isinstance(x[1], list):
                        resultString += str(x[0]) + '[]='
                        resultString += (''.join(str(e) +
                                                 ',' for e in x[1]))[:-1] + '\n'
                    else:
                        resultString += str(x[0]) + '=' + \
                            str(x[1]).lower() + '\n'
                resultString += '\n'
                # print '\n\nresultString:', resultString
        # parser in dictionary with key "network"
        if modules.has_key("network"):
            network = modules["network"].items()

            for n in network:
                if isinstance(n[1], dict):
                    resultString += '[network/' + n[0] + ']' + '\n'
                    # enter in type of network
                    for t in n[1].items():
                        resultString += t[0] + '=' + str(t[1]) + '\n'

                # if n[1] is a string
                else:
                    resultString += '[network]\n'
                    resultString += n[0] + '=' + n[1] + '\n'

            resultString += '\n'

        if modules.has_key("power"):
            power = modules["power"].items()

            resultString += "[power]\n"
            for p in power:
                resultString += p[0] + '=' + str(p[1]) + '\n'

        self.writeFile(resultString)

if __name__ == "__main__":

    obj = Sniper(sys.argv[1])
    obj.parse()
    obj.execute()
    obj.convertResults()
    obj.createReport()
    # obj.getResults()
