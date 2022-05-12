from enum import Enum


class Simulators(Enum):
    Simulator = 0
    Sniper = 1

    @staticmethod
    def belongs(value):
        return value in range(0, 1)

    @staticmethod
    def get_label(value):
        if value == 1:
            return "Sniper Multi-Core Simulator"

        raise ValueError("Value does not corresponds to a known simulator.")


class PredictedCores(Enum):
    Quark = 1
    Arm53 = 2
    Arm57 = 3
    Atom = 4

    @staticmethod
    def belongs(value):
        return value in range(1, 4)

    @staticmethod
    def get_label(value):
        if value == 1:
            return "Quark x1000"
        elif value == 2:
            return "ARM A53"
        elif value == 3:
            return "ARM A57"
        elif value == 4:
            return "Atom Silvermont"

        raise ValueError("Value does not corresponds to a known predicted core.")


class SniperCorePipelineKinds(Enum):
    Shared = "Shared"
    TimeSlice = "TimeSlice"

    @staticmethod
    def belongs(value):
        return value in ["Shared", "TimeSlice"]

    @staticmethod
    def get_label(value):
        if value == "Shared":
            return "Shared"
        elif value == "TimeSlice":
            return "Time Slice"

        raise ValueError("Value does not corresponds to a known mode of pipeline components.")


class CachePolicies(Enum):
    LRU = "LRU"

    @staticmethod
    def belongs(value):
        return value in ["LRU"]

    @staticmethod
    def get_label(value):
        if value == "LRU":
            return "LRU"

        raise ValueError("Value does not corresponds to a known mode of cache policy.")