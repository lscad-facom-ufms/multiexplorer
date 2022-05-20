from MultiExplorer.src.Infrastructure.Inputs import Input, InputType, InputGroup
from Adapters import SniperSimulatorAdapter


class CPUSimulationStep(object):
    """
        This class encapsulates and control the simulation step of a heterogeneous multicore exploration execution flow.

        The main role it plays is to communicate with a SimulatorAdapter, and manage its execution and results.
    """
    inputs = {}

    results = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CPUSimulationStep,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        self.simulator_adapter = SniperSimulatorAdapter()

    @staticmethod
    def get_label(): return 'Simulation'

    @staticmethod
    def has_user_input(): return True

    def get_user_inputs(self):
        return self.simulator_adapter.get_user_inputs()
