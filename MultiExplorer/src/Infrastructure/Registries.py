from typing import Dict, ClassVar
from ExecutionFlow import ExecutionFlow
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
        self.flow_classes = {}  # type: Dict[str, 'class']

        self.register_flow_class(
            CPUHeterogeneousMulticoreExplorationExecutionFlow,
            CPUHeterogeneousMulticoreExplorationExecutionFlow.get_label()
        )

    def register_flow_class(self, flow_class, label):
        # type: ('class', str) -> None
        self.flow_classes[label] = flow_class

    def get_flows_list(self):
        return self.flow_classes.keys()

    def get_flow_class(self, label):
        # type: (str) -> 'class'
        return self.flow_classes[label]

    def get_flow(self, label):
        # type: (str) -> ExecutionFlow
        return self.get_flow_class(label)()
