import threading
import time

from MultiExplorer.src.Infrastructure.Events import Event, EventFirer
from Adapters import SniperSimulatorAdapter, McPATAdapter, NsgaIIPredDSEAdapter
from MultiExplorer.src.Infrastructure.ExecutionFlow import Step


class CPUSimulationStep(Step):
    """
        This class encapsulates and control the simulation step of a heterogeneous multicore exploration execution flow.

        The main role it plays is to communicate with a SimulatorAdapter, and manage its execution and results.
    """

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CPUSimulationStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(CPUSimulationStep, self).__init__()

        self.events = {
            Event.STEP_EXECUTION_STARTED: [],
            Event.STEP_EXECUTION_ENDED: [],
        }

        self.simulator_adapter = SniperSimulatorAdapter()

        self.execution_thread = None

    @staticmethod
    def get_label():
        return 'Simulation'

    @staticmethod
    def has_user_input():
        return True

    def get_user_inputs(self):
        return self.simulator_adapter.get_user_inputs()

    # todo
    def __execute__(self):
        self.simulator_adapter.execute()

    # todo
    def __finish__(self):
        self.fire(Event.STEP_EXECUTION_ENDED)


class PhysicalExplorationStep(Step):
    """
        This class encapsulates and control the physical exploration step of a heterogeneous multicore exploration
        execution flow.

        The main role it plays is to communicate with a PhysicalExplorationAdapter, and manage its execution and
        results.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                PhysicalExplorationStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(PhysicalExplorationStep, self).__init__()

        self.events = {
            Event.STEP_EXECUTION_STARTED: [],
            Event.STEP_EXECUTION_ENDED: [],
        }

        self.adapter = McPATAdapter()

        self.execution_thread = None

    @staticmethod
    def get_label(): return 'Physical Exploration'

    # todo
    def __execute__(self):
        self.adapter.execute()

    # todo
    def __finish__(self):
        self.fire(Event.STEP_EXECUTION_ENDED)


class DSEStep(Step):
    """
        This class encapsulates and control the simulation step of a heterogeneous multicore CPU design space
        exploration.

        The main role it plays is to communicate with a DSEAdapter, and manage its execution and results.
    """

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

    # todo
    def __execute__(self):
        self.adapter.execute()

    # todo
    def __finish__(self):
        self.fire(Event.STEP_EXECUTION_ENDED)
