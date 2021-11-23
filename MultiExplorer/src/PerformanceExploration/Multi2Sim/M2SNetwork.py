class M2SNetwork(object):

    """docstring for M2SNetwork"""

    def __init__(self, inputs, outputs, netConfig, name, topology='simple'):
        super(M2SNetwork, self).__init__()
        self.inputs = inputs
        self.outputs = outputs
        self.inputBuffer = int(netConfig["input_buffer"])
        self.outputBuffer = int(netConfig["output_buffer"])
        self.bandwidth = int(netConfig["bandwidth"])
        self.networkName = name
        self.networkConfig = {}
        self.createNetworkConfig(topology)

    @staticmethod
    def getHighNetwork(module, networkList):
        for net in networkList:
            if module in net.outputs:
                return net
        return None

    @staticmethod
    def getLowNetwork(module, networkList):
        for net in networkList:
            if module in net.inputs:
                return net
        return None

    @staticmethod
    def getLowNetworkModules(module, networkList):
        for net in networkList:
            if module in net.inputs:
                return net.outputs
        return None

    def createNetworkConfig(self, topology):
        function = 'self.' + topology.lower() + '()'
        self.networkConfig = eval(function)
        pass

    def simple(self):
        return {'Network ' + self.networkName:
                {"DefaultInputBufferSize": self.inputBuffer,
                 "DefaultOutputBufferSize": self.outputBuffer,
                 "DefaultBandwidth": self.bandwidth}}

    def line(self):
        print "Not supported yet!"
        exit()
        pass

    def ring(self):
        print "Not supported yet!"
        exit()
        pass

    def mesh(self):
        print "Not supported yet!"
        exit()
        pass

    def torus(self):
        print "Not supported yet!"
        exit()
        pass

    def getNetworkConfig(self):
        return self.networkConfig

    def getLowModules(self):
        return self.outputs

    def getHighModules(self):
        return self.inputs

    def addInput(self, inModule):
        self.inputs.append(inModule)
        pass

    def addOutput(self, outModule):
        self.outputs.append(outModule)
        pass
    
    def printAttr(self):
        print "\n",self.networkName
        print "    High:", self.inputs
        print "    Low:", self.outputs

