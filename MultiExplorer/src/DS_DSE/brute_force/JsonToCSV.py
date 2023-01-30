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
            if count == 0:           
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
            csvWriter.writerow(list)
        csv_data.close()



if __name__ == '__main__':
    obj = JsonToCSV()
    obj.convertJSONToCSV()
