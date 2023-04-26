# -*- coding: utf-8 -*-

import os
import sys

#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/../../support/cloudsim-3.0.3/')
cwd = os.getcwd()


path = "MultiExplorer/src/DS_DSE/cloudsim-3.0.3/examples/org/cloudbus/cloudsim/examples/"
commandLineCompile = "javac -classpath jars/cloudsim-3.0.3.jar:examples examples/org/cloudbus/cloudsim/examples/CloudSimExample1.java"
commandLineExecute = "java -classpath jars/cloudsim-3.0.3.jar:examples org.cloudbus.cloudsim.examples.CloudSimExample1 > output.txt"

#/home/danillo/MultiExplorer/multiexplorerVM-versaofinal/MultiExplorer/src/DS_DSE
class CloudSim(object):

    """
        This class makes the interface between MultiExplorer and CloudSim
    """



    def __init__(self, inputMips, inputSize, inputRam, inputCpus, inputCoresCloudlet, inputLengthCloudlet):
        self.mips = inputMips
        self.size = inputSize
        self.ram = inputRam
        self.cpus = inputCpus
        self.coresCloudlet = inputCoresCloudlet
        self.lengthCloudlet = inputLengthCloudlet



    # This method takes the data of VM and Cloudlet , then
    # return time given by CloudSim, time in seconds (s)
    def getTime(self):

        self.prepareInput()
        
        #compila, executa e gera aqurivo de saida
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        os.system(commandLineCompile)
        os.system(commandLineExecute)

        
        #pega resultado da saida e devolve
        with open("output.txt") as f:
            try:
                data = f.readlines()[23]
            except IndexError:
                data = 0
            except:
                print("Something else went wrong") 
            

        os.chdir(cwd)
        f.close()
    
        if data == 0:
            return "0,0"
            
        outputLine = data.split()

        

        #print(outputLine[4])
        return outputLine[4]





    def prepareInput(self):
        #prepara entrada
        mips = self.mips
        size = self.size
        ram = self.ram 
        cpus = self.cpus
        coresCloudlet = self.coresCloudlet
        lengthCloudlet = self.lengthCloudlet

        vmMIPSLine = "			int mips = "+str(mips)+";\n"
        vmSizeLine = "			long size = "+str(size)+";\n"
        vmRamLine = "			int ram = "+str(ram)+";\n"
        vmCpusLine = "			int pesNumber = "+str(cpus)+";\n"

        coresCloudletLine = "			int coresCloudlet= "+str(coresCloudlet)+";\n"
        lengthCloudletLine = "			long length = "+str(lengthCloudlet)+";\n"



        fileExample = open(path+"CloudSimExample.java", "r")
        fileInput = open(path+"CloudSimExample1.java", "w")
        i = 0
        for line in fileExample:
            if i == 82:
                fileInput.write(vmMIPSLine)
            elif i == 83:
                fileInput.write(vmSizeLine)
            elif i == 84:
                fileInput.write(vmRamLine)
            elif i == 86:
                fileInput.write(vmCpusLine)
            elif i == 106:
                fileInput.write(coresCloudletLine)
            elif i == 103:
                fileInput.write(lengthCloudletLine)
            else:
                fileInput.write(line)
            i= i +1





if __name__ == "__main__":


    obj = CloudSim(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    obj.getTime()







