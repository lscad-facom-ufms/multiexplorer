# -*- coding: UTF-8 -*-
import json,csv

class JsonToCSV(object):
    
    def __init__(self, projectFolder, inputJSONResultPath="populationResults.json", outputCSVResultPath="populationResults.csv"):
        self.inputJSONResultPath = inputJSONResultPath
        self.outputCSVResultPath = outputCSVResultPath
        self.projectFolder = projectFolder
    def convertJSONToCSV(self):
        var = str(self.projectFolder)+"/"+self.inputJSONResultPath
        results_parsed = json.loads(open(var).read())
        var2 = str(self.projectFolder)+"/"+self.outputCSVResultPath
        csv_data = open(var2, 'w')
        csvWriter = csv.writer(csv_data)
        count = 0
        for collum in results_parsed:
            #print "collum:"
            #print collum
            if count == 0:
                #header = 'total_area', 'total_performance', 'performance_pred', 'total_power_density','id_ip_core', 'amount_ip_cores','performance ip', 'power ip', 'area_ip','amount_original_cores','performance_orig', 'power_orig', 'area orig'
		header = 'total_time', 'total_cost', 'time_pred', 'cost_pred', 'amount_original_vm', 'amount_sup_vm', 'id_sup_vm'
                csvWriter.writerow(header)
                count += 1
            result_data = results_parsed[collum]
            list = []
            list.append(result_data['Results']['total_time'])
            list.append(result_data['Results']['total_cost'])
            list.append(result_data['Results']['time_pred'])
            list.append(result_data['Results']['cost_pred'])
            list.append(result_data['amount_original_vm'])
            list.append(result_data['amount_sup_vm'])
            list.append(result_data['core_ip']['id'])
            #list.append(result_data['amount_ip_cores'])
           # list.append(result_data['core_ip']['perf'])
           # list.append(result_data['core_ip']['pow'])
            #list.append(result_data['core_ip']['area'])
            #list.append(result_data['amount_original_cores'])
            #list.append(result_data['performance_orig'])
            #list.append(result_data['power_orig'])
            #list.append(result_data['area_orig'])
            csvWriter.writerow(list)
        csv_data.close()
#            result_data = results_parsed[collum]


if __name__ == '__main__':
    obj = JsonToCSV()
    obj.convertJSONToCSV()
