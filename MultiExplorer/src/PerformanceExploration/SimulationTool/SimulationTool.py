##########################################################################
#                      MultiExplorer Tool                                      #
#                                                                              #
#        - Abstract Base Class SimulationTool                                  #
#                                                                              #
#                                                                              #
##########################################################################

from abc import abstractmethod


class SimulationTool(object):

    """docstring for SimulationTool"""

    def __init__(self, jsonFile, paramMap, outJson):
        super(SimulationTool, self).__init__()
        self.jsonFile = jsonFile
        self.paramMap = paramMap
        self.inputName = None
        self.resultInput = None
        self.outJson = None
        self.outputJson = None
        self.projectDir = None

    @abstractmethod
    def execute(self, configs=None):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def convertResults(self):
        pass

    @abstractmethod
    def writeResults(self):
        pass

    @abstractmethod
    def writeFile(self):
        pass

    def getInputName(self):
        return self.inputName

    def getInput(self):
        return self.resultInput

    def getjSON(self):
        return self.jsonFile

    def getOutputJson(self):
        return self.outputJson
