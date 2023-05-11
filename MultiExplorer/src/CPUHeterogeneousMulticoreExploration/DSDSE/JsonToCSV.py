# -*- coding: UTF-8 -*-
import json,csv, sys
import operator;


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
                header = 'total_area', 'total_performance', 'total_power_density', 'id_ip_core', 'amount_ip_cores', 'performance ip', 'power ip', 'area_ip', 'amount_original_cores', 'performance_orig', 'power_orig', 'area orig'
                csvWriter.writerow(header)
                count += 1
            result_data = results_parsed[collum]
            list = []
            list.append(result_data['Results']['total_area'])
            list.append(result_data['Results']['total_performance'])
            list.append(result_data['Results']['total_power_density'])
            list.append(result_data['core_ip']['id'])
            list.append(result_data['amount_ip_cores'])
            list.append(result_data['core_ip']['perf'])
            list.append(result_data['core_ip']['pow'])
            list.append(result_data['core_ip']['area'])
            list.append(result_data['amount_original_cores'])
            list.append(result_data['performance_orig'])
            list.append(result_data['power_orig'])
            list.append(result_data['area_orig'])
            csvWriter.writerow(list)
        csv_data.close()
#            result_data = results_parsed[collum]

    def orderCSV(self):
        csvList = []
        bodyList = []

        orderedCsv_data = open("ordered.csv", 'w')
        orderedcsvWriter = csv.writer(orderedCsv_data)

        header = 'total_area', 'total_performance', 'total_power_density', 'id_ip_core', 'amount_ip_cores', 'performance ip', 'power ip', 'area_ip', 'amount_original_cores', 'performance_orig', 'power_orig', 'area orig'
        orderedcsvWriter.writerow(header)

        with open("populationResults.csv", 'r') as csvFile:
            readCSV = csv.reader(csvFile)
            cont = 0
            for row in readCSV:
                #print row
                # tem esse if cont pra nao pegar o cabecario do csv no body
                if cont == 0:
                    csvList.append(row)
                    cont += 1
                else:
                    csvList.append(row)
                    bodyList.append(row)
        #print "csvList"
        #print csvList 
        #print "sortedcsv"
        sortedcsv = sorted(bodyList, key=operator.itemgetter(1))
        for item in sortedcsv:
            orderedcsvWriter.writerow(item)
        orderedCsv_data.close()
        #print sortedcsv




if __name__ == '__main__':
    obj = JsonToCSV()
    obj.convertJSONToCSV()
    obj.orderCSV()