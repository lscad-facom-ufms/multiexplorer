from abc import ABCMeta, abstractmethod

from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.CPUHeterogeneousMulticoreExplorationExecutionFlow import \
    CPUHeterogeneousMulticoreExplorationExecutionFlow


class ExecutionFlowRegistry(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                ExecutionFlowRegistry,
                cls
            ).__new__(cls)

        return cls.instance

    def get_flow_list(self):
        return [
            'CPU'
        ]

    def get_flow(self, list_value):
        if list_value == 'CPU':
            return CPUHeterogeneousMulticoreExplorationExecutionFlow()


class ExecutionFlow:
    __metaclass__ = ABCMeta
    """
    This is the interface used to extend MultiExplorer with a new execution flow.

    ExecutionFlow classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_title') and
                callable(subclass.get_title) and
                hasattr(subclass, 'get_steps') and
                callable(subclass.get_steps))

    @abstractmethod
    def get_title(self): raise NotImplementedError

    @abstractmethod
    def get_steps(self): raise NotImplementedError
