# -*- coding: UTF-8 -*-
import json, os, sys
import csv
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from InOut import InOut
from DbSelector import DbSelector
from PerformancePredictor import PerformancePredictor

class DsDseBruteForce(object):

    """Main Class"""

    def __init__(self, projectFolder, pathCSV=sys.argv[1], path_db=DbSelector(inputName=sys.argv[1]).select_db()):
        
        self.inputDict= InOut(projectFolder).makeInputDict()
        self.db = json.loads(open(path_db).read())
        self.pathCSV=projectFolder+"/outputBruteForce.csv"
        self.first_solution = [] #plataformas que obedecem a restricao de area 
        self.final_solution = [] #plataformas que obedecem a restrição de area e tem performance maxima
        
        
        self.combinations()        
        self.printCSV()

    def combinations(self):
        combinationList=[]

        def is_viable(parameters):
            #power density and total área, are restrictions
            if parameters[1] <= self.inputDict["restrictions"]["total_area"] and parameters[0] <= self.inputDict["restrictions"]["power_density"]:
                return True
            else:
                return False


        for amount_orig_core in range(self.inputDict["parameters"]["amount_original_cores"][0], self.inputDict["parameters"]["amount_original_cores"][1]+1):
            for amount_ip_core in range(self.inputDict["parameters"]["amount_ip_cores"][0], self.inputDict["parameters"]["amount_ip_cores"][1]+1):
                for ip_core in self.db["ipcores"]:
                    parameters= self.calculateParameters(amount_orig_core, amount_ip_core, ip_core)
                    
                    processor = ip_core["id"]
                    #processor = ""
                    #if ip_core["id"] == "ARM_A53_22nm":
                    #    processor = "arm53"
                    #if ip_core["id"] == "ARM_A57_22nm":
                    #    processor = "arm57"
                    #if ip_core["id"] == "Atom_Silvermont_22nm":
                    #    processor = "atom"
                    #if ip_core["id"] == "Quark_x1000_32nm":
                    #    processor = "quark"
                    #if ip_core["id"] == "Smithfield_90nm":
                    #    processor = "smithfield"

                    performancePred = PerformancePredictor(processor, amount_ip_core, amount_orig_core).getResults()
                    _dict={"amount_orig_core":amount_orig_core, "amount_ip_core":amount_ip_core, "ip_core":ip_core,"powerDensity":parameters[0],"area":parameters[1], "performance":parameters[2], "performancePred":performancePred}
                    self.first_solution.append(_dict)    
                    if is_viable(parameters):
                        self.final_solution.append(_dict)

    def calculateParameters(self, amount_original, amount_ip, ip_core):
        origPower = self.inputDict["parameters"]["power_orig"][1]
        origArea = self.inputDict["parameters"]["area_orig"][1]
        origPerf = self.inputDict["parameters"]["performance_orig"][1]

        powerDensity= float(amount_original*origPower+amount_ip*ip_core["pow"])/float(amount_original*origArea+amount_ip*ip_core["area"])
        totalArea=(amount_original*origArea+amount_ip*ip_core["area"])
        totalPeformance= (amount_original*origPerf+amount_ip*ip_core["perf"])

        return (powerDensity, totalArea, totalPeformance)

    def printCSV(self):
        csvFile= open(self.pathCSV, "w")
        csvWriter= csv.writer(csvFile)

        header = 'total_area', 'total_performance', 'performance_pred','total_power_density','id_ip_core', 'amount_ip_cores','performance ip', 'power ip', 'area_ip','amount_original_cores','performance_orig', 'power_orig', 'area orig'
        csvWriter.writerow(header)

        for element in self.first_solution:
           #_dict={"amount_orig_core":amount_orig_core, "amount_ip_core":amount_ip_core, "ip_core":ip_core,"powerDensity":parameters[0],"area":parameters[1], "performance":parameters[2]}

            _list=[]
            _list.append(element["area"])
            _list.append(element["performance"])
            _list.append(element["performancePred"])
            _list.append(element["powerDensity"])
            _list.append(element["ip_core"]["id"])
            _list.append(element["amount_ip_core"])
            _list.append(element["ip_core"]["perf"])
            _list.append(element["ip_core"]["pow"])
            _list.append(element["ip_core"]["area"])
            _list.append(element["amount_orig_core"])
            _list.append(self.inputDict["parameters"]["performance_orig"][1])
            _list.append(self.inputDict["parameters"]["power_orig"][1])
            _list.append(self.inputDict["parameters"]["area_orig"][1])

            csvWriter.writerow(_list)
        csvFile.close()
if __name__ == "__main__":
    objDse = DsDseBruteForce()
