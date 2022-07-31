from sklearn.externals import joblib
#import dill
import json

class PerformancePredictor(object):

    """Main Class"""

    def __init__(self, mips, coresvm, price, instructions, corescloudlet, heterogeneous):
	
    	self.mips = mips
        self.coresvm = coresvm
        self.price = price
        self.instructions = instructions
        self.corescloudlet = corescloudlet
        self.heterogeneous = heterogeneous



        self.preditorTime = joblib.load("/home/danillo/MultiExplorer/multiexplorerVM-versaofinal/MultiExplorer/src/DS_DSE/predictors/"+'timepredictor2022-2.pkl')#carregou o preditor
        self.scalatorTime = joblib.load("/home/danillo/MultiExplorer/multiexplorerVM-versaofinal/MultiExplorer/src/DS_DSE/predictors/"+'scalertime2022.pkl')#carregou o escalador do conjunto de entrada

        self.preditorCost = joblib.load("/home/danillo/MultiExplorer/multiexplorerVM-versaofinal/MultiExplorer/src/DS_DSE/predictors/"+'costpredictor2022.pkl')#carregou o preditor
        self.scalatorCost = joblib.load("/home/danillo/MultiExplorer/multiexplorerVM-versaofinal/MultiExplorer/src/DS_DSE/predictors/"+'scalercost2022.pkl')#carregou o escalador do conjunto de entrada



    def getResultsTime(self):
        

	teste = [[self.mips,self.coresvm,self.instructions,self.corescloudlet,self.heterogeneous]]#monta o teste   
	    
        #testeS = self.scalatorTime.transform(teste)#escalona os parametros

        resp = self.preditorTime.predict(teste) 

	#print(resp)

        return str(round(float(resp[0]), 3))#tempo predito sera retornado

    def getResultsCost(self):
        

	teste = [[self.mips,self.coresvm,self.price,self.instructions,self.corescloudlet,self.heterogeneous]]#monta o teste        
        testeS = self.scalatorCost.transform(teste)#escalona os parametros
        resp = self.preditorCost.predict(testeS) #prediz custo config

	

        return str(round(float(resp[0]), 3))#custo predito sera retornado



if __name__ == "__main__":
    objPerformancePredictor = PerformancePredictor()
