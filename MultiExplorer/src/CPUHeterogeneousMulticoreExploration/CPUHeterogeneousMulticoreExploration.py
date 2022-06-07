from MultiExplorer.src.Infrastructure.Events import Event
from Steps import CPUSimulationStep


class CPUHeterogeneousMulticoreExplorationExecutionFlow(object):
    """
    This class controls an execution flow that performs a DSE process based on an initial
    homogeneous multicore architecture. This process is composed of three steps: simulation, physical evaluation, and
    exploration. The main result of the process is a set of new architectures and their evaluations. These architectures
    might include different models of cores (i.e., the results might include heterogeneous architectures).

    This process requires as input the description of a single or multicore homogeneous architecture

    The simulation step consists in acquiring a performance evaluation of the original architecture through
     the use of a simulator (in this case Sniper).

     The physical evaluation step consists in acquiring an evaluation of physical parameters such as area and power.

     The exploration consists of a design space exploration, relying on an exploration engine, that may be built around
     a multi objective optimization algorithm (in this case NSGA-II), aided by an evaluation device (in this case, a
     predictor for both performance and physical evaluation).

     Since we're using a predictor tailored around the core models on its database, the inputs must respect the
     limitations of the dataset available, i.e., only certain core models can be selected, since the predictor can't
     make evaluations for architectures based on any arbitrary core.

     The exploration is oriented towards max performance and minimal power density.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CPUHeterogeneousMulticoreExplorationExecutionFlow,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        self.cur_step = -1

        self.steps = [
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
            CPUSimulationStep(),
        ]

    @staticmethod
    def get_label(): return 'Multicore CPU Heterogeneous DSE'

    def get_steps(self): return self.steps

    def execute(self):
        self.cur_step = -1

        self.execute_next_step()

    def execute_next_step(self):
        self.cur_step += 1

        step = self.steps[self.cur_step]

        step.add_handler(Event.STEP_EXECUTION_ENDED, self.execute_next_step)

        step.start_execution()
