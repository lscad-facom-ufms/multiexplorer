from abc import ABCMeta, abstractmethod, abstractproperty


class ExecutionFlow(metaclass=ABCMeta):
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
