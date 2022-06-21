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

        if value == PredictedCores.Arm53:
            return PATH_INPUTS + "/armA53.cfg"

        if value == PredictedCores.Arm57:
            return PATH_INPUTS + "/armA57.cfg"

        if value == PredictedCores.Atom:
            return PATH_INPUTS + "/atom.cfg"

        raise ValueError("Can't find default sniper configuration file for unknown/unpredicted cores.")

    @staticmethod
    def get_json_path(value):
        if value == PredictedCores.Quark:
            return PATH_INPUTS + "/quark.json"

        if value == PredictedCores.Arm53:
            return PATH_INPUTS + "/armA53.json"

        if value == PredictedCores.Arm57:
            return PATH_INPUTS + "/armA57.json"

        if value == PredictedCores.Atom:
            return PATH_INPUTS + "/atom.json"

        raise ValueError("Can't find default input json file for unknown/unpredicted cores.")


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

    @staticmethod
    def from_json(value):
        if value == "LRU":
            return CachePolicies.LRU

        raise ValueError("Unknown cache policy.")


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

    @staticmethod
    def from_json(value):
        if value == 'parallel':
            return PerformanceModelTypes.Parallel

        raise ValueError("Unknown performance model type.")



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

    @staticmethod
    def from_json(value):
        if value == 'mask':
            return HashTypes.Mask

        raise ValueError("Unknown performance model type.")


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

    @staticmethod
    def from_json(value):
        if value == "core":
            return Domains.Core

        raise ValueError("Unknown domain.")


class Prefetchers(Enum):
    NA = "none"

    @staticmethod
    def belongs(value): return value in set(item.value for item in Prefetchers)

    @staticmethod
    def get_label(value):
        if value == Prefetchers.NA:
            return "None"

        raise ValueError("Value does not corresponds to a known prefetching mechanism.")

    @staticmethod
    def get_dict():
        return {
            Prefetchers.NA: Prefetchers.get_label(Prefetchers.NA)
        }

    @staticmethod
    def from_json(value):
        if value == "none":
            return Prefetchers.NA

        raise ValueError("Unknown prefetching mechanism.")


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

    @staticmethod
    def from_json(value):
        if value == "full_map":
            return DramDirectoryTypes.FULL_MAP

        raise ValueError("Unknown DRAM directory type.")


class MemoryModels(Enum):
    BUS = "bus"

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

    @staticmethod
    def from_json(value):
        if value == "bus":
            return MemoryModels.BUS

        raise ValueError("Unknown memory model.")


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
    