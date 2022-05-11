import json
import os
import sys
from pprint import pprint

from MultiExplorer.src.Infrastructure.Input import Input, InputGroup
from MultiExplorer.src.config import PATH_SNIPER, PATH_RUNDIR


class SniperSimulatorAdapter(object):
    """
    This adapter utilises Snipersim to execute a performance evaluation of a CPU architecture through simulation.
    """
    def __init__(self):
        self.inputs = inputs = {}

        self.results = {}

        self.use_benchmarks = True

        self.benchmark_size = None

        self.cfg_path = None

        self.output_path = None

    def set_inputs(self, inputs):
        for i in inputs:
            if isinstance(i, Input):
                self.inputs[i.key] = i.value
            elif isinstance(i, InputGroup):
                group = i

                for grouped_input in group.inputs:
                    self.inputs[grouped_input.key] = grouped_input.value
            else:
                raise TypeError("Argument 'inputs' must be an array composed solely of objects that belongs either to "
                                "the Input or the InputGroup classes.")

    def execute_simulation(self):
        os.system(
            self.get_executable_path() + "./run-sniper"
            + " -p " + self.inputs["Preferences"]["application"]
            + " -n " + str(self.inputs["General_Modeling"]["total_cores"])
            + " -i " + self.get_benchmark_size()
            + " -c " + self.get_cfg_path()
            + " -d " + self.get_output_path()
            + "> " + self.get_output_path() + "/sniper_output.out"
        )

    def get_executable_path(self):
        if self.use_benchmarks is True:
            return PATH_SNIPER + "/benchmarks/"
        else:
            return PATH_SNIPER

    def get_benchmark_size(self):
        if self.benchmark_size is None:
            return "test"

        return self.benchmark_size

    def get_cfg_path(self):
        if self.cfg_path is None:
            return PATH_SNIPER + "/config/processor.config"

        return self.cfg_path

    def get_output_path(self):
        if self.output_path is None:
            return PATH_RUNDIR

        return self.output_path

    def get_results(self):
        pass


def main():
    sim = SniperSimulatorAdapter()

    sim.inputs = json.loads(open("/home/ufms/projetos/multiexplorer/input-examples/quark.json").read())

    sim.output_path = "/home/ufms/projetos/multiexplorer/rundir/test"

    sim.cfg_path = "/home/ufms/projetos/multiexplorer/input-examples/quark.cfg"

    sim.execute_simulation()


if __name__ == '__main__':
    sys.exit(main())
