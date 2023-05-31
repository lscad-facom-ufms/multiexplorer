from enum import Enum

from MultiExplorer.src.config import PATH_INPUTS
"""
Modelos - c5, m5 e r5
Aplicações - 0 a 26

C5 - define o valor do mips
c5.24large - define price, coresVM e memory
c5.24large-18 - define a aplicação

Informações necessárias para executar no cloudsim:
mips, coreVM e memory
instructions for design(aplicação), 
cores cloudlet for design

Depois de executar o cloudlet calcula o tempo e devolve
o custo é o tempo que o cloudsim devolveu vezes o preço 
que vem no modelo

Inicialmente, colocar apenas a VM c5 
e as aplicações de 0 a 3

?
Em qual arquivo que eu posso encontrar onde muda na
interface gráfica?



"""
class Simulators(Enum):
    Cloudsim = 1

    @staticmethod
    def belongs(value): return value in set(item.value for item in Simulators)

    @staticmethod
    def get_label(value):
        if value == Simulators.Cloudsim:
            return "Cloudsim Simulator"

        raise ValueError("Value does not corresponds to a known simulator.")


class PredictedModels(Enum):
    c5 = 1
    c5x = 2
    c5x2 = 3

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedModels)

    @staticmethod
    def get_label(value):
        if value == PredictedModels.c5:
            return "c5.large"
        if value == PredictedModels.c5x:
            return "c5.xlarge"
        if value == PredictedModels.c5x2:
            return "c5.2xlarge"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedModels.c5.value: PredictedModels.get_label(PredictedModels.c5),
            PredictedModels.c5x.value: PredictedModels.get_label(PredictedModels.c5x),
            PredictedModels.c5x2.value: PredictedModels.get_label(PredictedModels.c5x2),
        }
    
    @staticmethod
    def get_model(value):
        # type: (int) -> str
        if value == PredictedModels.c5.value:
            return "c5.large"
        elif value == PredictedModels.c5x.value:
            return "c5.xlarge"
        elif value == PredictedModels.c5x2.value:
            return "c5.2xlarge"

        raise ValueError("Value does not corresponds to a known predicted core.")

    def get_mips(value):
        return 72
    
    def get_coresVM(value):
        if value == PredictedModels.c5.value:
            return 2
        elif value == PredictedModels.c5x.value:
            return 4
        elif value == PredictedModels.c5x2.value:
            return 8
    
    def get_price(value):
        if value == PredictedModels.c5.value:
            return 0.085
        elif value == PredictedModels.c5x.value:
            return 0.17
        elif value == PredictedModels.c5x2.value:
            return 0.34
    
    def get_memory(value):
        if value == PredictedModels.c5.value:
            return 4000
        elif value == PredictedModels.c5x.value:
            return 8000
        elif value == PredictedModels.c5x2.value:
            return 16000

class PredictedApplications(Enum):
    EPS = 1
    EPW = 2
    EPA = 3

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedApplications)

    @staticmethod
    def get_label(value):
        if value == PredictedApplications.EPS:
            return "EP-S"
        if value == PredictedApplications.EPW:
            return "EP-W"
        if value == PredictedApplications.EPA:
            return "EP-A"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedApplications.EPS.value: PredictedApplications.get_label(PredictedApplications.EPS),
            PredictedApplications.EPW.value: PredictedApplications.get_label(PredictedApplications.EPW),
            PredictedApplications.EPA.value: PredictedApplications.get_label(PredictedApplications.EPA),
        }
    
    @staticmethod
    def get_application(value):
        # type: (int) -> str
        if value == PredictedApplications.EPS.value:
            return "EP-S"
        elif value == PredictedApplications.EPW.value:
            return "EP-W"
        elif value == PredictedApplications.EPA.value:
            return "EP-A"

        raise ValueError("Value does not corresponds to a known predicted core.")

    def get_instructions_for_design(value):
        if value == PredictedApplications.EPS.value:
            return 581290490
        elif value == PredictedApplications.EPW.value:
            return 1162275455
        elif value == PredictedApplications.EPA.value:
            return 9235513739
        

class Applications(Enum):
    SPLASH_II_CHOLESKY = "splash2-cholesky"

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in Applications)

    @staticmethod
    def get_label(value):
        if value == Applications.SPLASH_II_CHOLESKY:
            return "Splash II - Cholesky"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            Applications.SPLASH_II_CHOLESKY.value: Applications.get_label(Applications.SPLASH_II_CHOLESKY)
        }

    def to_cfg(self):
        if self.value == "splash2-cholesky":
            return "splash2-cholesky"
