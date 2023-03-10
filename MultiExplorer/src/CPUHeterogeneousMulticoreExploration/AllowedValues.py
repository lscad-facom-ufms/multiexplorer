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
    Smithfield = 5

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
        elif value == PredictedCores.Smithfield:
            return "Smithfield"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_dict():
        return {
            PredictedCores.Quark.value: PredictedCores.get_label(PredictedCores.Quark),
            PredictedCores.Arm53.value: PredictedCores.get_label(PredictedCores.Arm53),
            PredictedCores.Arm57.value: PredictedCores.get_label(PredictedCores.Arm57),
            PredictedCores.Atom.value: PredictedCores.get_label(PredictedCores.Atom),
            PredictedCores.Smithfield.value: PredictedCores.get_label(PredictedCores.Smithfield),
        }

    @staticmethod
    def get_info_dict():
        # todo
        return {
            PredictedCores.Quark.value: {
                'text': (
                    "Intel Quark (400 Mhz) is a line of 32-bit x86 SoCs and microcontrollers by Intel, "
                    "designed for"
                    + "small size and low power consumption, and targeted at new markets including wearable devices ("
                      "process 32 nm).\n"
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 2,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['4', '1000 Mhz', '42.05 mm^2', '1.05 W/mm^2', '83.68 s^-1', '21.78 mm^2', '36.77%'],
                    ]
                }
            },
            PredictedCores.Arm53.value: {
                'text': (
                    "The ARM Cortex-A53 is one of the first two central processing units implementing the ARMv8-A "
                    "64-bit instruction set designed by ARM Holdings' Cambridge design centre. The Cortex-A53 is a "
                    "2-wide decode superscalar processor, capable of dual-issuing some instructions (process 22 nm)."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 2,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['8', '2500 Mhz', '45.69 mm^2', '1.89 W/mm^2', '706.98 s^-1', '-', '-'],
                    ]
                }
            },
            PredictedCores.Arm57.value: {
                'text': (
                    "The ARM Cortex-A57 is a central processing unit implementing the ARMv8-A 64-bit instruction set "
                    "designed by ARM Holdings. The Cortex-A57 is an out-of-order superscalar pipeline (process 22 nm)."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 2,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['16', '3500 Mhz', '91 mm^2', '2.40 W/mm^2', '1241.01 s^-1', '-', '-'],
                    ]
                }
            },
            PredictedCores.Atom.value: {
                'text': (
                    "Silvermont is a microarchitecture for low-power Atom, Celeron and Pentium branded processors "
                    "used in systems on a chip made by Intel (process 22 nm)."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 2,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['32', '5000 Mhz', '182.76 mm^2', '3.75 W/mm^2', '254.15 s^-1', '-', '-'],
                    ]
                }
            },
            PredictedCores.Smithfield.value: {
                'text': (
                    "Pentium D[2] is a range of desktop 64-bit x86-64 processors based on the NetBurst "
                    "microarchitecture, which is the dual-core variant of the Pentium 4 manufactured by Intel. Each "
                    "CPU comprised two dies, each containing a single core, residing next to each other on a "
                    "multi-chip module package (process 65 nm)."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 2,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['4', '1000 Mhz', '42.05 mm^2', '1.05 W/mm^2', '83.68 s^-1', '21.78 mm^2', '36.77%'],
                    ]
                }
            },
        }

    @staticmethod
    def get_processor(value):
        # type: (int) -> str
        if value == PredictedCores.Quark.value:
            return "Quark_x1000"
        elif value == PredictedCores.Arm53.value:
            return "ARM_A53"
        elif value == PredictedCores.Arm57.value:
            return "ARM_A57"
        elif value == PredictedCores.Atom.value:
            return "Atom_Silvermont"
        elif value == PredictedCores.Smithfield.value:
            return "Smithfield"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_technology(value):
        # type: (int) -> str
        if value == PredictedCores.Quark.value:
            return "32nm"
        elif value == PredictedCores.Arm53.value:
            return "22nm"
        elif value == PredictedCores.Arm57.value:
            return "22nm"
        elif value == PredictedCores.Atom.value:
            return "22nm"
        elif value == PredictedCores.Smithfield.value:
            return "90nm"

        raise ValueError("Value does not corresponds to a known predicted core.")

    @staticmethod
    def get_cfg_path(value):
        if value == PredictedCores.Quark.value:
            return PATH_INPUTS + "/quark.cfg"
        elif value == PredictedCores.Arm53.value:
            return PATH_INPUTS + "/armA53.cfg"
        elif value == PredictedCores.Arm57.value:
            return PATH_INPUTS + "/armA57.cfg"
        elif value == PredictedCores.Atom.value:
            return PATH_INPUTS + "/atom.cfg"
        elif value == PredictedCores.Smithfield.value:
            return PATH_INPUTS + "/smithfield.cfg"

        raise ValueError("Can't find default sniper configuration file for unknown/unpredicted cores.")

    @staticmethod
    def get_json_path(value):
        if value == PredictedCores.Quark.value:
            return PATH_INPUTS + "/quark.json"
        elif value == PredictedCores.Arm53.value:
            return PATH_INPUTS + "/armA53.json"
        elif value == PredictedCores.Arm57.value:
            return PATH_INPUTS + "/armA57.json"
        elif value == PredictedCores.Atom.value:
            return PATH_INPUTS + "/atom.json"
        elif value == PredictedCores.Smithfield.value:
            return PATH_INPUTS + "/smithfield.json"

        raise ValueError("Can't find default input json file for unknown/unpredicted cores.")

    @staticmethod
    def get_original_frequency(value):
        if value == PredictedCores.Quark.value:
            return 0.4
        elif value == PredictedCores.Arm53.value:
            return 1.6
        elif value == PredictedCores.Arm57.value:
            return 2.0
        elif value == PredictedCores.Atom.value:
            return 0.5
        elif value == PredictedCores.Smithfield.value:
            return 2.8

    @staticmethod
    def get_power(value):
        if value == PredictedCores.Quark.value:
            return 0.690
        elif value == PredictedCores.Arm53.value:
            return 1.39117
        elif value == PredictedCores.Arm57.value:
            return 1.59445
        elif value == PredictedCores.Atom.value:
            return 0.830237
        elif value == PredictedCores.Smithfield.value:
            return 0.439832

    @staticmethod
    def get_area(value):
        if value == PredictedCores.Quark.value:
            return 15.692
        elif value == PredictedCores.Arm53.value:
            return 10.5853
        elif value == PredictedCores.Arm57.value:
            return 10.5023
        elif value == PredictedCores.Atom.value:
            return 8.19052
        elif value == PredictedCores.Smithfield.value:
            return 111.117

    @staticmethod
    def get_original_performance(value):
        if value == PredictedCores.Quark.value:
            return 502.53
        elif value == PredictedCores.Arm53.value:
            return 3125.68
        elif value == PredictedCores.Arm57.value:
            return 4006.64
        elif value == PredictedCores.Atom.value:
            return 648.47
        elif value == PredictedCores.Smithfield.value:
            return 6428


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

    def to_cfg(self):
        if self.value == "LRU":
            return "lru"


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
            PerformanceModelTypes.Parallel.value: PerformanceModelTypes.get_label(PerformanceModelTypes.Parallel)
        }

    @staticmethod
    def from_json(value):
        if value == 'parallel':
            return PerformanceModelTypes.Parallel

        raise ValueError("Unknown performance model type.")

    def to_cfg(self):
        if self.value == "parallel":
            return "parallel"


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
            HashTypes.Mask.value: HashTypes.get_label(HashTypes.Mask)
        }

    @staticmethod
    def from_json(value):
        if value == 'mask':
            return HashTypes.Mask

        raise ValueError("Unknown performance model type.")

    def to_cfg(self):
        if self.value == "mask":
            return "mask"

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
            Domains.Core.value: Domains.get_label(Domains.Core)
        }

    @staticmethod
    def from_json(value):
        if value == "core":
            return Domains.Core

        raise ValueError("Unknown domain.")

    def to_cfg(self):
        if self.value == "core":
            return "core"


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
            Prefetchers.NA.value: Prefetchers.get_label(Prefetchers.NA)
        }

    @staticmethod
    def from_json(value):
        if value == "none":
            return Prefetchers.NA

        raise ValueError("Unknown prefetching mechanism.")

    def to_cfg(self):
        if self.value == "none":
            return "none"


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
            DramDirectoryTypes.FULL_MAP.value: DramDirectoryTypes.get_label(DramDirectoryTypes.FULL_MAP)
        }

    @staticmethod
    def from_json(value):
        if value == "full_map":
            return DramDirectoryTypes.FULL_MAP

        raise ValueError("Unknown DRAM directory type.")

    def to_cfg(self):
        if self.value == "full_map":
            return "full_map"


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
            MemoryModels.BUS.value: MemoryModels.get_label(MemoryModels.BUS)
        }

    @staticmethod
    def from_json(value):
        if value == "bus":
            return MemoryModels.BUS

        raise ValueError("Unknown memory model.")

    def to_cfg(self):
        if self.value == "bus":
            return "bus"


class Technologies(Enum):
    TWENTY_TWO_NANOMETERS = "22nm"

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
            Technologies.TWENTY_TWO_NANOMETERS.value: Technologies.get_label(Technologies.TWENTY_TWO_NANOMETERS)
        }


class Applications(Enum):
    SPLASH_II_CHOLESKY = "splash2-cholesky"

    @staticmethod
    def belongs(value): return value in set(item.value for item in Applications)

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
    