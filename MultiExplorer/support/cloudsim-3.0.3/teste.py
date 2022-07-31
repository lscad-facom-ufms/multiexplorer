import os, subprocess, signal

path = "examples/org/cloudbus/cloudsim/examples/"

commandLineCompile = "javac -classpath jars/cloudsim-3.0.3.jar:examples examples/org/cloudbus/cloudsim/examples/CloudSimExample1.java"
commandLineExecute = "java -classpath jars/cloudsim-3.0.3.jar:examples org.cloudbus.cloudsim.examples.CloudSimExample1 > output.txt"


#prepara entrada

mips = 44
size = 44
ram = 44
cpus = 44
coresCloudlet = 44
lengthCloudlet = 44

vmMIPSLine = "			int mips = "+str(mips)+";\n"
vmSizeLine = "			long size = "+str(size)+";\n"
vmRamLine = "			int ram = "+str(ram)+";\n"
vmCpusLine = "			int pesNumber = "+str(cpus)+";\n"

coresCloudletLine = "			int coresCloudlet= "+str(coresCloudlet)+";\n"
lengthCloudletLine = "			long length = "+str(lengthCloudlet)+";\n"



fileExample = open(path+"CloudSimExample.java", "r")
fileInput = open(path+"CloudSimExample1.java", "w")
i=0
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




#compila, executa e gera aqurivo de saida
os.system(commandLineCompile)
os.system(commandLineExecute)


#pega resultado da saida e devolve

with open("output.txt") as f:
    data = f.readlines()[23]
print(data)

outputLine = data.split()

print(outputLine[4])
