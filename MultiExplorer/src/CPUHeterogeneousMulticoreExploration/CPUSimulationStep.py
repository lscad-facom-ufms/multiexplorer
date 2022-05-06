from MultiExplorer.src.Infrastructure.Input import Input, InputType
from SniperSimulatorAdapter import SniperSimulatorAdapter

class CPUSimulationStep(object):
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
        self.simulator_adapter = SniperSimulatorAdapter()

        self.inputs = {}

        self.add_input(Input({
            'label': 'Preferences',
            'type': InputType.group,
        }))

        self.add_input(Input({
            'label': 'General Modeling',
            'type': InputType.group
        }))

        self.add_input(Input({
            'label': 'Design Space Exploration',
            'type': InputType.group,
        }))

    @staticmethod
    def get_title(): return 'Simulation'

    def add_input(self, new_input): self.inputs[new_input.get_label()] = input

    def get_inputs(self): return self.inputs
