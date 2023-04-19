# -*- coding= UTF-8 -*-
import os, sys, json

class DbSelector(object):
    ''' This class makes the selection of json file 
        concerning the data base.
    '''
    def __init__(self, inputPath=os.path.dirname(os.path.realpath(__file__))+'/', inputName=sys.argv[1]):
        #print "\n"+inputName

        #self.input = json.loads(open(str(inputPath)+inputName).read())
        self.input = json.loads(open(inputName).read())

    def get_performance_in_db(self):
        databasePath=''
        tech = self.input["General_Modeling"]["power"]["technology_node"] + "nm"
        restrictions=self.input["DSE"]["Constraints"]
        model_name = self.input["General_Modeling"]["model_name"].replace(" ", "_")
        id_input = model_name + "_" + tech
        perf = ""
        try:
            bench = restrictions["benchmark"]
            app= restrictions["application"]

            list_itens_bd = json.loads(open(os.path.dirname(os.path.realpath(__file__))+'/db/'+bench+'/'+app+'/'+tech+'.json').read())
            
            for item_bd in list_itens_bd["ipcores"]:
                if item_bd["id"] == id_input:
                    perf = item_bd["perf"]
            
            return perf
        except KeyError:
            print "The DSE constraints must have key\n'technology'= xnm\n'benchmark'=benchmark_name\n'application'=application_name"

        
    #This method return a string with the full path of database choosen
    def select_db(self):
        databasePath=''
        restrictions=self.input["DSE"]["Constraints"]
        try:
            tech = restrictions["technology"]
            bench = restrictions["benchmark"]
            app= restrictions["application"]

            databasePath=os.path.dirname(os.path.realpath(__file__))+'/db/'+bench+'/'+app+'/'+tech+'.json'
            #print "path of db : "+databasePath
            return databasePath 
        except KeyError:
            print "The DSE constraints must have key\n'technology'= xnm\n'benchmark'=benchmark_name\n'application'=application_name"

if __name__=="__main__":
    Db = DbSelector()
    Db.select_db()
