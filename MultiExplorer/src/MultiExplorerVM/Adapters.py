# -*- coding: utf-8 -*-
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
            InputGroup({
                'label': "Application",
                'key': 'application',
                "inputs": [
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
                        "allowed_values" : PredictedApplications.get_dict(),
                    }),
                ]
            }),
            InputGroup({
                'label': "Constraints",
                'key': 'constraints',
                "inputs": [
                    Input({
                       'label': 'Maximum Cost',
                        'key': 'maximum_cost',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Maximum Time',
                        'key': 'maximum_time',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                ]
            })
        ])

        self.config = {}

        self.results = {}

        self.presentable_results = None

        self.use_benchmarks = True

        self.benchmark_size = None

        self.dse_settings_file_name = None

        self.cfg_path = None

        self.output_path = None


    def set_values_from_json(self, absolute_file_path):
        """
        This method reads a json file and sets the values of the inputs.
        """
        input_json = json.loads(open(absolute_file_path).read())

# Organizar os sets para o json

""""
criar um get para juntar as infos 
"""

class NsgaIIPredDSEAdapter(Adapter):
    """
        For VM.
    """

    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            InputGroup({
                'label': "Exploration Space",
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Cores Cloudlet for design',
                        'key': 'corescloudlet_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.Integer,
                        'max_val': 32,
                    }),
                    Input({
                        'label': 'Original number VM for design',
                        'key': 'original_vm_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Suplementar number VM for design',
                        'key': 'sup_vm_for_design',
                        "is_user_input": True,
                        "required": True,
                        "type": InputType.IntegerRange,
                        "min_val": 1,
                        "max_val": 32,
                    })
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

        self.presentable_results = {
            'profile': self.profile,
            'solutions': {},
        }

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

        self.register_db(settings)

        self.dse_engine = Nsga2Main(settings)

    def register_profile(self, settings):
        self.profile = {
            'model': settings['dse']['processor'],
            'process': settings['dse']['technology'],
            'frequency': settings['dse']['frequency'],
            'core_area': settings['mcpat_results']['total_cores']['area'],
            'core_number': settings['sniper_results']['ncores'],
            'power': settings['mcpat_results']['processor']['peak_power'],
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
            json.dump(self.profile, profile_json, indent=4)

    def register_db(self, settings):
        nbr_of_cores = settings['sniper_results']['ncores']

        total_ic = 0

        for ic in settings['sniper_results']['performance_model.instruction_count']:
            total_ic += ic

        self.db = {
            'id': settings['dse']['processor'] + settings['dse']['technology'],
            'pow': round(float(settings['mcpat_results']['processor']['peak_power'][0]) / nbr_of_cores, 2),
            'area': round(float(settings['mcpat_results']['processor']['area'][0]) / nbr_of_cores, 2),
            'perf': round(float(settings['dse']['original_performance'][0]) / nbr_of_cores, 2),
            'freq': settings['dse']['frequency'],
            'cpi': round(settings['sniper_results']['performance_model.cycle_count'][0] / total_ic, 10),
        }

        file_path = self.get_output_path() + "/db.json"

        with open(file_path, 'w') as db_json:
            json.dump(self.db, db_json, indent=4)

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

        self.set_dse_settings_from_inputs([
            'num_of_generations',
            'num_of_individuals',
            'mutation_strength',
            'mutation_rate',
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

        self.dse_settings['num_of_generations'] = int(self.inputs['nsga_parameters']['num_of_generations'])
        self.dse_settings['num_of_individuals'] = int(self.inputs['nsga_parameters']['num_of_individuals'])
        self.dse_settings['mutation_strength'] = float(self.inputs['nsga_parameters']['mutation_strength'])
        self.dse_settings['mutation_rate'] = float(self.inputs['nsga_parameters']['mutation_rate'])

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
