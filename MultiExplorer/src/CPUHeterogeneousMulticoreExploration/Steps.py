from MultiExplorer.src.Infrastructure.Events import Event
from Adapters import SniperSimulatorAdapter, McPATAdapter, NsgaIIPredDSEAdapter
from MultiExplorer.src.Infrastructure.ExecutionFlow import Step


class CPUSimulationStep(Step):
    """
        This class encapsulates and control the simulation step of a heterogeneous multicore exploration execution flow.

        The main role it plays is to communicate with a SimulatorAdapter, and manage its execution and results.
    """
    def get_results(self):
        return self.adapter.get_results()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CPUSimulationStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(CPUSimulationStep, self).__init__()

        self.adapter = SniperSimulatorAdapter()

    @staticmethod
    def get_label():
        return 'Simulation'

    @staticmethod
    def has_user_input():
        return True

    def get_user_inputs(self):
        return self.adapter.get_user_inputs()

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)


class PhysicalExplorationStep(Step):
    """
        This class encapsulates and control the physical exploration step of a heterogeneous multicore exploration
        execution flow.

        The main role it plays is to communicate with a PhysicalExplorationAdapter, and manage its execution and
        results.
    """
    def get_results(self):
        return self.adapter.get_results()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                PhysicalExplorationStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(PhysicalExplorationStep, self).__init__()

        self.adapter = McPATAdapter()

    @staticmethod
    def get_label(): return 'Physical Exploration'

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)


class DSEStep(Step):
    """
        This class encapsulates and control the simulation step of a heterogeneous multicore CPU design space
        exploration.

        The main role it plays is to communicate with a DSEAdapter, and manage its execution and results.
    """
    def get_results(self):
        return self.adapter.get_results()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                DSEStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(DSEStep, self).__init__()

        self.adapter = NsgaIIPredDSEAdapter()

    @staticmethod
    def get_label(): return 'DSE'

    @staticmethod
    def has_user_input(): return True

    def get_user_inputs(self): return self.adapter.get_user_inputs()

    def __execute__(self):
        self.execution_exception = None

        try:
            self.adapter.execute()
        except BaseException as exception:
            self.execution_exception = exception

    def __finish__(self):
        if self.execution_exception is None:
            self.fire(Event.STEP_EXECUTION_ENDED)
        else:
            self.fire(Event.STEP_EXECUTION_FAILED, self)
