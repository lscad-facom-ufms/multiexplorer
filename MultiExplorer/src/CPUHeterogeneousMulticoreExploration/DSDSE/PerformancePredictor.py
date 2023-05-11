import json
import os
from typing import Dict
from sklearn.externals import joblib


class PerformancePredictor(object):
    default_settings = {
        'bd_json_file_path': os.path.dirname(os.path.realpath(__file__)) + "/predictors/bdPredictor.json",
        'preditor_pkl_file_path': os.path.dirname(os.path.realpath(__file__)) + "/predictors/preditor.pkl",
        'scalator_pkl_file_path': os.path.dirname(os.path.realpath(__file__)) + "/predictors/scaler.pkl",
    }

    def __init__(self, settings):
        # type: (Dict) -> None
        """
            Dict settings {
                Opt[str] "ip_processor": bd key for the imported core model (for a heterogeneous architecture)
                    assumed to follow the pattern "ProcessorName_TechnologyNm",
                Opt[int] "ip_core_nbr": number of imported cores (for a heterogeneous architecture),
                Opt[str] "orig_processor": bd key for the original core model of the proposed architecture
                    assumed to follow the pattern "ProcessorName_TechnologyNm",
                Opt[int] "orig_core_nbr": number of original cores,
                Opt[float] "orig_frequency": float value (in Ghz) of the original core model's frequency
                    in the proposed architecture,
                Opt[str] "bd_json_file_path": path to the json containing the database for the predictor,
                Opt[str] "preditor_pkl_file_path": path to the file of the pickled predictor object,
                Opt[str] "scalator_pkl_file_path": path to the file o f the pickled scalator object,
            }
        """
        merged_settings = PerformancePredictor.default_settings.copy()

        merged_settings.update(settings)

        self.bd = json.load(open(merged_settings['bd_json_file_path']))

        self.preditor = joblib.load(merged_settings['preditor_pkl_file_path'])

        self.scalator = joblib.load(merged_settings['scalator_pkl_file_path'])

        self.ip_frequency = None

        if 'ip_processor' in merged_settings:
            self.ip_processor = merged_settings['ip_processor']

            self.ip_frequency = float(self.bd[str(self.ip_processor)][0]["freq"])

        self.ip_core_nbr = None

        if 'ip_core_nbr' in merged_settings:
            self.ip_core_nbr = merged_settings['ip_core_nbr']

        self.orig_processor = merged_settings['orig_processor']

        self.orig_core_nbr = merged_settings['orig_core_nbr']

        self.orig_frequency = merged_settings['orig_frequency']

        self.cpi = float(self.bd[str(self.orig_processor)][0][str(self.orig_core_nbr)])

        if self.ip_core_nbr is not None and self.ip_frequency is not None:
            self.frequency_ratio = PerformancePredictor.get_frequency_ratio(
                self.ip_core_nbr,
                self.ip_frequency,
                self.orig_core_nbr,
                self.orig_frequency
            )

    @staticmethod
    def get_frequency_ratio(ip_core_nbr, ip_frequency, orig_core_nbr, orig_frequency):
        total_ip_frequency = float(ip_core_nbr) * float(ip_frequency)

        total_orig_frequency = float(orig_core_nbr) * orig_frequency

        total_frequency = total_ip_frequency + total_orig_frequency

        return total_ip_frequency / total_frequency

    def set_original_processor(self, orig_bd_key, alt_frequency=None):
        self.orig_processor = orig_bd_key

        if alt_frequency is None:
            self.orig_frequency = float(self.bd[str(orig_bd_key)][0]["freq"])
        else:
            self.orig_frequency = alt_frequency

    def set_imported_processor(self, ip_bd_key):
        self.ip_processor = ip_bd_key

        self.ip_frequency = float(self.bd[str(ip_bd_key)][0]["freq"])

    def get_results(self):  # chamada feita depois de setar os 2 processadores
        total = int(self.orig_core_nbr) + int(self.ip_core_nbr)

        self.cpi = float(self.bd[str(self.ip_processor)][0][str(self.ip_core_nbr)])

        self.frequency_ratio = PerformancePredictor.get_frequency_ratio(
            self.ip_core_nbr,
            self.ip_frequency,
            self.orig_core_nbr,
            self.orig_frequency
        )

        teste = [[
            self.orig_core_nbr,
            self.ip_core_nbr,
            total,
            self.cpi,
            self.orig_frequency,
            self.frequency_ratio,
        ]]  # monta o teste

        testes = self.scalator.transform(teste)  # escalona os parametros

        resp = self.preditor.predict(testes)  # prediz desempenho core self.nbr_ip_core

        self.cpi = float(self.bd[str(self.orig_processor)][0][str(self.orig_core_nbr)])

        teste = [[
            self.ip_core_nbr,
            self.orig_core_nbr,
            total,
            self.cpi,
            self.orig_frequency,
            float(1.0 - self.frequency_ratio)
        ]]

        testes = self.scalator.transform(teste)

        resp2 = self.preditor.predict(testes)  # prediz desempenho core self.nbr_orig_core

        if resp2 < resp:
            resp = resp2

        return str(round(float(resp[0]), 3))  # pior desempenho sera retornado

    def get_results_l(self, ip_core_nbr, orig_core_nbr):  # chamada feita passando os 2 processadores
        total = int(orig_core_nbr) + int(ip_core_nbr)

        self.cpi = float(self.bd[str(self.ip_processor)][0][str(ip_core_nbr)])

        self.frequency_ratio = PerformancePredictor.get_frequency_ratio(
            ip_core_nbr,
            self.ip_frequency,
            orig_core_nbr,
            self.orig_frequency
        )

        teste = [[
            orig_core_nbr,
            ip_core_nbr,
            total,
            self.cpi,
            self.orig_frequency,
            self.frequency_ratio
        ]]  # monta o teste

        testes = self.scalator.transform(teste)  # escalona os parametros
        resp = self.preditor.predict(testes)  # prediz desempenho core IP

        self.cpi = float(self.bd[str(self.orig_processor)][0][str(orig_core_nbr)])

        teste = [[
            ip_core_nbr,
            orig_core_nbr,
            total,
            self.cpi,
            self.orig_frequency,
            float(1.0 - self.frequency_ratio),
        ]]

        testes = self.scalator.transform(teste)
        resp2 = self.preditor.predict(testes)  # prediz desempenho core Original

        if resp2 < resp:
            resp = resp2

        return str(round(float(resp[0]), 3))
