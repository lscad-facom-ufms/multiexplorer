#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json
import re
import math
import shutil


from SimulationTool import SimulationTool
dir_path = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(dir_path + '../../config.py')
from config import GPU_PATH



CONFIGPATH=os.path.join(GPU_PATH+'/configs/tested-cfgs/')
print(CONFIGPATH)
# Set path to the output
SIM_OUT = os.getcwd()

BENCHPATH = "Benchmarks/"
class GPGPU(SimulationTool):
    """
        This class makes the interface between MultiExplorer and GPGPU-Sim
    """

    def __init__(self, jsonFile="input.json", app="clock",paramMap= "paramMap.json", directory_out=SIM_OUT, outJson=None):
        super(GPGPU, self).__init__(jsonFile, paramMap, outJson)
        self.jsonFile = jsonFile
        self.outJson = outJson
        with open(dir_path + '/' + paramMap) as data_file:
            self.paramMap = json.load(data_file)
        self.appConfig = os.path.join(dir_path+"/"+ "appconfig.json")
        self.config = json.load(open(self.jsonFile))
        self.app = self.config['Preferences']['application']
        self.geral = self.config['General_Modeling']
        self.outFile= self.createInputFolder(self.geral)
        try: 
            gpuConfigFolders= [f for f in os.listdir(CONFIGPATH)]
            self.gpuInputFolder = [x for x in gpuConfigFolders if x.endswith(self.geral["model_name"])][0]
        except:
             raise Exception("Model name not found")
        # self.outputJson = None
        # read json file as object, and extracts the number of cores
        
        #config = eval(config)
    
    """ def enviromentConfig(self):
        print("entrou aqui")
        os.chdir(GPU_PATH)
        print(os.getcwd())
        os.system("./run.sh") """
    def lineCheck(self,line):
        #print("entrou aqui")
        aux = line.split()
        #print(aux)
        paramDict= self.paramMap
        for param in paramDict.keys():
            inputValue= self.geral[paramDict[param]]
            if param == "gpgpu_clock_domains" and line.startswith("-"+ param):
                DRAMclock = (aux[1].split(":"))[3]
                line = aux[0]+ " "+str(inputValue)+".0:"+str(inputValue)+".0:"+str(inputValue)+".0:"+DRAMclock+"\n"
            elif param == "gpgpu_shader_core_pipeline" and line.startswith("-"+param):
                line = aux[0]+ " "+ str(inputValue)+":32\n"
            elif line.startswith("-"+param):
                line = aux[0]+ " "+ str(inputValue)+"\n"
        return line 

    def inputFolderName(self,params, path):
        if path == "": 
            DirName=path
        else : 
            DirName=path +"/"
        for i in params.keys():
            if i == "power":
                continue
            DirName = DirName+str(params[i])+"_"
        return DirName
    
    def createInputFolder(self,params):
        Inputpath ="Inputs"
        DirName= self.inputFolderName(params, "")
        #print(DirName)
        if not os.path.exists(DirName):
            os.makedirs(DirName)
        return DirName 

    def copyFiles(self, SrcDir, DestDir):
        SrcDir=CONFIGPATH + SrcDir
        SrcFiles=os.listdir(SrcDir)
        #print(SrcFiles)
        for fname in SrcFiles:
            if fname.endswith(".config"):
                continue
            else :
                shutil.copy2(os.path.join(SrcDir,fname), DestDir)
    def jsonToDict(self,JsonFile):
        with open(JsonFile) as json_file:
            data = json.load(json_file)
        return data

    def appArgs(self,app, jsonFile):
        Arg =""    
        jsonDict = self.jsonToDict(jsonFile)
        #print(JsonDict)
        try:
            if jsonDict[app]:
                Arg= app+ " "+ jsonDict[app]
                if app == "dwt2d": 
                    Arg = jsonDict[app]
                    
                
        except:
            Arg =  app
            #print(InputParams["app"])
        #print(Arg)
        return Arg

    def parse(self):
        
        dstFolder =os.path.join(SIM_OUT+"/"+ self.outFile+"/gpgpusim.config")
        print(dstFolder)           
        WF=open(dstFolder, 'w')
        RF=os.path.join(CONFIGPATH+self.gpuInputFolder+"/gpgpusim.config")
        
        with open(RF, 'r') as f:
            for line in f:
                #print(line)
                modifyLine=self.lineCheck(line)
                WF.write(modifyLine)
        
        self.copyFiles(self.gpuInputFolder, self.outFile) 
    #def parse():
        
    def execute(self):
        appArg= self.appArgs(self.app,self.appConfig )
        #print("./gpgpusim-new.sh Rundir " + self.outFile+" BFSOutput.txt BFSstderr.txt "+BENCHPATH+appArg)
        os.system("./gpgpusim-new.sh "+self.config['Preferences']['project_name']+" " + self.outFile+" BFSOutput.txt BFSstderr.txt "+BENCHPATH+appArg)

    def convertResults(self):
        print("Converte results")



if __name__ == "__main__":

    obj = GPGPU(sys.argv[1])
    #obj.lineCheck()
    obj.parse()
    obj.execute()
    obj.convertResults()
    obj.createReport()
    # obj.getResults()
