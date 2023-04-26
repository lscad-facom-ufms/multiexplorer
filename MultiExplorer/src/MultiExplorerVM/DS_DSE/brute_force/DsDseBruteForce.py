# -*- coding: UTF-8 -*-
import json, os, sys
import csv

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../cloudsim/')

from InOutVM import InOut
from DbSelector import DbSelector
from PerformancePredictorVM import PerformancePredictor
from cloudsim.CloudSim import CloudSim
import math

cwd = os.getcwd()

class DsDseBruteForce(object):

    """Main Class"""

    def __init__(self, projectFolder, pathCSV=sys.argv[1], path_db=DbSelector(inputName=sys.argv[1]).select_db()):
        
        self.inputDict= InOut(projectFolder).makeInputDict()
        self.db = json.loads(open(path_db).read())
        self.pathCSV=projectFolder+"/outputBruteForce.csv"
        self.pathCSVfinal=projectFolder+"/outputBruteForcefinal.csv"
        self.first_solution = [] #plataformas que obedecem a restricao de area 
        self.final_solution = [] #plataformas que obedecem a restrição de area e tem performance maxima
        
        
        self.combinations()        
        self.printCSV()
        self.printCSVfinal()

    def combinations(self):
        combinationList=[]

        def is_viable(parameters):
            #total time and total cost, are restrictions

            if parameters[0] <= self.inputDict["restrictions"]["total_time"] and parameters[1] <= self.inputDict["restrictions"]["total_cost"]:
                return True
            else:
                return False


        for amount_orig_vm in range(self.inputDict["parameters"]["amount_original_vm"][0], self.inputDict["parameters"]["amount_original_vm"][1]+1):
            for amount_sup_vm in range(self.inputDict["parameters"]["amount_sup_vm"][0], self.inputDict["parameters"]["amount_sup_vm"][1]+1):
                print(amount_orig_vm, amount_sup_vm)
                for ip_core in self.db["ipcores"]:
                    
                    processor = ip_core["id"]

                    instructions = self.inputDict["parameters"]["instructions"]
                    corescloudlet = self.inputDict["parameters"]["corescloudlet"]

                    mips_orig = self.inputDict["parameters"]["mips"]
                    coresvm_orig = self.inputDict["parameters"]["coresVM"]
                    price_orig = self.inputDict["parameters"]["price_orig"]

                    mips_sup = ip_core["mips"]
                    coresvm_sup = ip_core["coresVM"]
                    price_sup = ip_core["price"]

                    cores_cloudlet_orig = int(round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm)))
                    cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig
                    

                    instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
                    instructions_sup = instructions - instructions_orig
                    
                    instructions_orig = int(instructions_orig/1000000)
                    instructions_sup = int(instructions_sup/1000000)
                    
                    # get time by CloudSim 
                    obj_orig = CloudSim(mips_orig, 10000, 512, coresvm_orig, int(cores_cloudlet_orig/amount_orig_vm), int(instructions_orig/amount_orig_vm))


                    #Time in hours
                    tempo = obj_orig.getTime()
                    time_vm_orig = float(tempo.replace(',','.'))/3600
                    if math.ceil(time_vm_orig) == 0:
                        cost_vm_orig = 1*price_orig*amount_orig_vm
                    else:
                        cost_vm_orig = math.ceil(time_vm_orig)*price_orig*amount_orig_vm
                        
                
                    obj_sup = CloudSim(mips_sup, 10000, 512, coresvm_sup, int(cores_cloudlet_sup/amount_sup_vm), int(instructions_sup/amount_sup_vm))


                    tempo = obj_sup.getTime()
                    time_vm_sup = float(tempo.replace(',','.'))/3600
                    

                    if math.ceil(time_vm_sup) == 0:
                        cost_vm_sup = 1*price_sup*amount_sup_vm
                    else:
                        cost_vm_sup = math.ceil(time_vm_sup)*price_sup*amount_sup_vm
                        
                    
                    if time_vm_orig > time_vm_sup:
                        totalTime = time_vm_orig
                    else:
                        totalTime = time_vm_sup

                    totalCost = cost_vm_orig + cost_vm_sup

                
                    
                    # Predictors
                    instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
                    instructions_sup = instructions - instructions_orig
                    time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600
                    time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600
                    
                    
                    if time_vm_orig > time_vm_sup:
                        timePred = time_vm_orig
                    else:
                        timePred = time_vm_sup
                        
                        
                    if math.ceil(time_vm_orig) == 0:
                        cost_vm_orig = 1*price_orig*amount_orig_vm
                    else:
                        cost_vm_orig = math.ceil(time_vm_orig)*price_orig*amount_orig_vm
                    
                    if math.ceil(time_vm_sup) == 0:
                        cost_vm_sup = 1*price_sup*amount_sup_vm
                    else:
                        cost_vm_sup = math.ceil(time_vm_sup)*price_sup*amount_sup_vm
                        
                    costPred = cost_vm_orig + cost_vm_sup


                    _dict={"amount_sup_vm":amount_sup_vm, "ip_core":ip_core, "time":totalTime,"cost":totalCost, "amount_orig_vm":amount_orig_vm, "time_pred": timePred, "cost_pred": costPred, "time_orig": time_vm_orig, "time_sup": time_vm_sup, "cost_orig":cost_vm_orig, "cost_sup":cost_vm_sup}
                    self.first_solution.append(_dict)    
                    if is_viable((totalTime, totalCost)):
                        self.final_solution.append(_dict)


    def printCSV(self):
        csvFile= open(self.pathCSV, "w")
        csvWriter= csv.writer(csvFile)

        header = 'total_time', 'total_cost', 'time_pred', 'cost_pred', 'id_sup_vm', 'amount_sup_vm', 'time_sup_vm', 'cost_sup_vm', 'amount_original_vm', 'time_original_vm', 'cost_original_vm'
        csvWriter.writerow(header)


        for element in self.first_solution:
                
            _list=[]
    
            _list.append(element["time"])
            _list.append(element["cost"])
            _list.append(element["time_pred"])
            _list.append(element["cost_pred"])
                
            _list.append(element["ip_core"]["id"])
            _list.append(element["amount_sup_vm"])
            _list.append(element["time_sup"])
            _list.append(element["cost_sup"])
            _list.append(element["amount_orig_vm"])
            _list.append(element["time_orig"])
            _list.append(element["cost_orig"])

            csvWriter.writerow(_list)
        csvFile.close()


    def printCSVfinal(self):
        csvFile= open(self.pathCSVfinal, "w")
        csvWriter= csv.writer(csvFile)

        header = 'total_time', 'total_cost', 'time_pred', 'cost_pred', 'id_sup_vm', 'amount_sup_vm', 'time_sup_vm', 'cost_sup_vm', 'amount_original_vm', 'time_original_vm', 'cost_original_vm'
        csvWriter.writerow(header)


        for element in self.final_solution:


            _list=[]
            _list.append(element["time"])
            _list.append(element["cost"])
            _list.append(element["time_pred"])
            _list.append(element["cost_pred"])

            _list.append(element["ip_core"]["id"])
            _list.append(element["amount_sup_vm"])
            _list.append(element["time_sup"])
            _list.append(element["cost_sup"])
            _list.append(element["amount_orig_vm"])
            _list.append(element["time_orig"])
            _list.append(element["cost_orig"])



            csvWriter.writerow(_list)
        csvFile.close()

if __name__ == "__main__":
    objDse = DsDseBruteForce()

