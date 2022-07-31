import sys
import json
import os
import csv
import re
from glob import glob
from datetime import datetime
from pprint import pprint
import shutil

# Import from any relative path

importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/nsga2/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/'
sys.path.insert(0, importPath)
importPath = os.path.dirname(os.path.realpath(
    __file__)) + '/DS_DSE/brute_force/'
sys.path.insert(0, importPath)

#from Multi2Sim import Multi2Sim
#from Sniper import Sniper
#from McPAT import McPAT
#from MPSoCBench import MPSoCBench

#import InOut
from Nsga2MainVM import Nsga2Main

from DsDseBruteForce import DsDseBruteForce


class MultiExplorer(object):
    """ Main Class for MultiExplorer Software"""

    def __init__(self, inFile):
        self.inFile = inFile
        self.simTool = None
        # Opens the jSON file
        with open(inFile) as data_file:
            self.inJson = json.load(data_file)

        self.dirListB4 = os.listdir(os.getcwd())
        
        # pprint.pprint(self.inJson)
        self.folderOldSimul = None
    pass

    def controller(self):

	global projectFolder
        projectFolder = "rundir/" + self.inJson['Preferences']['project_name']
        # Add Date & Time to the name format: yyyymmdd_hhmmss
        projectFolder += ''.join(str(datetime.now().date()).split('-')) + '_' + str(datetime.now().time()).replace(':', '').split('.')[0]
        
       
        #print "Directory name:", projectFolder
        os.system('mkdir ' + projectFolder)


        self.dseBruteForce()
        #self.dse()
        #self.performanceReport()        
        #if self.inJson['Preferences']['DSE']:
            #self.suggestedArchitecture()
        

   







    def dse(self):
        if self.inJson['Preferences']['DSE']:
            Nsga2Main(projectFolder)
            print "DSE NSGA2: OK"
            #self.suggestedArchitecture()

    def dseBruteForce(self):
        if self.inJson['Preferences']['DSE']:
            DsDseBruteForce(projectFolder)
            print "DSE Brute Force: OK"





    
            
if __name__ == "__main__":
    multiexplorer = MultiExplorer(sys.argv[1])
    
    multiexplorer.controller()
    #multiexplorer.callPerformanceSim()
    #multiexplorer.stepByStep()
    #multiexplorer.physicalSim()

    #multiexplorer.putIntoDir()
    #multiexplorer.dse()
    #multiexplorer.performanceReport()
    #multiexplorer.suggestedArchitecture()
