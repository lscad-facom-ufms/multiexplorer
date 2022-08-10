from sklearn.externals import joblib
import json
import os


class PerformancePredictor(object):
    """Main Class"""

    def __init__(self, processor, amountIpCore, amountOriginalCore):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        input_file = open (dir_path+"/predictors/"+'bdPredictor.json') #le o BD pelo primeira vez
        self.bd = json.load(input_file)
        self.originalProcessor = "Smithfield_90nm"
        self.processor = processor
        self.frequencyOriginal = 2.8
        self.frequencyIP =  float(self.bd[str(processor)][0]["freq"])
        self.cpi = 0.6
        self.percent = 0.5
        self.amountIpCore = amountIpCore
        self.amountOriginalCore = amountOriginalCore
        #instaciou todas as variaveis com valores validos
        self.preditor = joblib.load(dir_path+"/predictors/"+'preditor.pkl')#carregou o preditor
        self.scalator = joblib.load(dir_path+"/predictors/"+'scaler.pkl')#carregou o escalador do conjunto de entrada
        #print "Pred + Escala: " + str(self.processor) + "\n"

    def setOrigiginal(self, original):
        self.originalProcessor = original
        self.frequencyOriginal = float(self.bd[str(original)][0]["freq"])

    def setProcessor(self, ip):
        self.processor = ip
        self.frequencyIP = float(self.bd[str(ip)][0]["freq"])

    def getResults(self):#chamada feita depois de setar os 2 processadores
        original = self.amountOriginalCore
        ip = self.amountIpCore
        ORI = self.amountOriginalCore
        IP = self.amountIpCore
        total = int(original)+int(ip)
        self.cpi = float(self.bd[str(self.processor)][0][str(IP)])
        self.percent = float((int(IP)*float(self.frequencyIP))/((int(IP)*float(self.frequencyIP))+(int(ORI)*float(self.frequencyOriginal))))#calculo da porcentagem
        teste = [[original,ip,total,self.cpi,self.frequencyOriginal,self.percent]]#monta o teste        
        testeS = self.scalator.transform(teste)#escalona os parametros
        resp = self.preditor.predict(testeS) #prediz desempenho core IP

        self.cpi = float(self.bd[str(self.originalProcessor)][0][str(original)])
        teste = [[ip, original,total,self.cpi,self.frequencyOriginal,float(1.0 - self.percent)]]
      
        testeS = self.scalator.transform(teste)
        resp2 = self.preditor.predict(testeS) #prediz desempenho core Original
        if (resp2 < resp):
            resp = resp2

        return str(round(float(resp[0]), 3))#pior desempenho sera retornado

    def getResultsL(self, IP, ORI):#chamada feita passando os 2 processadores
        original = ORI
        ip = IP
        total = int(original)+int(ip)
        self.cpi = float(self.bd[str(self.processor)][0][str(IP)])
        self.percent = float((int(IP)*float(self.frequencyIP))/((int(IP)*float(self.frequencyIP))+(int(ORI)*float(self.frequencyOriginal))))#calculo da porcentagem
        teste = [[original,ip,total,self.cpi,self.frequencyOriginal,self.percent]]#monta o teste  
            
        testeS = self.scalator.transform(teste)#escalona os parametros
        resp = self.preditor.predict(testeS)#prediz desempenho core IP

        self.cpi = float(self.bd[str(self.originalProcessor)][0][str(original)])
        teste = [[ip, original,total,self.cpi,self.frequencyOriginal,float(1.0 - self.percent)]]
        
        testeS = self.scalator.transform(teste)
        resp2 = self.preditor.predict(testeS) #prediz desempenho core Original

        if (resp2 < resp):
            resp = resp2

        return str(round(float(resp[0]), 3))

    if __name__ == "__main__":
        objPerformancePredictor = PerformancePredictor()
