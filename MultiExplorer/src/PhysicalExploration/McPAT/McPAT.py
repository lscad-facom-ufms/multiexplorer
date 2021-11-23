import re
import imp
import sys
import os
import json

from copy import deepcopy

try:
    imp.find_module('lxml')
    from lxml import etree as ET
except ImportError:
    print "The lxml library is not installed."
    print "Try $git clone git://github.com/lxml/lxml.git lxml to install"
    exit()


class McPAT(object):
    """docstring for McPAT"""

    def __init__(self, inputJsonPath, inputPerformanceJsonPath, outputName, xmlTemplatePath='Template.xml'):
        super(McPAT, self).__init__()
        self.inputJsonPath = inputJsonPath
        self.inputPerformanceJsonPath = inputPerformanceJsonPath
        self.xmlTemplatePath = os.path.dirname(
            os.path.realpath(__file__)) + '/' + xmlTemplatePath
        self.numOfCores = 0
        self.outputName = outputName

    def getChildrenList(self, regionName, tagName, xmlRoot):
        # List components which are system children
        children = []
        components = list(xmlRoot.iter(tagName))
        for c in components:
            if c.getparent() != None and c.getparent().get('name') == regionName:
                children.append(c)
        return children

    def createXmlInput(self):
        # Open xml file
        doc = ET.parse(self.xmlTemplatePath).getroot()
        #######################################################################
        #       DOING                                                                          #
        #######################################################################

        print(self.inputPerformanceJsonPath)
        print(self.inputJsonPath)

        with open(self.inputPerformanceJsonPath) as data_file:
            statsInput = json.load(data_file)

        with open(self.inputJsonPath) as data_file:
            paramInput = json.load(data_file)
        
        # pprint(statsInput['system'])
        # Figure out the number of cores, L2s, L3s and NoCs
        self.numOfCores = int(statsInput['system']['number_of_cores'])
        self.numOfL2s = int(statsInput['system']['number_of_L2s'])
        self.numOfL3s = int(statsInput['system']['number_of_L3s'])
        self.numOfNoCs = int(statsInput['system']['number_of_NoCs'])

        # Create the base of xml.
        system = self.fillInRegion(ET.Element(
            "component", id="system", name="system"), doc[0], statsInput['system'])

        # Create root and append system on it
        root = ET.Element("component", id="root", name="root")
        root.append(system)

        # print(ET.tostring(root, pretty_print=True))
        # Create xml file to write the result
        file = open(os.getcwd() + '/' + self.outputName, "wb")
        if root is not None:
            # Write the results
            file.write(ET.tostring(root, pretty_print=True))
        else:
            print ("Something has gone wrong!")
        # Close the file
        file.close()
        # doc.write(self.outputName, encoding='UTF-8',pretty_print=True, xml_declaration=True)
        print "Done."
        pass

    def fillInRegion(self, region, elemTemplate, statsData):
        # For any ElementTree, it searches and replace all ids and names with
        # '$' by the number v
        def replacing(elem, v):
            if len(elem):
                elem.set('id', elem.get('id').replace('$', str(v)))
                elem.set('name', elem.get('name').replace('$', str(v)))
                for e in range(len(elem)):
                    if type(elem[e]) is not ET._Comment:
                        replacing(elem[e], v)

        # Loop to write down and append the core nodes into the ElementTree
        def coreFunction(element):
            for c in range(self.numOfCores):
                newCoreRegion = deepcopy(element)
                replacing(newCoreRegion, c)
                newRegion = ET.Element("component", id=newCoreRegion.get(
                    'id'), name=newCoreRegion.get('name'))
                region.append(self.fillInRegion(
                    newRegion, newCoreRegion, statsData[newCoreRegion.get('id')]))

        def L2Function(element):
            for l in range(self.numOfL2s):
                newL2Region = deepcopy(element)
                replacing(newL2Region, l)
                newRegion = ET.Element("component", id=newL2Region.get(
                    'id'), name=newL2Region.get('name'))
                region.append(self.fillInRegion(
                    newRegion, newL2Region, statsData[newL2Region.get('id')]))

        def L3Function(element):
            for l in range(self.numOfL3s):
                newL3Region = deepcopy(element)
                replacing(newL3Region, l)
                newRegion = ET.Element("component", id=newL3Region.get(
                    'id'), name=newL3Region.get('name'))
                region.append(self.fillInRegion(
                    newRegion, newL3Region, statsData[newL3Region.get('id')]))

        def nocFunction(element):
            for l in range(self.numOfNoCs):
                newNoCRegion = deepcopy(element)
                replacing(newNoCRegion, l)
                newRegion = ET.Element("component", id=newNoCRegion.get(
                    'id'), name=newNoCRegion.get('name'))
                region.append(self.fillInRegion(
                    newRegion, newNoCRegion, statsData[newNoCRegion.get('id')]))

        # print "\n\n\t\tWriting %s region....." % (region.get('name'))
        for e in elemTemplate:
            if e.tag == 'stat':
                e.set('value', self.getValue(statsData, e.get('name')))
                # print "- Replacing", e.get('name'), "for", e.get('value')
            elif e.tag == 'param':
                e.set('value', self.getValue(statsData, e.get('name')))
                # print "Param Routine for ", e.get('name')
                # print "- Replacing", e.get('name'), "for", e.get('value')
                pass
            elif e.tag == 'component':
                if e.get('id') in statsData.keys():
                    newRegion = ET.Element(
                        "component", id=e.get('id'), name=e.get('name'))
                    e = self.fillInRegion(newRegion, e, statsData[e.get('id')])
                else:
                    matchTest = re.match(r"(\w+)\$", e.get('name'))
                    if matchTest:
                        e = eval(matchTest.group(1) + 'Function(e)')
                    #else:
                    #    print "*** Match not found:", e.get('id')
                pass
            # print "After:", e.get('value')
            if e is not None:
                region.append(e)

        # for r in region:
        #     print r.tag, '--', r.attrib

        # for e in self.getChildrenList('system','component', elemTemplate):
        #     print e.get('name')
        return region
        pass

    def getValue(self, data, parameterName):
        if parameterName in data.keys():
            return str(data[parameterName])
        else:
            print "*** Match not found:", parameterName
            return '0'

    def parseStatsInput(self, doc):
        def getValue(statsInput, s, parent=None):
            elem = None
            for item in statsInput.keys():
                if isinstance(statsInput[item], dict):
                    elem = getValue(statsInput[item], stats, item)
                else:
                    # print "StatsInput[%s]:"%(item),statsInput[item], "- Parent:", parent
                    # [x for x in lst if fulfills_some_condition(x)]
                    # elem = next(x for x in stats if x.get('name') == item and x.getparent() == parent)
                    for x in stats:
                        if (x.get('name') == item and x.getparent().get('name') == parent):
                            x.set('value', str(statsInput[item]))

                    # print "Stats for x:", x.get('name'), "- Parent:",
                    # x.getparent().get('name')
            pass

        with open(self.inputPerformanceJsonPath) as data_file:
            statsInput = json.load(data_file)

        # Get all the elements by the tag "stat"
        stats = list(doc.iter("stat"))
        # print "BEFORE"
        # for s in stats:
        #     print s.attrib
        getValue(statsInput, stats)

        # print "\n\n\nAFTER"
        # for s in stats:
        #     print s.attrib

        pass

    def parseParamInput(self, doc):
        with open(self.inputJsonPath) as data_file:
            paramInput = json.load(data_file)
        pass

    def getElementValue(self, path, data):
        pass

    def execute(self, configs=None):
        commandLine = os.path.dirname(os.path.realpath(__file__)) + '/../../../support/mcpat/mcpat -infile ' + self.outputName
        commandLine += ' -print_level 5 > MCPATPhysicalResults'
        commandLine += '.txt'
        print "*** McPAT ***"
        os.system(commandLine)
        pass

if __name__ == "__main__":
    print "wrong path called"
    m = McPAT("/home/melgarejojr/DarkSilicon/ds-repo/MultiExplorer/samples/input1.json",
              sys.argv[1], sys.argv[2], "Template.xml")
    m.createXmlInput()
