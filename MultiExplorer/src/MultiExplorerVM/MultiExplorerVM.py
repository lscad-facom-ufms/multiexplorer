import os
import tkMessageBox

from MultiExplorer.src.Infrastructure.Events import Event
from MultiExplorer.src.Infrastructure.ExecutionFlow import ExecutionFlow
from MultiExplorer.src.config import PATH_RUNDIR
from Steps import CloudSimStep, NSGAIIDSEStep

class MultiExplorerVMExecutionFlow(ExecutionFlow):


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
                MultiExplorerVMExecutionFlow,
                cls
            ).__new__(cls)

        return cls.instance

    def __init__(self):
        super(MultiExplorerVMExecutionFlow, self).__init__()

        self.steps = [
            CloudSimStep(),
            NSGAIIDSEStep()
        ]

    @staticmethod
    def get_label():
        return 'MultiExplorer VM'

    def get_output_path(self):
        return (
                PATH_RUNDIR
                + "/" + MultiExplorerVMExecutionFlow.get_label().replace(' ', '_')
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

    def handle_step_failure(self, step):
        tkMessageBox.showerror(
            "Execution Failure",
            "The " + step.get_label() + " Step execution wasn't successful. " + str(step.execution_exception)
        )

        self.fire(Event.FLOW_EXECUTION_FAILED)

    def finish(self):
        self.fire(Event.FLOW_EXECUTION_ENDED)
