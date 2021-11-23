from sklearn.externals import joblib

class PerformancePredictor(object):

    """Main Class"""

    def __init__(self, processor, amountIpCore, amountOriginalCore):
    
        self.processor = processor
        self.amountIpCore = amountIpCore
        self.amountOriginalCore = amountOriginalCore

        print self.processor
        print self.amountOriginalCore
        print self.amountIpCore

        #self.getResults()

    def getResults(self):
        preditor = joblib.load(self.processor+'.pkl')
        scalator = joblib.load('Scaler_'+self.processor+'.pkl')
        while(True):
            original = self.amountOriginalCore
            ip = self.amountIpCore
            total = int(original)+int(ip)
            teste = [[original,ip,total]]
            
            testeS = scalator.transform(teste)
            print("\nCaso de Teste: ", testeS)
            resp = preditor.predict(testeS)
            print("\nresp: ", resp)

if __name__ == "__main__":
    objPerformancePredictor = PerformancePredictor()