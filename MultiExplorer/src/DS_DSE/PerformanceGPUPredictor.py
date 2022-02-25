import joblib
import json
import os


class PerformanceGPUPredictor(object):
    """Main Class"""

    def __init__(self,ipCoreName, amountIpCore,amountOriginCore,multiexplorerInput):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        input_file_app = open(dir_path+"/predictors/"+'bdGpuApp.json')
        input_file_model = open(dir_path+"/predictors/"+'bdGpuModel.json') #le o BD pelo primeira vez
        self.bdApp = json.load(input_file_app)
        self.bdModel = json.load(input_file_model)
        self.ipCoreName = ipCoreName
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
        self.preditor = joblib.load(dir_path+"/predictors/"+'model.joblib')#carregou o preditor
        #self.scalator = joblib.load(dir_path+"/predictors/"+'scaler.pkl')#carregou o escalador do conjunto de entrada
        #print "Pred + Escala: " + str(self.processor) + "\n"

    def getResults(self):#prediz o desempenho do core original
        #teste = [[ip, original,total,self.cpi,self.frequencyOriginal,float(1.0 - self.percent)]]
        y_pred=[[49152,8,65536,1024,1,774656,0.0309,700000000]]
        resp = self.preditor.predict(y_pred)
        file1 = open('predictorResults.txt', 'a')
        originPred=self.getOriginalPerformance(self.amountOriginCore,self.sharedMem,self.blocks, self.regs,self.threads, self.app, self.bdApp, self.freq)
        file1.write("originPred\n")
        file1.write("\n")
        file1.write(str(originPred[1]))
        file1.write("\n")
               
        file1.write(str(originPred[0]))
        file1.write("\n")
        IPPred= self.getIPPerformance(self.amountIpCore, self.ipCoreName, self.bdModel,self.app,self.bdApp )
        file1.write("IPPred\n")
        file1.write(str(IPPred[1]))
        file1.write("\n")
        file1.write(str(IPPred[0]))
        file1.write("\n")
        

        finalResult= originPred[0]+ IPPred[0]
        return str(round(float(finalResult), 3))
        #print("Valor preditooooooooo \n")
        #print(resp) #prediz desempenho core Original

        #pior desempenho sera retornado

    def getOriginalPerformance(self, ORI, sharedMem,blocks, regs, threads, app, bdApp, freq):
        freq= freq*1000000#chamada feita passando os 2 processadores
        teste= [[sharedMem, blocks,regs,threads,ORI,bdApp[app]["inst"],bdApp[app]["%TimeKernel"], freq ]]
        y_pred= self.preditor.predict(teste)
        
        return y_pred,teste
        #return str(round(float(y_pred), 3))
    def getIPPerformance(self, ipcore, ipcoreName, bdModel, app, bdApp):
        freq= bdModel[ipcoreName]["clockRate"]*1000000
        teste=[[bdModel[ipcoreName]["sharedMem"],bdModel[ipcoreName]["blocks"],bdModel[ipcoreName]['regs'],bdModel[ipcoreName]["threads"],ipcore, bdApp[app]["inst"],bdApp[app]["%TimeKernel"], freq  ]]
       
        y_pred= self.preditor.predict(teste)
        return y_pred, teste
        
    if __name__ == "__main__":
        objPerformancePredictor = PerformancePredictor()
