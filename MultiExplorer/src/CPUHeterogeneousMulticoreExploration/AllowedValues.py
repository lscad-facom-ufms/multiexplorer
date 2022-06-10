from enum import Enum

from MultiExplorer.src.config import PATH_INPUTS


class Simulators(Enum):
    Sniper = 1

    @staticmethod
    def belongs(value): return value in set(item.value for item in Simulators)

    @staticmethod
    def get_label(value):
        if value == Simulators.Sniper:
            return "Sniper Multi-Core Simulator"

        raise ValueError("Value does not corresponds to a known simulator.")


class PredictedCores(Enum):
    Quark = 1
    Arm53 = 2
    Arm57 = 3
    Atom = 4

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in PredictedCores)

    @staticmethod
    def get_label(value):
        if value == PredictedCores.Quark:
            return "Quark x1000"
        elif value == PredictedCores.Arm53:
            return "ARM A53"
        elif value == PredictedCores.Arm57:
            return "ARM A57"
        elif value == PredictedCores.Atom:
            return "Atom Silvermont"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_cfg_path(value):
        if value == PredictedCores.Quark:
            return PATH_INPUTS + "/quark.cfg"


class SniperCorePipelineKinds(Enum):
    Shared = "Shared"
    TimeSlice = "TimeSlice"

    @staticmethod
    def belongs(value):
        return value in set(item.value for item in SniperCorePipelineKinds)

    @staticmethod
    def get_label(value):
        if value == SniperCorePipelineKinds.Shared:
            return "Shared"
        elif value == SniperCorePipelineKinds.TimeSlice:
            return "Time Slice"

        raise ValueError("Value does not corresponds to a known mode of pipeline components.")


class CachePolicies(Enum):
    LRU = "LRU"

    @staticmethod
    def belongs(value): return value in set(item.value for item in CachePolicies)

    @staticmethod
    def get_label(value):
        if value == CachePolicies.LRU:
            return "LRU"

        raise ValueError("Value does not corresponds to a known mode of cache policy.")


class PerformanceModelTypes(Enum):
    Parallel = "parallel"

    @staticmethod
    def belongs(value): return value in set(item.value for item in PerformanceModelTypes)

    @staticmethod
    def get_label(value):
        if value == PerformanceModelTypes.Parallel:
            return "Parallel"

        raise ValueError("Value does not corresponds to a known type of performance model.")

    @staticmethod
    def get_dict():
        return {
            PerformanceModelTypes.Parallel: PerformanceModelTypes.get_label(PerformanceModelTypes.Parallel)
        }


class HashTypes(Enum):
    Mask = "mask"

    @staticmethod
    def belongs(value): return value in set(item.value for item in HashTypes)

    @staticmethod
    def get_label(value):
        if value == HashTypes.Mask:
            return "Mask"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            HashTypes.Mask: HashTypes.get_label(HashTypes.Mask)
        }


class Domains(Enum):
    Core = "core"

    @staticmethod
    def belongs(value): return value in set(item.value for item in Domains)

    @staticmethod
    def get_label(value):
        if value == Domains.Core:
            return "Core"

        raise ValueError("Value does not corresponds to a known domain.")

    @staticmethod
    def get_dict():
        return {
            Domains.Core: Domains.get_label(Domains.Core)
        }


class Prefetchers(Enum):
    NA = "none"

    @staticmethod
    def belongs(value): return value in set(item.value for item in Prefetchers)

    @staticmethod
    def get_label(value):
        if value == Prefetchers.NA:
            return "None"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            Prefetchers.NA: Prefetchers.get_label(Prefetchers.NA)
        }


class DramDirectoryTypes(Enum):
    FULL_MAP = "full_map"

    @staticmethod
    def belongs(value): return value in set(item.value for item in DramDirectoryTypes)

    @staticmethod
    def get_label(value):
        if value == DramDirectoryTypes.FULL_MAP:
            return "None"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            DramDirectoryTypes.FULL_MAP: DramDirectoryTypes.get_label(DramDirectoryTypes.FULL_MAP)
        }


class MemoryModels(Enum):
    BUS = "bus",

    @staticmethod
    def belongs(value): return value in set(item.value for item in DramDirectoryTypes)

    @staticmethod
    def get_label(value):
        if value == MemoryModels.BUS:
            return "Memory Bus"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            MemoryModels.BUS: MemoryModels.get_label(MemoryModels.BUS)
        }


class Technologies(Enum):
    TWENTY_TWO_NANOMETERS = "22nm",

    @staticmethod
    def belongs(value): return value in set(item.value for item in Technologies)

    @staticmethod
    def get_label(value):
        if value == Technologies.TWENTY_TWO_NANOMETERS:
            return "22nm"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            Technologies.TWENTY_TWO_NANOMETERS: Technologies.get_label(Technologies.TWENTY_TWO_NANOMETERS)
        }


class Applications(Enum):
    ALL = "All",

    @staticmethod
    def belongs(value): return value in set(item.value for item in Applications)

    @staticmethod
    def get_label(value):
        if value == Applications.ALL:
            return "All"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            Applications.ALL: Applications.get_label(Applications.ALL)
        }
    