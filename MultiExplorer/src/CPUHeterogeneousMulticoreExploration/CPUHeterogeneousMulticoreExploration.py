import os
import tkMessageBox

from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Presenters import SniperPresenter, McPATPresenter, \
    NSGAPresenter, BruteForcePresenter
from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow
from MultiExplorer.src.config import PATH_RUNDIR
from Steps import CPUSimulationStep, PhysicalExplorationStep, DSEStep


class CPUHeterogeneousMulticoreExplorationExecutionFlow(ExecutionFlow):
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

    @staticmethod
    def get_info():
        return (
            "This flow allows for an automatic dark silicon aware design space exploration that produces designs for"
            + " multicore heterogeneous platforms.\n"
            + "It begins with the user proposing a homogeneous multicore platform and setting DSE constraints. "
            + "After that, the execution is composed of three steps: Simulation, Physical Exploration and DSE"
            + " (Design Space Exploration).\n"
            + "In the Simulation Step, Sniper is used to assess the performance of the proposed architecture.\n"
            + "In the Physical Exploration Step, McPAT is employed to acquire area and power stats.\n"
            + "Our version of McPAT has been extended to output dark silicon estimates aswell.\n"
            + "In the DSE Step, the NSGA-II algorithm is used for the automatic design space exploration.\n"
            + "The DSE objectives are performance and power density (stat correlated to dark silicon)."
        )

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                CPUHeterogeneousMulticoreExplorationExecutionFlow,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(CPUHeterogeneousMulticoreExplorationExecutionFlow, self).__init__()

        self.steps = [
            CPUSimulationStep(),
            PhysicalExplorationStep(),
            DSEStep(),
        ]

    @staticmethod
    def get_label():
        return 'Multicore CPU Heterogeneous DSDSE'

    def get_output_path(self):
        return (
                PATH_RUNDIR
                + "/" + CPUHeterogeneousMulticoreExplorationExecutionFlow.get_label().replace(' ', '_')
        )

    def setup_dirs(self):
        output_path = self.get_output_path()

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        nbr_of_dirs = len(next(os.walk(output_path))[1])

        nbr_of_dirs = nbr_of_dirs & 63

        output_path = output_path + "/" + "{:02d}".format(nbr_of_dirs)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        for step in self.steps:
            step.set_output_path(output_path)

    def execute(self):
        self.setup_dirs()

        ExecutionFlow.execute(self)

    def get_results(self):
        return {
            "performance_simulation": self.steps[0].get_results(),
            "physical_simulation": self.steps[1].get_results(),
            "dsdse": self.steps[2].get_results(),
        }

    def get_presenters(self):
        return [
            SniperPresenter(),
            McPATPresenter(),
            NSGAPresenter(),
            BruteForcePresenter(),
        ]

    def handle_step_failure(self, step):
        tkMessageBox.showerror(
            "Execution Failure",
            "The " + step.get_label() + " Step execution wasn't successful. " + str(step.execution_exception)
        )

        self.fire(Event.FLOW_EXECUTION_FAILED)

    def finish(self):
        self.fire(Event.FLOW_EXECUTION_ENDED)
