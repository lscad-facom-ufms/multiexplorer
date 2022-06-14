import json
import os
import sys
import time

from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.AllowedValues import Simulators, PredictedCores, \
    SniperCorePipelineKinds, \
    CachePolicies, HashTypes, PerformanceModelTypes, Domains, Prefetchers, DramDirectoryTypes, MemoryModels, \
    Technologies, Applications
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_SNIPER, PATH_RUNDIR


class SniperSimulatorAdapter(Adapter):
    """
    This adapter utilises Sniper Multi-Core Simulator to execute a performance evaluation of a CPU architecture
    through simulation.
    """

    def __init__(self):
        Adapter.__init__(self)

        self.inputs = {}

        self.set_inputs([
            Input({
                'label': 'application',
                'key': 'application',
                'allowed_values': Applications.get_dict(),
                "required": True,
                "is_user_input": True,
            }),
            InputGroup({
                "label": "General Modeling",
                "key": "general_modeling",
                "inputs": [
                    Input({
                        "label": "Core Model",
                        "key": "model_name",
                        "is_user_input": True,
                        "required": True,
                        "allowed_values": {
                            PredictedCores.Quark: PredictedCores.get_label(PredictedCores.Quark),
                            PredictedCores.Arm53: PredictedCores.get_label(PredictedCores.Arm53),
                            PredictedCores.Arm57: PredictedCores.get_label(PredictedCores.Arm57),
                            PredictedCores.Atom: PredictedCores.get_label(PredictedCores.Atom),
                        },
                    }),
                    Input({
                        "label": "Number of Cores",
                        "key": "total_cores",
                        "is_user_input": True,
                        "required": True,
                        "type": InputType.Integer,
                    }),
                    InputGroup({
                        "label": "Core Specifications",
                        "key": "core",
                        "inputs": [
                            Input({
                                "label": "Global Frequency",
                                "key": "global_frequency",
                                "is_user_input": True,
                                "required": True,
                                "type": InputType.Integer,
                            }),
                            Input({
                                "label": "Frequency",
                                "key": "frequency",
                                "type": InputType.IntegerArray,
                            }),
                            Input({
                                "label": "Number of Threads",
                                "key": "threads",
                                "type": InputType.Integer,
                            }),
                            Input({
                                "label": "Number of Logical CPUs",
                                "key": "logical_cpus",
                                "type": InputType.Integer,
                            }),
                            InputGroup({
                                "label": "Pipeline",
                                "key": "pipeline",
                                "inputs": [
                                    Input({
                                        "label": "",
                                        "key": "present",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "",
                                        "key": "fetch_kind",
                                        "allowed_values": {
                                            SniperCorePipelineKinds.Shared: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.Shared
                                            ),
                                            SniperCorePipelineKinds.TimeSlice: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.TimeSlice
                                            ),
                                        },
                                    }),
                                    Input({
                                        "label": "Decode Width",
                                        "key": "decode_width",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Dispatch Kind",
                                        "key": "dispatch_kind",
                                        "allowed_values": {
                                            SniperCorePipelineKinds.Shared: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.Shared
                                            ),
                                            SniperCorePipelineKinds.TimeSlice: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.TimeSlice
                                            ),
                                        },
                                    }),
                                    Input({
                                        "label": "Dispatch Width",
                                        "key": "dispatch_width",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Issue Kind",
                                        "key": "issue_kind",
                                        "allowed_values": {
                                            SniperCorePipelineKinds.Shared: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.Shared
                                            ),
                                            SniperCorePipelineKinds.TimeSlice: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.TimeSlice
                                            ),
                                        },
                                    }),
                                    Input({
                                        "label": "Issue Width",
                                        "key": "issue_width",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Commit Kind",
                                        "key": "commit_kind",
                                        "allowed_values": {
                                            SniperCorePipelineKinds.Shared: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.Shared
                                            ),
                                            SniperCorePipelineKinds.TimeSlice: SniperCorePipelineKinds.get_label(
                                                SniperCorePipelineKinds.TimeSlice
                                            ),
                                        },
                                    }),
                                    Input({
                                        "label": "Commit Width",
                                        "key": "commit_width",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Occupancy Stats",
                                        "key": "occupancy_stats",
                                        "type": InputType.Bool,
                                    }),
                                ],
                            }),
                        ],
                    }),
                    InputGroup({
                        "label": "Memory Model",
                        "key": "memory",
                        "inputs": [
                            InputGroup({
                                "label": "Cache",
                                "key": "cache",
                                "inputs": [
                                    Input({
                                        "label": "Number of Cache Levels",
                                        "key": "levels",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            3: 3
                                        },
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "TLB",
                                "key": "tlb",
                                "inputs": [
                                    Input({
                                        "label": "Sets",
                                        "key": "sets",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Block Size",
                                        "key": "block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "Latency",
                                        "key": "latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Policy",
                                        "key": "policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "ITLB",
                                "key": "itlb",
                                "inputs": [
                                    Input({
                                        "label": "Sets",
                                        "key": "sets",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Block Size",
                                        "key": "block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Latency",
                                        "key": "latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Policy",
                                        "key": "policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "DTLB",
                                "key": "dtlb",
                                "inputs": [
                                    Input({
                                        "label": "Sets",
                                        "key": "sets",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Block Size",
                                        "key": "block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Latency",
                                        "key": "latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Policy",
                                        "key": "policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "STLB",
                                "key": "stlb",
                                "inputs": [
                                    Input({
                                        "label": "Sets",
                                        "key": "sets",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Block Size",
                                        "key": "block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "Latency",
                                        "key": "latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Policy",
                                        "key": "policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "L1 iCache",
                                "key": "li_icache-0",
                                "inputs": [
                                    Input({
                                        "label": "Perfect?",
                                        "key": "perfect",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "passthrough",
                                        "key": "passthrough",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "cache_block_size",
                                        "key": "cache_block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "cache_size",
                                        "key": "cache_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "ports",
                                        "key": "ports",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "address_hash",
                                        "key": "address_hash",
                                        "allowed_values": {
                                            HashTypes.Mask: HashTypes.get_label(HashTypes.Mask),
                                        },
                                    }),
                                    Input({
                                        "label": "replacement_policy",
                                        "key": "replacement_policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                    Input({
                                        "label": "data_access_time",
                                        "key": "data_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "tags_access_time",
                                        "key": "tags_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "perf_model_type",
                                        "key": "perf_model_type",
                                        "allowed_values": PerformanceModelTypes.get_dict(),
                                    }),
                                    Input({
                                        "label": "writethrough",
                                        "key": "writethrough",
                                        "type": InputType.Bit,
                                    }),
                                    Input({
                                        "label": "writeback_time",
                                        "key": "writeback_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "dvfs_domain",
                                        "key": "dvfs_domain",
                                        "allowed_values": Domains.get_dict(),
                                    }),
                                    Input({
                                        "label": "shared_cores",
                                        "key": "shared_cores",
                                        "type": InputType.IntegerArray,
                                    }),
                                    Input({
                                        "label": "prefetcher",
                                        "key": "prefetcher",
                                        "allowed_values": Prefetchers.get_dict(),
                                    }),
                                    Input({
                                        "label": "next_level_read_bandwidth",
                                        "key": "next_level_read_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "L1 dCache",
                                "key": "li_dcache-0",
                                "inputs": [
                                    Input({
                                        "label": "Perfect?",
                                        "key": "perfect",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "passthrough",
                                        "key": "passthrough",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "cache_block_size",
                                        "key": "cache_block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "cache_size",
                                        "key": "cache_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "ports",
                                        "key": "ports",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "address_hash",
                                        "key": "address_hash",
                                        "allowed_values": {
                                            HashTypes.Mask: HashTypes.get_label(HashTypes.Mask),
                                        },
                                    }),
                                    Input({
                                        "label": "replacement_policy",
                                        "key": "replacement_policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                    Input({
                                        "label": "data_access_time",
                                        "key": "data_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "tags_access_time",
                                        "key": "tags_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "perf_model_type",
                                        "key": "perf_model_type",
                                        "allowed_values": PerformanceModelTypes.get_dict(),
                                    }),
                                    Input({
                                        "label": "writethrough",
                                        "key": "writethrough",
                                        "type": InputType.Bit,
                                    }),
                                    Input({
                                        "label": "writeback_time",
                                        "key": "writeback_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "dvfs_domain",
                                        "key": "dvfs_domain",
                                        "allowed_values": Domains.get_dict(),
                                    }),
                                    Input({
                                        "label": "shared_cores",
                                        "key": "shared_cores",
                                        "type": InputType.IntegerArray,
                                    }),
                                    Input({
                                        "label": "prefetcher",
                                        "key": "prefetcher",
                                        "allowed_values": Prefetchers.get_dict(),
                                    }),
                                    Input({
                                        "label": "next_level_read_bandwidth",
                                        "key": "next_level_read_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "L2 Cache",
                                "key": "l2_cache-0",
                                "inputs": [
                                    Input({
                                        "label": "Perfect?",
                                        "key": "perfect",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "passthrough",
                                        "key": "passthrough",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "cache_block_size",
                                        "key": "cache_block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "cache_size",
                                        "key": "cache_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "ports",
                                        "key": "ports",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "address_hash",
                                        "key": "address_hash",
                                        "allowed_values": {
                                            HashTypes.Mask: HashTypes.get_label(HashTypes.Mask),
                                        },
                                    }),
                                    Input({
                                        "label": "replacement_policy",
                                        "key": "replacement_policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                    Input({
                                        "label": "data_access_time",
                                        "key": "data_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "tags_access_time",
                                        "key": "tags_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "perf_model_type",
                                        "key": "perf_model_type",
                                        "allowed_values": PerformanceModelTypes.get_dict(),
                                    }),
                                    Input({
                                        "label": "writethrough",
                                        "key": "writethrough",
                                        "type": InputType.Bit,
                                    }),
                                    Input({
                                        "label": "writeback_time",
                                        "key": "writeback_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "dvfs_domain",
                                        "key": "dvfs_domain",
                                        "allowed_values": Domains.get_dict(),
                                    }),
                                    Input({
                                        "label": "shared_cores",
                                        "key": "shared_cores",
                                        "type": InputType.IntegerArray,
                                    }),
                                    Input({
                                        "label": "prefetcher",
                                        "key": "prefetcher",
                                        "allowed_values": Prefetchers.get_dict(),
                                    }),
                                    Input({
                                        "label": "next_level_read_bandwidth",
                                        "key": "next_level_read_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "L3 Cache",
                                "key": "l3_cache-0",
                                "inputs": [
                                    Input({
                                        "label": "Perfect?",
                                        "key": "perfect",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "passthrough",
                                        "key": "passthrough",
                                        "type": InputType.Bool,
                                    }),
                                    Input({
                                        "label": "cache_block_size",
                                        "key": "cache_block_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "cache_size",
                                        "key": "cache_size",
                                        "allowed_values": {
                                            8: 8,
                                            16: 16,
                                            32: 32,
                                            64: 64,
                                            128: 128,
                                        },
                                    }),
                                    Input({
                                        "label": "associativity",
                                        "key": "associativity",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "ports",
                                        "key": "ports",
                                        "allowed_values": {
                                            1: 1,
                                            2: 2,
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "address_hash",
                                        "key": "address_hash",
                                        "allowed_values": {
                                            HashTypes.Mask: HashTypes.get_label(HashTypes.Mask),
                                        },
                                    }),
                                    Input({
                                        "label": "replacement_policy",
                                        "key": "replacement_policy",
                                        "allowed_values": {
                                            CachePolicies.LRU: CachePolicies.get_label(CachePolicies.LRU),
                                        },
                                    }),
                                    Input({
                                        "label": "data_access_time",
                                        "key": "data_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "tags_access_time",
                                        "key": "tags_access_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "perf_model_type",
                                        "key": "perf_model_type",
                                        "allowed_values": PerformanceModelTypes.get_dict(),
                                    }),
                                    Input({
                                        "label": "writethrough",
                                        "key": "writethrough",
                                        "type": InputType.Bit,
                                    }),
                                    Input({
                                        "label": "writeback_time",
                                        "key": "writeback_time",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "dvfs_domain",
                                        "key": "dvfs_domain",
                                        "allowed_values": Domains.get_dict(),
                                    }),
                                    Input({
                                        "label": "shared_cores",
                                        "key": "shared_cores",
                                        "type": InputType.IntegerArray,
                                    }),
                                    Input({
                                        "label": "prefetcher",
                                        "key": "prefetcher",
                                        "allowed_values": Prefetchers.get_dict(),
                                    }),
                                    Input({
                                        "label": "next_level_read_bandwidth",
                                        "key": "next_level_read_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "DRAM",
                                "key": "dram",
                                "inputs": [
                                    InputGroup({
                                        "label": "DRAM Directory",
                                        "key": "dram_directory",
                                        "inputs": [
                                            Input({
                                                "label": "Total Number of Entries",
                                                "key": "total_entries",
                                                "type": InputType.Integer,
                                            }),
                                            Input({
                                                "label": "Associativity",
                                                "key": "associativity",
                                                "allowed_values": {
                                                    1: 1,
                                                    2: 2,
                                                    4: 4,
                                                    8: 8,
                                                    16: 16,
                                                },
                                            }),
                                            Input({
                                                "label": "Total Number of Entries",
                                                "key": "total_entries",
                                                "allowed_values": DramDirectoryTypes.get_dict(),
                                            }),
                                        ]
                                    }),
                                    Input({
                                        "label": "Number of Controllers",
                                        "key": "num_controllers",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "controllers_interleaving",
                                        "key": "controllers_interleaving",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "latency",
                                        "key": "latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "block_size",
                                        "key": "block_size",
                                        "allowed_values": {
                                            256: 256,
                                            512: 512,
                                            1024: 1024,
                                            2048: 2048,
                                        },
                                    }),
                                    Input({
                                        "label": "per_controller_bandwidth",
                                        "key": "per_controller_bandwidth",
                                        "type": InputType.Float,
                                    }),
                                    Input({
                                        "label": "chips_per_dimm",
                                        "key": "chips_per_dimm",
                                        "allowed_values": {
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                    Input({
                                        "label": "dimms_per_controller",
                                        "key": "dimms_per_controller",
                                        "allowed_values": {
                                            4: 4,
                                            8: 8,
                                            16: 16,
                                        },
                                    }),
                                ],
                            }),
                        ],
                    }),
                    InputGroup({
                        "label": "Network",
                        "key": "network",
                        "inputs": [
                            Input({
                                "label": "Memory Model #1",
                                "key": "memory_model_1",
                                "allowed_values": MemoryModels.get_dict(),
                            }),
                            Input({
                                "label": "Memory Model #2",
                                "key": "memory_model_2",
                                "allowed_values": MemoryModels.get_dict(),
                            }),
                            InputGroup({
                                "label": "Bus Configuration",
                                "key": "bus",
                                "inputs": [
                                    Input({
                                        "label": "Bandwidth",
                                        "key": "bandwidth",
                                        "type": InputType.Float,
                                    }),
                                    Input({
                                        "label": "ignore_local_traffic",
                                        "key": "ignore_local_traffic",
                                        "type": InputType.Bool,
                                    })
                                ],
                            }),
                            InputGroup({
                                "label": "EMESH Hop by Hop Configuration",
                                "key": "emesh_hop_by_hop",
                                "inputs": [
                                    Input({
                                        "label": "Link Bandwidth",
                                        "key": "link_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Hop Latency",
                                        "key": "hop_latency",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Concentration",
                                        "key": "concentration",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Dimensions",
                                        "key": "dimensions",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "Wrap_around",
                                        "key": "wrap_around",
                                        "type": InputType.Bool,
                                    }),
                                ],
                            }),
                            InputGroup({
                                "label": "Bus Configuration",
                                "key": "emesh_hop_counter",
                                "inputs": [
                                    Input({
                                        "label": "link_bandwidth",
                                        "key": "link_bandwidth",
                                        "type": InputType.Integer,
                                    }),
                                    Input({
                                        "label": "hop_latency",
                                        "key": "hop_latency",
                                        "type": InputType.Integer,
                                    })
                                ],
                            }),
                        ],
                    }),
                    InputGroup({
                        "label": "Power",
                        "key": "power",
                        "inputs": [
                            Input({
                                "label": "VDD",
                                "key": "vdd",
                                "type": InputType.Float,
                            }),
                            Input({
                                "label": "Technology Node",
                                "key": "technology_node",
                                "type": InputType.Integer,
                            }),
                            Input({
                                "label": "Temperature",
                                "key": "temperature",
                                "type": InputType.Integer,
                            }),
                        ],
                    }),
                ],
            }),
        ])

        self.results = {}

        self.use_benchmarks = True

        self.benchmark_size = None

        self.cfg_path = None

        self.output_path = None

    # todo
    def set_values_from_file(self, absolute_file_path):
        """
        This method reads a json file and sets the values of the inputs.
        """
        input_json = json.loads(open(absolute_file_path).read())

        print json.dumps(input_json, indent=4, sort_keys=True)

    # todo
    def set_values_from_cfg(self, absolute_cfg_file_path):
        cfg_file = open(absolute_cfg_file_path)

        # todo properly set values by reading the cfg_file

    # todo
    def generate_cfg_from_inputs(self):
            cfg_file_path = self.get_output_path() + "/sniper_input.cfg"

            cfg_file = open(cfg_file_path, 'w')

            # todo WRITE PROPER CFG FILE

            cfg_file.writelines([
                "#include nehalem\n",
                "[general]\n",
                "total_cores=" + str(self.inputs['general_modeling']['total_cores']) + "\n\n",
            ])

            global_frequency = str(self.inputs['general_modeling']['core']['global_frequency'])

            try:
                frequencies = ','.join(map(str, self.inputs['general_modeling']['core']['frequency']))
            except TypeError:
                frequencies = global_frequency

            cfg_file.writelines([
                "[perf_model/core]\n",
                "logical_cpus=" + str(self.inputs['general_modeling']['core']['logical_cpus']) + "\n",
                "frequency=" + global_frequency + "\n",
                "frequency[]=" + frequencies + "\n\n",
            ])

            cfg_file.writelines([
                "[perf_model/cache]\n",
                "levels=" + str(self.inputs['general_modeling']['memory']['cache']['levels']) + "\n",
            ])

            cfg_file.writelines([
                "[perf_model/tlb]\n",
                "size[]=" + str(self.inputs['general_modeling']['memory']['tlb']['sets']) + "\n",
                "penalty=" + str(self.inputs['general_modeling']['memory']['tlb']['latency']) + "\n",
                "policy=" + str(self.inputs['general_modeling']['memory']['tlb']['policy']) + "\n",
                "associativity=" + str(self.inputs['general_modeling']['memory']['tlb']['associativity']) + "\n",
                "block_size=" + str(self.inputs['general_modeling']['memory']['tlb']['block_size']) + "\n",
                "latency=" + str(self.inputs['general_modeling']['memory']['tlb']['latency']) + "\n",
                "sets=" + str(self.inputs['general_modeling']['memory']['tlb']['sets']) + "\n\n",
            ])

            cfg_file.writelines([
                "[perf_model/itlb]\n",
                "size[]=" + str(self.inputs['general_modeling']['memory']['itlb']['sets']) + "\n",
                "penalty=" + str(self.inputs['general_modeling']['memory']['itlb']['latency']) + "\n",
                "policy=" + str(self.inputs['general_modeling']['memory']['itlb']['policy']) + "\n",
                "associativity=" + str(self.inputs['general_modeling']['memory']['itlb']['associativity']) + "\n",
                "block_size=" + str(self.inputs['general_modeling']['memory']['itlb']['block_size']) + "\n",
                "latency=" + str(self.inputs['general_modeling']['memory']['itlb']['latency']) + "\n",
                "sets=" + str(self.inputs['general_modeling']['memory']['itlb']['sets']) + "\n\n",
            ])

            cfg_file.close()

            self.cfg_path = cfg_file_path

    # todo
    def execute(self):
        time.sleep(6)

    def prepare(self):
        self.generate_cfg_from_inputs()

    def execute_simulation(self):
        os.system(
            self.get_executable_path() + "./run-sniper"
            + " -p " + self.get_benchmark_application()
            + " -n " + str(self.get_original_nbr_of_cores())
            + " -i " + self.get_benchmark_size()
            + " -c " + self.get_cfg_path()
            + " -d " + self.get_output_path()
            + "> " + self.get_output_path() + "/sniper_output.out"
        )

    def get_original_nbr_of_cores(self):
        return self.inputs["general_modeling"].inputs["total_cores"].value

    def get_benchmark_application(self):
        return self.inputs["application"].value

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


class McPATAdapter(Adapter):
    """
        This adapter utilises McPAT (an integrated power, area, and timing modeling framework for multithreading,
        multicore, and many-core architectures) to obtain the physical parameters  for a CPU architecture.
    """

    # todo
    def __init__(self):
        Adapter.__init__(self)

    # todo
    def get_user_inputs(self):
        pass

    # todo
    def execute(self):
        time.sleep(6)


class NsgaIIPredDSEAdapter(Adapter):
    """
        This adapter uses a NSGA-II implementation as it's exploration engine, and a heterogeneous multicore CPU
        architecture performance predictor as it's evaluation engine, in order to perform a design space exploration.
    """

    # todo
    def __init__(self):
        Adapter.__init__(self)

        self.inputs = {}

        self.set_inputs([
            InputGroup({
                'label': "Exploration Space",
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Number of Original Cores for Design',
                        'key': 'original_cores_for_design',
                        # "is_user_input": True,
                        # "required": True,
                        'type': InputType.IntegerRange,
                    }),
                    Input({
                        'label': 'Number of IP Cores for Design',
                        'key': 'ip_cores_for_design',
                        # "is_user_input": True,
                        # "required": True,
                        'type': InputType.IntegerRange,
                    }),
                ],
            }),
            InputGroup({
                'label': "Constraints",
                'key': 'constraints',
                'inputs': [
                    Input({
                        'label': 'Maximum Power Density',
                        'key': 'maximum_power_density',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Technology',
                        'key': 'technology',
                        'allowed_values': Technologies.get_dict(),
                        "is_user_input": True,
                        "required": True,
                    }),
                ],
            }),
        ])

    # todo
    def execute(self):
        time.sleep(6)


def main():
    sim = SniperSimulatorAdapter()

    sim.inputs = json.loads(open("/home/ufms/projetos/multiexplorer/input-examples/quark.json").read())

    sim.output_path = "/home/ufms/projetos/multiexplorer/rundir/test"

    sim.cfg_path = "/home/ufms/projetos/multiexplorer/input-examples/quark.cfg"

    sim.execute_simulation()


if __name__ == '__main__':
    sys.exit(main())
