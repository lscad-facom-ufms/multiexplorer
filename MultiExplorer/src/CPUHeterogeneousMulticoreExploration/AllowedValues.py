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
                    "small size and low power consumption, and targeted at new markets including wearable devices.\n"
                    "The model used here is a 32nm process core."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 7,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['1', '400 Mhz', '0.73 W/mm^2', '17.28 s^-1', '5.64 mm^2', '37.88%'],
                        ['2', '400 Mhz', '0.73 W/mm^2', '31.06 s^-1', '11.27 mm^2', '37.96%'],
                        ['4', '400 Mhz', '0.73 W/mm^2', '56.51 s^-1', '22.53 mm^2', '38.02%'],
                        ['8', '400 Mhz', '0.73 W/mm^2', '94.15 s^-1', '45.04 mm^2', '38.07%'],
                        ['16', '400 Mhz', '0.73 W/mm^2', '128.69 s^-1', '90.06 mm^2', '38.1%'],
                        ['32', '400 Mhz', '0.73 W/mm^2', '138.92 s^-1', '180.09 mm^2', '38.12%'],
                    ],
                }
            },
            PredictedCores.Arm53.value: {
                'text': (
                    "The ARM Cortex-A53 is one of the first two central processing units implementing the ARMv8-A "
                    "64-bit instruction set designed by ARM Holdings' Cambridge design centre. The Cortex-A53 is a "
                    "2-wide decode superscalar processor, capable of dual-issuing some instructions.\n"
                    "The model used here is a 22nm process core."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 7,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['1', '1600 Mhz', '1.42 W/mm^2', '181.17 s^-1', '3.2 mm^2', '33.92%'],
                        ['2', '1600 Mhz', '1.42 W/mm^2', '261.43 s^-1', '6.39 mm^2', '33.98%'],
                        ['4', '1600 Mhz', '1.42 W/mm^2', '440.51 s^-1', '12.77 mm^2', '34.2%'],
                        ['8', '1600 Mhz', '1.42 W/mm^2', '553.38 s^-1', '25.53 mm^2', '34.04%'],
                        ['16', '1600 Mhz', '1.42 W/mm^2', '814.24 s^-1', '51.05 mm^2', '34.06%'],
                        ['32', '1600 Mhz', '1.42 W/mm^2', '673.02 s^-1', '102.04 mm^2', '34.02%'],
                    ],
                }
            },
            PredictedCores.Arm57.value: {
                'text': (
                    "The ARM Cortex-A57 is a central processing unit implementing the ARMv8-A 64-bit instruction set "
                    "designed by ARM Holdings. The Cortex-A57 is an out-of-order superscalar pipeline.\n"
                    "The model used here is a 22nm process core."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 7,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['1', '1960 Mhz', '1.61 W/mm^2', '201.38 s^-1', '3.13 mm^2', '33.23%'],
                        ['2', '1960 Mhz', '1.61 W/mm^2', '334.61 s^-1', '6.26 mm^2', '33.29%'],
                        ['4', '1960 Mhz', '1.61 W/mm^2', '505.02 s^-1', '12.51 mm^2', '33.33%'],
                        ['8', '1960 Mhz', '1.62 W/mm^2', '672.83 s^-1', '25.02 mm^2', '33.36%'],
                        ['16', '1960 Mhz', '1.62 W/mm^2', '935.56 s^-1', '50.02 mm^2', '33.38%'],
                        ['32', '1960 Mhz', '1.62 W/mm^2', '687.75 s^-1', '100 mm^2', '33.35%'],
                    ],
                }
            },
            PredictedCores.Atom.value: {
                'text': (
                    "Silvermont is a microarchitecture for low-power Atom, Celeron and Pentium branded processors "
                    "used in systems on a chip made by Intel.\n"
                    "The model used here is a 22nm process core."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 7,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['1', '500 Mhz', '0.95 W/mm^2', '19.39 s^-1', '0 mm^2', '0%'],
                        ['2', '500 Mhz', '0.95 W/mm^2', '34.15 s^-1', '0 mm^2', '0%'],
                        ['4', '500 Mhz', '0.95 W/mm^2', '61.61 s^-1', '0 mm^2', '0%'],
                        ['8', '500 Mhz', '0.95 W/mm^2', '98.32 s^-1', '0 mm^2', '0%'],
                        ['16', '500 Mhz', '0.95 W/mm^2', '145.54 s^-1', '0 mm^2', '0%'],
                        ['32', '500 Mhz', '0.95 W/mm^2', '152.54 s^-1', '0 mm^2', '0%'],
                    ],
                }
            },
            PredictedCores.Smithfield.value: {
                'text': (
                    "Pentium D[2] is a range of desktop 64-bit x86-64 processors based on the NetBurst "
                    "microarchitecture, which is the dual-core variant of the Pentium 4 manufactured by Intel. Each "
                    "CPU comprised two dies, each containing a single core, residing next to each other on a "
                    "multi-chip module package.\n"
                    "The model used here is a 90nm process core."
                ),
                'table_data': {
                    'nbr_of_columns': 6,
                    'nbr_of_rows': 7,
                    'data': [
                        ['# Cores', 'Frequency', 'Power Density', 'Performance', 'DS Area', 'DS%'],
                        ['1', '2800 Mhz', '0.25 W/mm^2', '310.25 s^-1', '0 mm^2', '0%'],
                        ['2', '2800 Mhz', '0.24 W/mm^2', '463.81 s^-1', '0 mm^2', '0%'],
                        ['4', '2800 Mhz', '0.25 W/mm^2', '657.80 s^-1', '0 mm^2', '0%'],
                        ['8', '2800 Mhz', '0.25 W/mm^2', '807.18 s^-1', '0 mm^2', '0%'],
                        ['16', '2800 Mhz', '0.25 W/mm^2', '973.25 s^-1', '0 mm^2', '0%'],
                        ['32', '2800 Mhz', '0.25 W/mm^2', '916.08 s^-1', '0 mm^2', '0%'],
                    ],
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
    def belongs(value):
        return value in set(item.value for item in CachePolicies)

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
    def belongs(value):
        return value in set(item.value for item in PerformanceModelTypes)

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
    def belongs(value):
        return value in set(item.value for item in HashTypes)

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
    def belongs(value):
        return value in set(item.value for item in Domains)

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
    def belongs(value):
        return value in set(item.value for item in Prefetchers)

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
    def belongs(value):
        return value in set(item.value for item in DramDirectoryTypes)

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
    def belongs(value):
        return value in set(item.value for item in DramDirectoryTypes)

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
    NINETY_NANOMETERS = "90"
    SIXTY_FIVE_NANOMETERS = "65"
    FOURTY_FIVE_NANOMETERS = "45"
    THIRTY_TWO_NANOMETERES = "32"
    TWENTY_TWO_NANOMETERS = "22"

    @staticmethod
    def belongs(value): return value in set(item.value for item in Technologies)

    @staticmethod
    def get_label(value):
        if value == Technologies.NINETY_NANOMETERS:
            return "90"
        elif value == Technologies.SIXTY_FIVE_NANOMETERS:
            return "65"
        elif value == Technologies.FOURTY_FIVE_NANOMETERS:
            return "45"
        elif value == Technologies.THIRTY_TWO_NANOMETERES:
            return "32"
        elif value == Technologies.TWENTY_TWO_NANOMETERS:
            return "22"

        raise ValueError("Value does not corresponds to a known hash type.")

    @staticmethod
    def get_dict():
        return {
            Technologies.NINETY_NANOMETERS.value: Technologies.get_label(Technologies.NINETY_NANOMETERS),
            Technologies.SIXTY_FIVE_NANOMETERS.value: Technologies.get_label(Technologies.SIXTY_FIVE_NANOMETERS),
            Technologies.FOURTY_FIVE_NANOMETERS.value: Technologies.get_label(Technologies.FOURTY_FIVE_NANOMETERS),
            Technologies.THIRTY_TWO_NANOMETERES.value: Technologies.get_label(Technologies.THIRTY_TWO_NANOMETERES),
            Technologies.TWENTY_TWO_NANOMETERS.value: Technologies.get_label(Technologies.TWENTY_TWO_NANOMETERS),
        }


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
