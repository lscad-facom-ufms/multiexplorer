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

    @staticmethod
    def get_title(): return 'Simulation'
