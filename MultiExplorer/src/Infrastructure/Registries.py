from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.CPUHeterogeneousMulticoreExploration import \
    CPUHeterogeneousMulticoreExplorationExecutionFlow


class ExecutionFlowRegistry(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                ExecutionFlowRegistry,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        self.flow_classes = {}

        self.register_flow_class(
            CPUHeterogeneousMulticoreExplorationExecutionFlow,
            'Multicore CPU Heterogeneous DSE'
        )

    def register_flow_class(self, flow_class, label):
        self.flow_classes[label] = flow_class

    def get_flows_list(self):
        return self.flow_classes.keys()

    def get_flow_class(self, label):
        return self.flow_classes[label]

    def get_flow(self, label):
        return self.get_flow_class(label)()
