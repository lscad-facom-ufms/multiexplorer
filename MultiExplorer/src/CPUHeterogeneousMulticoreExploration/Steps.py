import threading
import time

from MultiExplorer.src.Infrastructure.Events import Event, EventFirer
from Adapters import SniperSimulatorAdapter


class CPUSimulationStep(EventFirer):
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
        self.events = {
            Event.STEP_EXECUTION_STARTED: [],
            Event.STEP_EXECUTION_ENDED: [],
        }

        self.simulator_adapter = SniperSimulatorAdapter()

        self.execution_thread = None

    @staticmethod
    def get_label(): return 'Simulation'

    @staticmethod
    def has_user_input(): return True

    def get_user_inputs(self):
        return self.simulator_adapter.get_user_inputs()

    def start_execution(self):
        self.execution_thread = threading.Thread(target=self.simulator_adapter.execute)

        self.execution_thread.start()

        self.fire(Event.STEP_EXECUTION_STARTED)

    def is_finished(self):
        if self.execution_thread is None:
            raise RuntimeError("Cannot check execution thread: thread not set.")

        if not self.execution_thread.is_alive():
            self.finish()

            return True

        return False

    def finish(self):
        self.fire(Event.STEP_EXECUTION_ENDED)
