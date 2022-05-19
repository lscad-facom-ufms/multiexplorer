from abc import ABCMeta, abstractmethod


class Step:
    __metaclass__ = ABCMeta
    """
    This is the interface used to extend MultiExplorer execution flows with new steps.
    
    Step classes should be implemented as SINGLETONS.
    """

    def __init__(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title) and
                hasattr(subclass, 'has_user_input') and
                callable(subclass.has_user_input))

    @abstractmethod
    def get_label(self): raise NotImplementedError

    @abstractmethod
    def has_user_input(self): raise NotImplementedError


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
        return (hasattr(subclass, 'get_label') and
                callable(subclass.get_title) and
                hasattr(subclass, 'get_steps') and
                callable(subclass.get_steps))

    @abstractmethod
    def get_label(self): raise NotImplementedError

    @abstractmethod
    def get_steps(self): raise NotImplementedError
