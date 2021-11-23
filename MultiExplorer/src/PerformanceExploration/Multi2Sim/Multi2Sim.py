import json
import os
import sys
import re
import ast
import imp

from copy import deepcopy
from M2SNetwork import M2SNetwork

try:
    imp.find_module('configparser')
    from configparser import ConfigParser as iniParser
except ImportError:
    print "The configparser library is not installed."
    print "Try $ pip install configparser to install"
    exit()


# Import from any relative path
importPath = os.path.dirname(os.path.realpath(__file__)) + '/../SimulationTool'
sys.path.insert(0, importPath)

from SimulationTool import SimulationTool


class Multi2Sim(SimulationTool):

    """docstring for Multi2Sim"""

    def __init__(self, jsonFile, paramMap, outJson):
        super(Multi2Sim, self).__init__(jsonFile, paramMap, outJson)
        self.resultInput = {'proc': "", 'mem': ""}
        # Opens the jSON file with all parameters to map the input
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + paramMap) as data_file:
            self.paramMap = json.load(data_file)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + outJson) as data_file:
            self.outJson = json.load(data_file)
        self.outputJson = None

    # Gather all the files created and execute m2s in the commandLine.
    def execute(self, configs=None):
        outname = "Resultado_" + self.inputName.replace('Input_', "")
        # Gets the cmd line to execute Multi2Sim
        commandLine = "m2s --x86-sim detailed --x86-report " + outname
        commandLine += " --x86-config " + self.inputName + ".ini"

        # Includes mem-config file if it exists.
        if self.resultInput['mem'] is not None:
            commandLine += " --mem-config " + self.inputName + \
                "_memconfig.ini"
            commandLine += " --mem-report " + outname + "_mem"
            pass

        # Opens the jSON file and stores it as a list
        with open(self.jsonFile) as data_file:
            data = json.load(data_file)
        commandLine += " 2> " + \
            self.inputName.replace('Input_', "") + "_cmdOutput.txt"
        print commandLine
        os.system(commandLine)

        self.outputNamePath = {outname: os.getcwd() + '/' + outname, outname + "_cmdOutput.txt": os.getcwd(
        ) + '/' + outname + "_cmdOutput.txt", outname + "_mem": os.getcwd() + '/' + outname + "_mem"}
        pass

    # Create the .ini file that will be used as input for m2s.
    def writeFile(self):
        print (self.inputName)

        # Open a file with the processor name
        inputFile = open(os.getcwd() + '/' + self.inputName + ".ini", "wb")
        if self.resultInput is not None:
            # Write the results
            inputFile.write(self.resultInput['proc'])
        else:
            print ("Something has gone wrong!")
        # Close the file
        inputFile.close()

        # Open a file with the processor name, but for memory
        inputFile = open(os.getcwd() + '/' +
                         self.inputName + "_memconfig.ini", "wb")
        self.memInput.write(inputFile)
        # Close the file
        inputFile.close()
        pass

    # Translate the MultiExplorer input as a set of m2s files.
    def parse(self):
        print "===== PARSING ======"

        # Opens the jSON file and stores it as a dict
        with open(self.jsonFile) as data_file:
            data = json.load(data_file)

        ###Gets some of the information needed to run ###
        # Input Configuration for the processor
        processorConfig = data['General_Modeling']
        # Number of Cores
        self.numberOfCores = int(data['General_Modeling']['total_cores'])
        self.numberOfThreads = int(data['General_Modeling']['core']['threads'])
        # Calculate the number of L2s and L3s
        self.numberOfL2s = len([d for d in data['General_Modeling'][
                               'memory'] if d.find('l2') != -1])
        self.numberOfL3s = len([d for d in data['General_Modeling'][
                               'memory'] if d.find('l3') != -1])
        # Default value for NoCs
        self.numberOfNocs = 1

        # Take the attributes names and values to be written in a string
        resultString = ""

        ##############################################
        # TRANSFORM THE INPUT INTO M2S REPORT MODEL

        # Write [General] Section
        resultString += self.generalSection(processorConfig)

        # Write [Pipeline] Section
        resultString += self.pipelineSection(
            processorConfig['core']['pipeline'])

        # Write [Queues] Section
        resultString += self.queuesSection(processorConfig)

        # Write [Trace Cache] Section
        resultString += self.tracecacheSection(processorConfig)

        # Write [Functional Units] Section
        resultString += self.functionalUnitsSection(processorConfig)

        # Write [Branch Predictor] Section
        resultString += self.branchPredictorSection(processorConfig)

        try:
            # Write Memory config file
            self.resultInput['mem'] = self.memoryReport(
            processorConfig['memory'], processorConfig['network'])
        except KeyError:
            # In case memory is not in the input File
            self.resultInput['mem'] = None 
            
        ##############################################

        self.resultInput['proc'] = resultString

        # Create a file with the final result and named as
        # "Multi2Sim_Input_<processor name>"
        self.inputName = type(self).__name__ + "_Input_" + \
            data['Preferences']['project_name']
        self.writeFile()
        pass

    # Get a path with regions separated by a splitter and
    # search the indicated value into data to return it.
    def mappedValuesToString(self, path, data, splitter='.'):
        k = None
        desiredRegion = path.split(splitter)
        if len(desiredRegion) > 1:
            k = data[desiredRegion[0]]
            for i in xrange(1, len(desiredRegion)):
                k = k[desiredRegion[i]]
        else:
            k = data[desiredRegion[0]]
        return str(k)

    # Rewrite the name capitalized
    def transformIntoM2sStandard(self, name):
        temp = re.match(u'([A-Z|a-z]+)(_([A-Z|a-z]+))?', name)
        if temp.group(2) != None:
            return temp.group(1).title() + temp.group(3).title()
        else:
            return temp.group(1).title()

    # Write the General Section from x86 .ini file
    def generalSection(self, data):
        def mappedValuesToStringLoop(mappedKeys, data):
            txt = ""
            for p in mappedKeys.keys():
                k = self.mappedValuesToString(mappedKeys[p], data)
                txt += p + " = " + k + "\n"
            return txt

        general = self.paramMap['General']
        txt = "[General]\n"
        txt += mappedValuesToStringLoop(general, data)
        return txt + "\n"
    # Write the Pipeline Section from x86 .ini file

    def pipelineSection(self, data):
        txt = "[Pipeline]\n"
        if data['present']:
            for p in data.keys():
                if p != 'present':
                    p_ = self.transformIntoM2sStandard(p)
                    txt += p_ + " = " + str(data[p]) + '\n'
        return txt

    # Write the Queues Section from x86 .ini file
    def queuesSection(self, data):
        return ""

    # Write the Trace Cache Section from x86 .ini file
    def tracecacheSection(self, data):
        return ""

    # Write the Functional Units Section from x86 .ini file
    def functionalUnitsSection(self, data):
        return ""
    # Write the Branch Prediction Section from x86 .ini file

    def branchPredictorSection(self, data):
        return ""

    # Write the Memory .ini file
    def memoryReport(self, data, netData):
        def createMemoryGeometry(region):
            # print 'Inner Function(' + num + ')'
            # print 'Region:', region
            # print 'Data: ', data
            newDict = {}
            for r in region:
                # print 'r --> ' + r
                if type(region[r]) != list:
                    # print r, region[r]
                    newDict[r] = self.mappedValuesToString(region[r], data)
                else:
                    # Calculate Sets or Latency
                    values = []
                    for e in region[r]:
                        values.append(
                            int(self.mappedValuesToString(e, data)))
                    # print values
                    if r == 'Sets':
                        newDict['Sets'] = values[0] / values[1] / values[2]
                    elif r == 'Latency':
                        newDict['Latency'] = sum(values)
                    del values
                    pass
            # print newDict
            return newDict

        ##############################################
        ##############################################

        def createEntry():
            newDict = {}
            for core in xrange(self.numberOfCores):
                for thread in xrange(self.numberOfThreads):
                    entryName = 'Entry core-' + str(core) + '-' + str(thread)
                    coreEntry = {entryName: {'Arch': 'x86'}}
                    coreEntry[entryName]['Thread'] = thread
                    coreEntry[entryName]['Core'] = core

                    # print 'Starting search'
                    for d in data:
                        if d.find('dcache') != -1:
                            # print data[d]['shared_cores']
                            # print core in data[d]['shared_cores']
                            if core in data[d]['shared_cores'] or 'all' in data[d]['shared_cores']:
                                coreEntry[entryName][
                                    'DataModule'] = d.capitalize()
                        elif d.find('icache') != -1:
                            # print data[d]['shared_cores']
                            # print core in data[d]['shared_cores']
                            if core in data[d]['shared_cores'] or 'all' in data[d]['shared_cores']:
                                coreEntry[entryName][
                                    'InstModule'] = d.capitalize()
                    newDict.update(coreEntry)
            # print '---->',newDict
            return newDict

        ##############################################
        ##############################################

        def createMainMemory():
            MMModules = {}
            mainMemory_template = self.paramMap['Mem-config']['Module mm-$']
            # Find out the number of banks
            numOfBanks = data['dram']['controllers_interleaving']
            # Create each bank module
            for bank in xrange(numOfBanks):
                moduleName = 'Module mm-' + str(bank)
                newMMModule = {moduleName: deepcopy(mainMemory_template)}
                for item in newMMModule[moduleName]:
                    if item != 'AddressRange':
                        try:
                            newMMModule[moduleName][item] = self.mappedValuesToString(
                                newMMModule[moduleName][item], data)
                        except:
                            pass
                    else:
                        values = []
                        for e in newMMModule[moduleName][item]:
                            values.append(self.mappedValuesToString(e, data))
                        # Write an address range for each module,
                        # since they are in the same network
                        newMMModule[moduleName][
                            item] = 'ADDR DIV ' + \
                            str(values[0]) + ' MOD ' + \
                            str(values[1]) + ' EQ ' + str(bank)
                        # print item, newMMModule[moduleName][item]
                MMModules.update(newMMModule)
            return MMModules

        ##############################################
        ##############################################

        def createNetwork():
            # print 'data'  , netData
            cacheLevels = data['cache']['levels']
            netList = []
            coresRelated = {}
            # This vector keeps tracking the number of
            # networks created for each level
            numOfNetLevel = [0] * cacheLevels

            # Filter just caches and which cores they share
            cacheList = [{d: data[d]["shared_cores"]}
                         for d in data if d.find("cache-") != -1]

            # Get the path for each core visiting all caches
            for core in xrange(self.numberOfCores):
                coresRelated[core] = []
                for cache in cacheList:
                    cKey = cache.keys()[0]
                    # print cKey, cache[cKey]
                    if core in cache[cKey] or 'all' in cache[cKey]:
                        coresRelated[core].append(cKey)
                coresRelated[core].sort()
            # print 'cR:', coresRelated

            # Verify if there is just one level of cache
            if cacheLevels >=2:

                for c in coresRelated:
                    for level in xrange(2, cacheLevels + 1):
                        outs = []
                        ins = []
                        for elem in coresRelated[c]:
                            if elem.find('l' + str(level)) != -1:
                                outs.append(elem.capitalize())
                            elif elem.find('l' + str(level - 1)) != -1:
                                ins.append(elem.capitalize())
                        netName = 'net-l' + \
                            str(level - 1) + '-l' + str(level) + \
                            '-' + str(numOfNetLevel[level - 2])

                        # Verify if there is a network with the same Low Modules

                        # First loop
                        if not len(netList):
                            thisNetConfig = netData[
                                netData['memory_model_' + str(level - 1)]]
                            newNet = M2SNetwork(
                                ins, outs, thisNetConfig, netName, 'simple')
                            netList.append(newNet)
                            numOfNetLevel[level - 2] += 1
                        else:
                            netFlag = False
                            for net in netList:
                                if all(x in net.getLowModules() for x in outs):
                                    # print 'Add inputs'
                                    netFlag = True
                                    for i in ins:
                                        if not i in net.getHighModules():
                                            net.addInput(i)
                                            # print 'here', i, net.networkName
                            if not netFlag:
                                thisNetConfig = netData[
                                    netData['memory_model_' + str(level - 1)]]
                                newNet = M2SNetwork(
                                    ins, outs, thisNetConfig, netName, 'simple')
                                netList.append(newNet)
                                numOfNetLevel[level - 2] += 1
            else:
                level = 1
            # Create a connection between the last level and the MainMemory
            lastLevel = [d[7:] for d in self.memInput if d.find(
                "Module L" + str(cacheLevels)) != -1]
            mainMemory = [d[7:] for d in self.memInput if d.find("mm-") != -1]
            thisNetConfig = netData[netData['memory_model_' + str(level)]]
            # print lastLevel, 'and', mainMemory, 'and', thisNetConfig
            netName = 'net-l' + str(cacheLevels) + '-mm'
            netList.append(M2SNetwork(
                lastLevel, mainMemory, thisNetConfig, netName))
            # for n in netList:
            #     print 'N-->'
            #     n.printAttr()
            # Include Network into modules
            for mem in self.memInput:
                if mem.find("Module") != -1:
                    memName = mem[7:]
                    # print self.memInput[mem]
                    for net in netList:
                        # print net.networkName,  memName in
                        # net.getHighModules(), memName, net.getHighModules()
                        if memName in net.getHighModules():
                            # print 'Low'
                            # Include LowNetwork
                            self.memInput[mem]['LowNetwork'] = net.networkName
                            # Include LowNetworkModules
                            self.memInput[mem]['LowModules'] = ' '.join(
                                net.getLowModules())
                            # Include LowNetworkNodes
                            pass
                        elif memName in net.getLowModules():
                            # print 'High'
                            # Include HighNetwork
                            self.memInput[mem]['HighNetwork'] = net.networkName
                            # Include HighNetworkNodes
                        # Include network configuration into memInput
                        if not net.networkName in self.memInput:
                            # print net.getNetworkConfig()
                            self.memInput.update(net.getNetworkConfig())

        ##############################################
        ##############################################

        def replacing(dictionary, word, replaceTo='#'):
            for d in dictionary:
                if not type(dictionary[d]) is list and dictionary[d]:
                    if d != 'Geometry':
                        dictionary[d] = dictionary[d].replace(replaceTo, word)
                    else:
                        dictionary[d] = dictionary[d].replace(
                            replaceTo, word.capitalize())
                else:
                    for e in xrange(len(dictionary[d])):
                        dictionary[d][e] = dictionary[d][
                            e].replace(replaceTo, word)
            return dictionary

        ##############################################
        #         START memoryReport Function        #
        ##############################################
        self.memInput = iniParser()

        # Create a map according to the number of L1/L2/L3...
        numOfDCache = len([d for d in data if d.find('dcache') != -1])
        numOfICache = len([d for d in data if d.find('icache') != -1])

        # Insert all the cache number in a dictionary
        numOfCaches = {'L1_dcache': numOfDCache, 'L1_icache': numOfICache,
                       'L2_cache': self.numberOfL2s, 'L3_cache': self.numberOfL3s}
        memTemplate = {'CacheGeometry geo-#':
                       self.paramMap[
                           'Mem-config']['CacheGeometry geo-#'],
                       'Module #': self.paramMap['Mem-config']['Module #']}
        mem_config = {}
        # Create a memoryMap according to the number of Caches
        for nCache in numOfCaches:
            for num in xrange(numOfCaches[nCache]):
                memTemplateCopy = deepcopy(memTemplate)
                for mt in memTemplateCopy:
                    cacheName = nCache + '-' + str(num)
                    mem_config[mt.replace('#', cacheName)] = replacing(
                        memTemplateCopy[mt], cacheName.lower())

        # Fill CacheGeometry and Module map
        for mc in mem_config:
            if mc.find('CacheGeometry') != -1:
                self.memInput[mc] = (createMemoryGeometry(mem_config[mc]))
            elif mc.find('Module') != -1:
                self.memInput[mc] = mem_config[mc]
        # Create Entries for each core and thread
        self.memInput.update(createEntry())

        # Create Main Memory Modules
        self.memInput.update(createMainMemory())

        # Create the NetWork
        createNetwork()

        return ""

    def printJson(self, dictJson, level=0):
        levelstr = ""
        for i in range(level):
            levelstr += "\t"
        for p in dictJson.keys():
            if isinstance(dictJson[p], dict):
                print levelstr, p, "{"
                self.printJson(dictJson[p], level + 1)
                print levelstr + "}"
            else:
                print (levelstr + str(p) + ': ' + str(dictJson[p]))
        pass

    def fillInRegion(self, key, region, regionTemplate, databases):
        # It's a variable which stores the attributes that
        # use the " , , ,..." format.
        #############################################################
        #                 INNER FUNCTIONS                           #
        #############################################################
        def findEntry(n, word):
            # print word
            db = [d['memory'] for d in databases if "core" in d.keys()][0]
            for d in db.keys():
                if (word in d):
                    if (int(n) in db[d]["shared_cores"] or 'all' in db[d]["shared_cores"]):
                        return d[-1]
            pass
            # return str(number)
        # Create the lines with more than one value. As they are set right
        # below
        btwnComas = ['buffer_sizes', 'pipelines_per_core', 'pipeline_depth']

        def btwnComasFunction(pathStr, num):
            pathList = pathStr.split(',')
            # print pathList
            valuesList = []
            for p in pathList:
                if p.find('#') != -1:
                    # print 'entrou', p ,re.match(r'.*\s?((l|L)(\d)_(d|i)?cache)', p).group(1)
                    # entry = findEntry(num, ].lower())
                    entry = findEntry(num, re.match(
                        r'.*\s?((l|L)(\d)_(d|i)?cache)', p).group(1).lower())

                    p = p.replace('#', entry)
                # print p
                if p.find('cache_size') != -1:
                    valuesList.append(str(int(self.getValue(p, databases))*1024))
                else:
                    valuesList.append(self.getValue(p, databases))
            # Get the list, convert each number into strings followed by coma,
            # between quotes
            return (''.join(str(e) + ',' for e in valuesList))[:-1]

        def replacing(elem, num):
            for e in elem.keys():
                # Write the lines which are more than one value between comas
                if e in btwnComas or e.find('_config') != -1:
                    # print e
                    elem[e] = elem[e].replace('$', num)
                    elem[e] = btwnComasFunction(elem[e], num)
                    # print 'e:', elem[e]
                if isinstance(elem[e], dict):
                    elem[e.replace('$', num)] = elem[e]
                    del elem[e]
                    replacing(elem[e.replace('$', num)], num)
                elif e == 'total_cycles' or e == 'busy_cycles':
                    elem[e] = elem[e].replace('$', num)
                    splitPhrase = elem[e].split(',')
                    elem[e] = int(float(self.getValue(
                        splitPhrase[0], databases)) / (float(self.getValue(splitPhrase[1], databases)) + 0.00001))
                else:
                    if elem[e].find('#') != -1:
                        entry = findEntry(num, re.match(
                            r'.*\s?((l|L)(\d)_(d|i)?cache)', elem[e]).group(1).lower())
                        elem[e] = elem[e].replace('#', entry)
                        # print elem[e]
                    elem[e] = elem[e].replace('$', num)
                    elem[e] = self.getValue(elem[e], databases)
            pass

        def replaceCharLoop(element, elementName):
            self
            matchTest = re.match(r"system.(.*)\$", elementName)
            if matchTest:
                loops = eval('self.numberOf' +
                             matchTest.group(1).capitalize() + 's')
                for c in range(int(loops)):
                    newRegion = deepcopy(element)
                    replacing(newRegion, str(c))
                    region[key].update(
                        {(key + '.' + matchTest.group(1) + str(c)): newRegion})
            pass
        #############################################################
        #############################################################

        def solveForMM(template, databases):
            newDict = {}
            for db in databases:
                if 'mm-0' in db.keys():
                    data = db
            numOfMainMem = int(self.getValue(
                "memory/dram/controllers_interleaving", databases))
            # print db, numOfMainMem
            for k in template:
                # print template[k]
                if template[k].find('$') == -1:
                    newDict[k] = self.getValue(template[k], databases)
                else:
                    value = []
                    for mem in xrange(numOfMainMem):
                        value.append(
                            int(self.getValue(template[k].replace('$', str(mem)), databases)))
                    newDict[k] = sum(value)
                    # print value

            # print newDict
            return newDict
        #############################################################
        #############################################################

        for k in regionTemplate.keys():
            if isinstance(regionTemplate[k], dict):
                if k.find('mc') != -1:
                    innerDict = solveForMM(regionTemplate[k], databases)
                    # print key
                    region[key][k] = (innerDict)
                elif k.find('$') == -1:
                    innerDict = self.fillInRegion(
                        k, {k: {}}, regionTemplate[k], databases)
                    region[key].update(innerDict)
                else:
                    replaceCharLoop(regionTemplate[k], k)
            else:
                # print 'region: ' + k
                region[key].update(
                    {k: self.getValue(regionTemplate[k], databases)})
        # self.printintJson(region)
        return region

    def getValue(self, word, databases):
        # print 'word:',word
        def searchOnFile(sections, file):
            # print 'word(into SearchOnFile):',word
            # print 'sections:', sections
            value = file[sections[0]]
            for s in sections[1:]:
                value = value[s]
                # print 'value:',value
            return str(value)
        #############################
        if word.find('/') != -1:
            sectionMap = word.split('/')
            for db in databases:
                dbKeys = db.keys()
                # print sectionMap[0], dbKeys, "\n", sectionMap[0] in dbKeys
                if sectionMap[0] in dbKeys:
                    # print 'if:',sectionMap[0]
                    return searchOnFile(sectionMap, db)
        else:
            # print 'returning', word
            return word

    def convertResults(self):
        print "===== CONVERTING RESULTS ======"
        ##############################################
        #        START convertResults Function       #
        ##############################################

        # Load config files
        with open(self.jsonFile) as data_file:
            inputJson = json.load(data_file)
        iniConfigFile = iniParser()
        iniMemFile = iniParser()
        for p in self.outputNamePath.keys():
            if p.find('cmd') == -1 and p.find('mem') == -1:
                # print self.outputNamePath[p]
                iniConfigFile.read(self.outputNamePath[p])
            elif p.find('mem') != -1:
                # print self.outputNamePath[p]
                iniMemFile.read(self.outputNamePath[p])
        # iniConfigFile.read(
        #     '/home/melgarejojr/Desktop/MultiExplorerFiles/ResultTest/meshTest-x86.ini')
        # iniMemFile.read(
        #     '/home/melgarejojr/Desktop/MultiExplorerFiles/ResultTest/meshTest-mem.ini')

        systemJson = self.fillInRegion('system', {'system': {}}, self.outJson['system'], [
                                       inputJson['General_Modeling'], iniConfigFile, iniMemFile])

        systemJson['system']['number_of_L2s'] = str(self.numberOfL2s)
        systemJson['system']['number_of_L3s'] = str(self.numberOfL3s)
        with open('testing.json', 'w') as outfile:
            json.dump(systemJson, outfile, indent=4, sort_keys=True)
        self.outputJson = os.path.realpath('testing.json')
        pass

        ##############################################
        #        END convertResults Function         #
        ##############################################

    def writeResults(self):
        pass

if __name__ == "__main__":
    m = Multi2Sim(sys.argv[1], "paramMap.json", "PerformanceMap_new.json")
    m.parse()
    m.execute()
    m.convertResults()
