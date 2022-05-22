import joblib
import json
import os
import numpy as np
from sklearn import metrics
import pandas as pd
from metric import *

class PerformanceGPUPredictor(object):
    """Main Class"""
    
    def __init__(self,ipCoreName, amountIpCore,amountOriginCore,multiexplorerInput):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        input_file_app = open(dir_path+"/predictors/"+'bdGpuApp.json')
        input_file_model = open(dir_path+"/predictors/"+'bdGpuModel.json') #le o BD pelo primeira vez
        self.bdApp = json.load(input_file_app)
        self.bdModel = json.load(input_file_model)
        self.ipCoreName = ipCoreName
        self.originCoreName=multiexplorerInput["General_Modeling"]["model_name"]
        self.app =multiexplorerInput["Preferences"]["application"]
        self.amountIpCore = amountIpCore
        self.amountOriginCore=amountOriginCore       
        self.sharedMem= multiexplorerInput["General_Modeling"]["shmem_size"]
        self.blocks = multiexplorerInput["General_Modeling"]["blocks/SM"]
        self.regs = multiexplorerInput["General_Modeling"]["registers"]
        self.threads = multiexplorerInput["General_Modeling"]["threads/SM"]
        self.freq= multiexplorerInput["General_Modeling"]["clock_rate"]
        #print(self.processor)
        #print(self.amountCore)
        #instaciou todas as variaveis com valores validos
        # neg_mean_absolute_percentage_scorer = metrics.make_scorer(mean_absolute_percentage_error, greater_is_better=False)
        self.preditor = joblib.load(dir_path+"/predictors/"+'MLP.joblib')#carregou o preditor
        #print("oi")
        self.scaler = joblib.load(dir_path+"/predictors/"+'pipe.joblib')#carregou o escalador do conjunto de entrada
        #print "Pred + Escala: " + str(self.processor) + "\n"
    def logData(self,data):
        df = pd.DataFrame ([data], columns = ['Modelo', 'App', 'Shared_Mem', 'Blocks/SM', 'Number_Registers/core','Threads/SM', 'UC', 'Inst Kernel', '%Time_Kernel', 'Freq'])
        for col in set(df.columns) - set(['Modelo', 'App']):
            df['log_'+col] = np.log(df[col])
        df=self.scaler.transform(df)
        return df
    def getResults(self):#prediz o desempenho do core original
        originPred=self.getOriginalPerformance(self.originCoreName,self.bdModel,self.amountOriginCore,self.sharedMem,self.blocks, self.regs,self.threads, self.app, self.bdApp, self.freq)
     
        IPPred= self.getIPPerformance(self.amountIpCore, self.ipCoreName, self.bdModel,self.app,self.bdApp )
        
        

        finalResult= originPred[0]+ IPPred[0]
        return str(round(float(finalResult), 3))
    def getResultsNSGA(self, ipName, amountIP, amountOrig):#prediz o desempenho do core original
        originPred=self.getOriginalPerformance(self.originCoreName,self.bdModel,amountOrig,self.sharedMem,self.blocks, self.regs,self.threads, self.app, self.bdApp, self.freq)
     
        IPPred= self.getIPPerformance(amountIP, ipName, self.bdModel,self.app,self.bdApp )
        
        

        finalResult= originPred[0]+ IPPred[0]
        return str(round(float(finalResult), 3))


    def getOriginalPerformance(self, origCoreName,bdModel,ORI, sharedMem,blocks, regs, threads, app, bdApp, freq):
        freq= freq*1000000#chamada feita passando os 2 processadores

        teste= [bdModel[origCoreName]["name"],app,sharedMem, blocks,regs,threads,ORI,bdApp[app]["inst"],bdApp[app]["%TimeKernel"], freq ]
        teste = self.logData(teste)
        #y_pred = self.predictor().predict(teste)
        y_pred= self.preditor.predict(teste)
        y_pred = np.exp(y_pred)
        
        return y_pred,teste
        #return str(round(float(y_pred), 3))
    def getIPPerformance(self, ipcore, ipcoreName, bdModel, app, bdApp):
        freq= bdModel[ipcoreName]["clockRate"]*1000000
        teste=[bdModel[ipcoreName]["name"],app,bdModel[ipcoreName]["sharedMem"],bdModel[ipcoreName]["blocks"],bdModel[ipcoreName]['regs'],bdModel[ipcoreName]["threads"],ipcore, bdApp[app]["inst"],bdApp[app]["%TimeKernel"], freq  ]
        teste = self.logData(teste)
        #y_pred = self.predictor().predict(teste)
        y_pred= self.preditor.predict(teste)
        y_pred = np.exp(y_pred)

        return y_pred, teste
  
        
    if __name__ == "__main__":
        objPerformancePredictor = PerformancePredictor()
