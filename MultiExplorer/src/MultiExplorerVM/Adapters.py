import json
import os
import sys
import re
from typing import Dict, Union, Any, Optional
from xml.dom import minidom
from xml.etree import ElementTree
from MultiExplorer.src.MultiExplorerVM.AllowedValues import PredictedModels, \
    PredictedApplications, Applications
from MultiExplorer.src.MultiExplorerVM.DS_DSE.Nsga2MainVM import Nsga2Main
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_PRED_VM

class CloudsimAdapter(Adapter):
    def __init__(self):
        Adapter.__init__(self)

        self.presenter = None

        self.set_inputs([
            Input({
                'label' : 'Application',
                'key' : 'application',
                'allowed_values' : Applications.get_dict(),
                'value' : Applications.SPLASH_II_CHOLESKY.value,
            }),
            InputGroup({
                "label" : "Original Platform",
                "subtitle": (
                    "This platform will be the starting point for the automatic DSE."
                    + " It will be evaluated through simulation by Cloudsim."
                ),
                "key" : "general_modeling",
                "inputs" : [
                    Input({
                        "label" : "Model VM",
                        "key" : "model_vm",
                        "is_user_input" : True,
                        "required" : True,
                        "allowed_values" : PredictedModels.get_dict(),
                    }),
                    Input({
                        "label" : "Applicaton VM",
                        "key" : "application_vm",
                        "is_user_input" : True,
                        "required" : True,
                        "Allowed_values" : PredictedApplications.get_dict(),
                    }),
                ]
            })
        ]
        )

    def set_values_from_json(self, absolute_file_path):
        """
        This method reads a json file and sets the values of the inputs.
        """
        input_json = json.loads(open(absolute_file_path).read())

class NsgaIIPredDSEAdapter(Adapter):
    """
        This adapter uses a NSGA-II implementation as it's exploration engine, and a heterogeneous multicore CPU
        architecture performance predictor as it's evaluation engine, in order to perform a design space exploration.
    """

    def __init__(self):
        Adapter.__init__(self)

        self.project_path = None

        self.dse_settings_file_name = None

        self.dse_settings = None  # type: Dict[str, Any]

        self.mcpat_results_json_file_name = None

        self.mcpat_results = None

        self.sniper_results_json_file_name = None

        self.sniper_results = None

        self.inputs = {}  # type: Dict[str, Union[Input, InputGroup]]

        self.results = None

        self.presentable_results = None

        self.set_inputs([
            InputGroup({
                'label': "Exploration Space",
                'subtitle': (
                    "Define the limitations for core heterogeneity."
                    + " The platforms produced by the automatic DSE will often contain two different core models."
                    + " You are able to restrict the number of cores used of both models."
                ),
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Minimal number of cores from the original model',
                        'key': 'original_cores_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Number of cores that may be from another model',
                        'key': 'ip_cores_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                ],
            }),
            InputGroup({
                'label': "Constraints",
                'key': 'constraints',
                'inputs': [
                    Input({
                        'label': 'Maximum Power Density',
                        'unit': 'V/mm²',
                        'key': 'maximum_power_density',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'unit': 'mm²',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Technology',
                        'key': 'technology',
                        'allowed_values': Technologies.get_dict(),
                        "is_user_input": False,
                        "required": False,
                    }),
                ],
            }),
        ])

        self.dse_engine = None

    def execute(self):
        self.prepare()

        self.dse_engine.run()

        self.register_results()

    def register_results(self):
        results = {}

        try:
            population_results = json.load(open(self.get_output_path() + "/population_results.json"))

            results['population_results'] = population_results
        except IOError:
            results['population_results'] = None

        try:
            dse_settings = json.load(open(self.get_output_path() + "/dse_settings.json"))

            orig_core = dse_settings['processor'] + '_' + dse_settings['technology']
        except IOError:
            orig_core = None

        self.results = results

        self.presentable_results = {'solutions': {}}

        solution_cores = []

        for s in results['population_results']:
            solution = results['population_results'][s]

            title = (
                str(solution['amount_original_cores'])
                + "x " + orig_core
                + " & " + str(solution['amount_ip_cores'])
                + "x " + solution['core_ip']['id']
            )

            self.presentable_results['solutions'][title] = {
                'title': title,
                'nbr_ip_cores': solution['amount_ip_cores'],
                'nbr_orig_cores': solution['amount_original_cores'],
                'ip_core': solution['core_ip']['id'],
                'orig_core': orig_core,
                'total_nbr_cores': solution['amount_ip_cores'] + solution['amount_original_cores'],
                'total_area': solution['Results']['total_area'],
                'performance': abs(float(solution['Results']['performance_pred'])),
                'power_density': solution['Results']['total_power_density']
            }

    def get_results(self):
        return self.presentable_results

    def prepare(self):
        settings = self.get_settings()

        self.register_profile(settings)

        self.dse_engine = Nsga2Main(settings)

    def register_profile(self, settings):
        profile = {
            'model': settings['dse']['processor'],
            'process': settings['dse']['technology'],
            'frequency': settings['dse']['frequency'],
            'core_area': settings['mcpat_results']['core']['area'],
            'core_number': settings['sniper_results']['ncores'],
            'chip_area': settings['mcpat_results']['processor']['area'],
            'power_density': (
                round(float(settings['mcpat_results']['processor']['power_density'][0]), 2),
                'V/mm^2'
            ),
            'performance': settings['dse']['original_performance'],
            'ds_area': (
                round(float(settings['mcpat_results']['integer_alus']['area_ds'][0]), 2),
                'mm^2'
            ),
            'ds_percentage': (
                round(float(settings['mcpat_results']['integer_alus']['%ds'][0]), 2),
                '%'
            ),
        }

        file_path = self.get_output_path() + "/profile.json"

        with open(file_path, 'w') as profile_json:
            json.dump(profile, profile_json, indent=4)

    def get_settings(self):
        self.read_dse_settings()

        self.read_mcpat_results()

        self.read_sniper_results()

        settings = {
            'project_folder': self.get_project_folder(),
            'mcpat_results': self.mcpat_results,
            'sniper_results': self.sniper_results,
            'dse': self.dse_settings,
        }

        json_dsdse_input_file_path = self.get_output_path() + "/dsdse_input.json"

        with open(json_dsdse_input_file_path, 'w') as json_output_file:
            json.dump(settings, json_output_file, indent=4)

        return settings

    def read_mcpat_results(self):
        self.mcpat_results = json.loads(open(self.get_mcpat_results_json_file_path()).read())

        return self.mcpat_results

    def get_mcpat_results_json_file_path(self):
        if self.mcpat_results_json_file_name is None:
            return self.get_project_folder() + "/mcpat_results.json"

    def read_sniper_results(self):
        self.sniper_results = json.loads(open(self.get_sniper_results_json_file_path()).read())

    def get_sniper_results_json_file_path(self):
        if self.sniper_results_json_file_name is None:
            return self.get_project_folder() + "/sniper_results.json"

        return self.get_project_folder() + "/" + self.sniper_results_json_file_name

    def read_dse_settings(self):
        self.dse_settings = json.loads(open(self.get_dse_settings_file_path()).read())

        self.dse_settings['num_of_generations'] = 150

        self.dse_settings['num_of_individuals'] = 10

        self.dse_settings['mutation_strength'] = 0.5

        self.dse_settings['mutation_rate'] = 0.1

        self.set_dse_settings_from_inputs([
            'exploration_space',
            'constraints',
            'original_cores_for_design',
            'ip_cores_for_design',
            'maximum_power_density',
            'maximum_area',
        ])

    def set_dse_settings_from_inputs(self, keys=None):
        # type: (Optional[List[str]]) -> None
        if self.dse_settings is None:
            self.dse_settings = {}

        for key in self.inputs:
            if (keys is not None) and (key not in keys):
                continue

            if isinstance(self.inputs[key], Input):
                self.dse_settings[key] = self.inputs[key].get_typed_value()
            elif isinstance(self.inputs[key], InputGroup):
                self.dse_settings.update(self.inputs[key].get_dict(None, keys))

    def get_dse_settings_file_path(self):
        return self.get_project_folder() + "/" + self.get_dse_settings_file_name()

    def get_dse_settings_file_name(self):
        if self.dse_settings_file_name is None:
            return "dse_settings.json"

        return self.get_dse_settings_file_name

    def get_project_folder(self):
        if self.project_path is None:
            return self.get_output_path()
