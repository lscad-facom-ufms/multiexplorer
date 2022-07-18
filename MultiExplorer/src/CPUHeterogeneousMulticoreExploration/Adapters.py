import json
import os
import time
from xml.etree import ElementTree
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.AllowedValues import PredictedCores, \
    SniperCorePipelineKinds, \
    CachePolicies, HashTypes, PerformanceModelTypes, Domains, Prefetchers, DramDirectoryTypes, MemoryModels, \
    Technologies, Applications
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType
from MultiExplorer.src.config import PATH_SNIPER
import sys

sys.path.append(PATH_SNIPER + '/tools')
import sniper_lib


class SniperSimulatorAdapter(Adapter):
    """
    This adapter utilises Sniper Multi-Core Simulator to execute a performance evaluation of a CPU architecture
    through simulation.
    """

    def __init__(self):
        Adapter.__init__(self)

        self.set_inputs([
            Input({
                'label': 'Application',
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
                        "allowed_values": PredictedCores.get_dict(),
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
                                "key": "l1_icache",
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
                                            256: 256,
                                            512: 512,
                                            1024: 1024,
                                            2048: 2048,
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
                                        "type": InputType.Integer,
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
                                "key": "l1_dcache",
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
                                            256: 256,
                                            512: 512,
                                            1024: 1024,
                                            2048: 2048,
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
                                        "type": InputType.Integer,
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
                                "key": "l2_cache",
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
                                            256: 256,
                                            512: 512,
                                            1024: 1024,
                                            2048: 2048,
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
                                        "type": InputType.Integer,
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
                                "key": "l3_cache",
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
                                            256: 256,
                                            512: 512,
                                            1024: 1024,
                                            2048: 2048,
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
                                        "type": InputType.Integer,
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
                                                "label": "Directory Type",
                                                "key": "directory_type",
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
                                    }),
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

        self.config = {}

        self.results = {}

        self.use_benchmarks = True

        self.benchmark_size = None

        self.cfg_path = None

        self.output_path = None

    def set_values_from_json(self, absolute_file_path):
        """
        This method reads a json file and sets the values of the inputs.
        """
        input_json = json.loads(open(absolute_file_path).read())

        self.inputs['general_modeling']['total_cores'] = int(input_json['General_Modeling']['total_cores'])

        global_frequency = int(input_json['General_Modeling']['core']['global_frequency'])
        self.inputs['general_modeling']['core']['global_frequency'] = global_frequency

        try:
            self.inputs['general_modeling']['core']['frequency'] = \
                tuple(input_json['General_Modeling']['core']['frequency'])
        except TypeError:
            self.inputs['general_modeling']['core']['frequency'] = global_frequency

        self.inputs['general_modeling']['core']['logical_cpus'] = \
            int(input_json['General_Modeling']['core']['logical_cpus'])

        try:
            nbr_cache_levels = int(input_json['General_Modeling']['memory']['cache']['levels'])
        except TypeError:
            nbr_cache_levels = 2

        self.inputs['general_modeling']['memory']['cache']['levels'] = str(nbr_cache_levels)

        self.inputs['general_modeling']['memory']['tlb']['sets'] = \
            int(input_json['General_Modeling']['memory']['tlb']['sets'])
        self.inputs['general_modeling']['memory']['tlb']['latency'] = \
            input_json['General_Modeling']['memory']['tlb']['latency']
        self.inputs['general_modeling']['memory']['tlb']['policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['tlb']['policy'])
        self.inputs['general_modeling']['memory']['tlb']['associativity'] = \
            input_json['General_Modeling']['memory']['tlb']['associativity']
        self.inputs['general_modeling']['memory']['tlb']['block_size'] = \
            input_json['General_Modeling']['memory']['tlb']['block_size']
        self.inputs['general_modeling']['memory']['tlb']['latency'] = \
            input_json['General_Modeling']['memory']['tlb']['latency']
        self.inputs['general_modeling']['memory']['tlb']['sets'] = \
            input_json['General_Modeling']['memory']['tlb']['sets']

        self.inputs['general_modeling']['memory']['itlb']['sets'] = \
            int(input_json['General_Modeling']['memory']['itlb']['sets'])
        self.inputs['general_modeling']['memory']['itlb']['latency'] = \
            input_json['General_Modeling']['memory']['itlb']['latency']
        self.inputs['general_modeling']['memory']['itlb']['policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['itlb']['policy'])
        self.inputs['general_modeling']['memory']['itlb']['associativity'] = \
            input_json['General_Modeling']['memory']['itlb']['associativity']
        self.inputs['general_modeling']['memory']['itlb']['block_size'] = \
            input_json['General_Modeling']['memory']['itlb']['block_size']
        self.inputs['general_modeling']['memory']['itlb']['latency'] = \
            input_json['General_Modeling']['memory']['itlb']['latency']
        self.inputs['general_modeling']['memory']['itlb']['sets'] = \
            input_json['General_Modeling']['memory']['itlb']['sets']

        self.inputs['general_modeling']['memory']['dtlb']['sets'] = \
            int(input_json['General_Modeling']['memory']['dtlb']['sets'])
        self.inputs['general_modeling']['memory']['dtlb']['latency'] = \
            input_json['General_Modeling']['memory']['dtlb']['latency']
        self.inputs['general_modeling']['memory']['dtlb']['policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['dtlb']['policy'])
        self.inputs['general_modeling']['memory']['dtlb']['associativity'] = \
            input_json['General_Modeling']['memory']['dtlb']['associativity']
        self.inputs['general_modeling']['memory']['dtlb']['block_size'] = \
            input_json['General_Modeling']['memory']['dtlb']['block_size']
        self.inputs['general_modeling']['memory']['dtlb']['latency'] = \
            input_json['General_Modeling']['memory']['dtlb']['latency']
        self.inputs['general_modeling']['memory']['dtlb']['sets'] = \
            input_json['General_Modeling']['memory']['dtlb']['sets']

        self.inputs['general_modeling']['memory']['stlb']['sets'] = \
            int(input_json['General_Modeling']['memory']['stlb']['sets'])
        self.inputs['general_modeling']['memory']['stlb']['latency'] = \
            input_json['General_Modeling']['memory']['stlb']['latency']
        self.inputs['general_modeling']['memory']['stlb']['policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['stlb']['policy'])
        self.inputs['general_modeling']['memory']['stlb']['associativity'] = \
            input_json['General_Modeling']['memory']['stlb']['associativity']
        self.inputs['general_modeling']['memory']['stlb']['block_size'] = \
            input_json['General_Modeling']['memory']['stlb']['block_size']
        self.inputs['general_modeling']['memory']['stlb']['latency'] = \
            input_json['General_Modeling']['memory']['stlb']['latency']
        self.inputs['general_modeling']['memory']['stlb']['sets'] = \
            input_json['General_Modeling']['memory']['stlb']['sets']

        self.inputs['general_modeling']['memory']['l1_icache']['perfect'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['perfect']
        self.inputs['general_modeling']['memory']['l1_icache']['perf_model_type'] = \
            PerformanceModelTypes.from_json(input_json['General_Modeling']['memory']['l1_icache-0']['perf_model_type'])
        self.inputs['general_modeling']['memory']['l1_icache']['replacement_policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['l1_icache-0']['replacement_policy'])
        shared_cores = input_json['General_Modeling']['memory']['l1_icache-0']['shared_cores']
        if shared_cores == [0]:
            self.inputs['general_modeling']['memory']['l1_icache']['shared_cores'] = 1
        else:
            self.inputs['general_modeling']['memory']['l1_icache']['shared_cores'] = tuple(shared_cores)

        self.inputs['general_modeling']['memory']['l1_icache']['dvfs_domain'] = \
            Domains.from_json(input_json['General_Modeling']['memory']['l1_icache-0']['dvfs_domain'])
        self.inputs['general_modeling']['memory']['l1_icache']['passthrough'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['passthrough']
        self.inputs['general_modeling']['memory']['l1_icache']['cache_block_size'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['cache_block_size']
        self.inputs['general_modeling']['memory']['l1_icache']['prefetcher'] = \
            Prefetchers.from_json(input_json['General_Modeling']['memory']['l1_icache-0']['prefetcher'])
        self.inputs['general_modeling']['memory']['l1_icache']['address_hash'] = \
            HashTypes.from_json(input_json['General_Modeling']['memory']['l1_icache-0']['address_hash'])
        self.inputs['general_modeling']['memory']['l1_icache']['writethrough'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['writethrough']
        self.inputs['general_modeling']['memory']['l1_icache']['cache_size'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['cache_size']
        self.inputs['general_modeling']['memory']['l1_icache']['writeback_time'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['writeback_time']
        self.inputs['general_modeling']['memory']['l1_icache']['associativity'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['associativity']
        self.inputs['general_modeling']['memory']['l1_icache']['tags_access_time'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['tags_access_time']
        self.inputs['general_modeling']['memory']['l1_icache']['next_level_read_bandwidth'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['next_level_read_bandwidth']
        self.inputs['general_modeling']['memory']['l1_icache']['ports'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['ports']
        self.inputs['general_modeling']['memory']['l1_icache']['data_access_time'] = \
            input_json['General_Modeling']['memory']['l1_icache-0']['data_access_time']

        self.inputs['general_modeling']['memory']['l1_dcache']['perfect'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['perfect']
        self.inputs['general_modeling']['memory']['l1_dcache']['perf_model_type'] = \
            PerformanceModelTypes.from_json(input_json['General_Modeling']['memory']['l1_dcache-0']['perf_model_type'])
        self.inputs['general_modeling']['memory']['l1_dcache']['replacement_policy'] = \
            CachePolicies.from_json(input_json['General_Modeling']['memory']['l1_dcache-0']['replacement_policy'])
        shared_cores = input_json['General_Modeling']['memory']['l1_dcache-0']['shared_cores']
        if shared_cores == [0]:
            self.inputs['general_modeling']['memory']['l1_dcache']['shared_cores'] = 1
        else:
            self.inputs['general_modeling']['memory']['l1_dcache']['shared_cores'] = tuple(shared_cores)
        self.inputs['general_modeling']['memory']['l1_dcache']['dvfs_domain'] = \
            Domains.from_json(input_json['General_Modeling']['memory']['l1_dcache-0']['dvfs_domain'])
        self.inputs['general_modeling']['memory']['l1_dcache']['passthrough'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['passthrough']
        self.inputs['general_modeling']['memory']['l1_dcache']['cache_block_size'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['cache_block_size']
        self.inputs['general_modeling']['memory']['l1_dcache']['prefetcher'] = \
            Prefetchers.from_json(input_json['General_Modeling']['memory']['l1_dcache-0']['prefetcher'])
        self.inputs['general_modeling']['memory']['l1_dcache']['address_hash'] = \
            HashTypes.from_json(input_json['General_Modeling']['memory']['l1_dcache-0']['address_hash'])
        self.inputs['general_modeling']['memory']['l1_dcache']['writethrough'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['writethrough']
        self.inputs['general_modeling']['memory']['l1_dcache']['cache_size'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['cache_size']
        self.inputs['general_modeling']['memory']['l1_dcache']['writeback_time'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['writeback_time']
        self.inputs['general_modeling']['memory']['l1_dcache']['associativity'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['associativity']
        self.inputs['general_modeling']['memory']['l1_dcache']['tags_access_time'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['tags_access_time']
        self.inputs['general_modeling']['memory']['l1_dcache']['next_level_read_bandwidth'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['next_level_read_bandwidth']
        self.inputs['general_modeling']['memory']['l1_dcache']['ports'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['ports']
        self.inputs['general_modeling']['memory']['l1_dcache']['data_access_time'] = \
            input_json['General_Modeling']['memory']['l1_dcache-0']['data_access_time']

        if nbr_cache_levels >= 2:
            self.inputs['general_modeling']['memory']['l2_cache']['perfect'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['perfect']
            self.inputs['general_modeling']['memory']['l2_cache']['perf_model_type'] = \
                PerformanceModelTypes.from_json(
                    input_json['General_Modeling']['memory']['l2_cache-0']['perf_model_type'])
            self.inputs['general_modeling']['memory']['l2_cache']['replacement_policy'] = \
                CachePolicies.from_json(input_json['General_Modeling']['memory']['l2_cache-0']['replacement_policy'])
            shared_cores = input_json['General_Modeling']['memory']['l2_cache-0']['shared_cores']
            if shared_cores == [0]:
                self.inputs['general_modeling']['memory']['l2_cache']['shared_cores'] = 1
            else:
                self.inputs['general_modeling']['memory']['l2_cache']['shared_cores'] = tuple(shared_cores)
            self.inputs['general_modeling']['memory']['l2_cache']['dvfs_domain'] = \
                Domains.from_json(input_json['General_Modeling']['memory']['l2_cache-0']['dvfs_domain'])
            self.inputs['general_modeling']['memory']['l2_cache']['passthrough'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['passthrough']
            self.inputs['general_modeling']['memory']['l2_cache']['cache_block_size'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['cache_block_size']
            self.inputs['general_modeling']['memory']['l2_cache']['prefetcher'] = \
                Prefetchers.from_json(input_json['General_Modeling']['memory']['l2_cache-0']['prefetcher'])
            self.inputs['general_modeling']['memory']['l2_cache']['address_hash'] = \
                HashTypes.from_json(input_json['General_Modeling']['memory']['l2_cache-0']['address_hash'])
            self.inputs['general_modeling']['memory']['l2_cache']['writethrough'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['writethrough']
            self.inputs['general_modeling']['memory']['l2_cache']['cache_size'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['cache_size']
            self.inputs['general_modeling']['memory']['l2_cache']['writeback_time'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['writeback_time']
            self.inputs['general_modeling']['memory']['l2_cache']['associativity'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['associativity']
            self.inputs['general_modeling']['memory']['l2_cache']['tags_access_time'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['tags_access_time']
            self.inputs['general_modeling']['memory']['l2_cache']['next_level_read_bandwidth'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['next_level_read_bandwidth']
            self.inputs['general_modeling']['memory']['l2_cache']['ports'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['ports']
            self.inputs['general_modeling']['memory']['l2_cache']['data_access_time'] = \
                input_json['General_Modeling']['memory']['l2_cache-0']['data_access_time']

        if nbr_cache_levels >= 3:
            self.inputs['general_modeling']['memory']['l3_cache']['perfect'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['perfect']
            self.inputs['general_modeling']['memory']['l3_cache']['perf_model_type'] = \
                PerformanceModelTypes.from_json(
                    input_json['General_Modeling']['memory']['l3_cache-0']['perf_model_type'])
            self.inputs['general_modeling']['memory']['l3_cache']['replacement_policy'] = \
                CachePolicies.from_json(input_json['General_Modeling']['memory']['l3_cache-0']['replacement_policy'])
            shared_cores = input_json['General_Modeling']['memory']['l3_cache-0']['shared_cores']
            if shared_cores == [0]:
                self.inputs['general_modeling']['memory']['l3_cache']['shared_cores'] = 1
            else:
                self.inputs['general_modeling']['memory']['l3_cache']['shared_cores'] = tuple(shared_cores)
            self.inputs['general_modeling']['memory']['l3_cache']['dvfs_domain'] = \
                Domains.from_json(input_json['General_Modeling']['memory']['l3_cache-0']['dvfs_domain'])
            self.inputs['general_modeling']['memory']['l3_cache']['passthrough'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['passthrough']
            self.inputs['general_modeling']['memory']['l3_cache']['cache_block_size'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['cache_block_size']
            self.inputs['general_modeling']['memory']['l3_cache']['prefetcher'] = \
                Prefetchers.from_json(input_json['General_Modeling']['memory']['l3_cache-0']['prefetcher'])
            self.inputs['general_modeling']['memory']['l3_cache']['address_hash'] = \
                HashTypes.from_json(input_json['General_Modeling']['memory']['l3_cache-0']['address_hash'])
            self.inputs['general_modeling']['memory']['l3_cache']['writethrough'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['writethrough']
            self.inputs['general_modeling']['memory']['l3_cache']['cache_size'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['cache_size']
            self.inputs['general_modeling']['memory']['l3_cache']['writeback_time'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['writeback_time']
            self.inputs['general_modeling']['memory']['l3_cache']['associativity'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['associativity']
            self.inputs['general_modeling']['memory']['l3_cache']['tags_access_time'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['tags_access_time']
            self.inputs['general_modeling']['memory']['l3_cache']['next_level_read_bandwidth'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['next_level_read_bandwidth']
            self.inputs['general_modeling']['memory']['l3_cache']['ports'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['ports']
            self.inputs['general_modeling']['memory']['l3_cache']['data_access_time'] = \
                input_json['General_Modeling']['memory']['l3_cache-0']['data_access_time']

        self.inputs['general_modeling']['memory']['dram']['latency'] = \
            input_json['General_Modeling']['memory']['dram']['latency']
        self.inputs['general_modeling']['memory']['dram']['num_controllers'] = \
            input_json['General_Modeling']['memory']['dram']['num_controllers']
        self.inputs['general_modeling']['memory']['dram']['chips_per_dimm'] = \
            input_json['General_Modeling']['memory']['dram']['chips_per_dimm']
        self.inputs['general_modeling']['memory']['dram']['controllers_interleaving'] = \
            input_json['General_Modeling']['memory']['dram']['controllers_interleaving']
        self.inputs['general_modeling']['memory']['dram']['per_controller_bandwidth'] = \
            input_json['General_Modeling']['memory']['dram']['per_controller_bandwidth']
        self.inputs['general_modeling']['memory']['dram']['block_size'] = \
            input_json['General_Modeling']['memory']['dram']['block_size']
        self.inputs['general_modeling']['memory']['dram']['dimms_per_controller'] = \
            input_json['General_Modeling']['memory']['dram']['dimms_per_controller']

        self.inputs['general_modeling']['memory']['dram']['dram_directory']['associativity'] = \
            input_json['General_Modeling']['memory']['dram']['dram_directory']['associativity']
        self.inputs['general_modeling']['memory']['dram']['dram_directory']['total_entries'] = \
            input_json['General_Modeling']['memory']['dram']['dram_directory']['total_entries']
        self.inputs['general_modeling']['memory']['dram']['dram_directory']['directory_type'] = \
            DramDirectoryTypes.from_json(
                input_json['General_Modeling']['memory']['dram']['dram_directory']['directory_type']
            )

        self.inputs['general_modeling']['network']['emesh_hop_by_hop']['link_bandwidth'] = \
            input_json['General_Modeling']['network']['emesh_hop_by_hop']['link_bandwidth']
        self.inputs['general_modeling']['network']['emesh_hop_by_hop']['concentration'] = \
            input_json['General_Modeling']['network']['emesh_hop_by_hop']['concentration']
        self.inputs['general_modeling']['network']['emesh_hop_by_hop']['wrap_around'] = \
            input_json['General_Modeling']['network']['emesh_hop_by_hop']['wrap_around']
        self.inputs['general_modeling']['network']['emesh_hop_by_hop']['hop_latency'] = \
            input_json['General_Modeling']['network']['emesh_hop_by_hop']['hop_latency']
        self.inputs['general_modeling']['network']['emesh_hop_by_hop']['dimensions'] = \
            input_json['General_Modeling']['network']['emesh_hop_by_hop']['dimensions']

        self.inputs['general_modeling']['network']['bus']['bandwidth'] = \
            input_json['General_Modeling']['network']['bus']['bandwidth']
        self.inputs['general_modeling']['network']['bus']['ignore_local_traffic'] = \
            input_json['General_Modeling']['network']['bus']['ignore_local_traffic']

        self.inputs['general_modeling']['network']['emesh_hop_counter']['link_bandwidth'] = \
            input_json['General_Modeling']['network']['emesh_hop_counter']['link_bandwidth']
        self.inputs['general_modeling']['network']['emesh_hop_counter']['hop_latency'] = \
            input_json['General_Modeling']['network']['emesh_hop_counter']['hop_latency']

        self.inputs['general_modeling']['network']['memory_model_1'] = \
            MemoryModels.from_json(input_json['General_Modeling']['network']['memory_model_1'])
        self.inputs['general_modeling']['network']['memory_model_2'] = \
            MemoryModels.from_json(input_json['General_Modeling']['network']['memory_model_2'])

        self.inputs['general_modeling']['power']['technology_node'] = \
            input_json['General_Modeling']['power']['technology_node']
        self.inputs['general_modeling']['power']['vdd'] = \
            input_json['General_Modeling']['power']['vdd']
        self.inputs['general_modeling']['power']['temperature'] = \
            input_json['General_Modeling']['power']['temperature']

    def generate_cfg_from_inputs(self):
        cfg_file_path = self.get_output_path() + "/sniper_input.cfg"

        cfg_file = open(cfg_file_path, 'w')

        cfg_file.writelines([
            "#include nehalem\n",
            "[general]\n",
            "total_cores=" + str(self.inputs['general_modeling']['total_cores']) + "\n\n",
        ])

        global_frequency = str(float(self.inputs['general_modeling']['core']['global_frequency']) / 1000.0)

        try:
            frequencies = []

            for value in self.inputs['general_modeling']['core']['frequency']:
                frequencies.append(float(value) / 1000.0)

            frequencies = ','.join(map(str, frequencies))
        except TypeError:
            frequencies = global_frequency

        cfg_file.writelines([
            "[perf_model/core]\n",
            "logical_cpus=" + str(self.inputs['general_modeling']['core']['logical_cpus']) + "\n",
            "frequency=" + global_frequency + "\n",
            "frequency[]=" + frequencies + "\n\n",
        ])

        try:
            nbr_cache_levels = int(self.inputs['general_modeling']['memory']['cache']['levels'])
        except TypeError:
            nbr_cache_levels = 2

        cfg_file.writelines([
            "[perf_model/cache]\n",
            "levels=" + str(nbr_cache_levels) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/tlb]\n",
            "size[]=" + str(self.inputs['general_modeling']['memory']['tlb']['sets']) + "\n",
            "penalty=" + str(self.inputs['general_modeling']['memory']['tlb']['latency']) + "\n",
            "policy=" + self.inputs['general_modeling']['memory']['tlb']['policy'].to_cfg() + "\n",
            "associativity=" + str(self.inputs['general_modeling']['memory']['tlb']['associativity']) + "\n",
            "block_size=" + str(self.inputs['general_modeling']['memory']['tlb']['block_size']) + "\n",
            "latency=" + str(self.inputs['general_modeling']['memory']['tlb']['latency']) + "\n",
            "sets=" + str(self.inputs['general_modeling']['memory']['tlb']['sets']) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/itlb]\n",
            "size[]=" + str(self.inputs['general_modeling']['memory']['itlb']['sets']) + "\n",
            "penalty=" + str(self.inputs['general_modeling']['memory']['itlb']['latency']) + "\n",
            "policy=" + self.inputs['general_modeling']['memory']['itlb']['policy'].to_cfg() + "\n",
            "associativity=" + str(self.inputs['general_modeling']['memory']['itlb']['associativity']) + "\n",
            "block_size=" + str(self.inputs['general_modeling']['memory']['itlb']['block_size']) + "\n",
            "latency=" + str(self.inputs['general_modeling']['memory']['itlb']['latency']) + "\n",
            "sets=" + str(self.inputs['general_modeling']['memory']['itlb']['sets']) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/dtlb]\n",
            "size[]=" + str(self.inputs['general_modeling']['memory']['dtlb']['sets']) + "\n",
            "penalty=" + str(self.inputs['general_modeling']['memory']['dtlb']['latency']) + "\n",
            "policy=" + self.inputs['general_modeling']['memory']['dtlb']['policy'].to_cfg() + "\n",
            "associativity=" + str(self.inputs['general_modeling']['memory']['dtlb']['associativity']) + "\n",
            "block_size=" + str(self.inputs['general_modeling']['memory']['dtlb']['block_size']) + "\n",
            "latency=" + str(self.inputs['general_modeling']['memory']['dtlb']['latency']) + "\n",
            "sets=" + str(self.inputs['general_modeling']['memory']['dtlb']['sets']) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/stlb]\n",
            "size[]=" + str(self.inputs['general_modeling']['memory']['stlb']['sets']) + "\n",
            "penalty=" + str(self.inputs['general_modeling']['memory']['stlb']['latency']) + "\n",
            "policy=" + self.inputs['general_modeling']['memory']['stlb']['policy'].to_cfg() + "\n",
            "associativity=" + str(self.inputs['general_modeling']['memory']['stlb']['associativity']) + "\n",
            "block_size=" + str(self.inputs['general_modeling']['memory']['stlb']['block_size']) + "\n",
            "latency=" + str(self.inputs['general_modeling']['memory']['stlb']['latency']) + "\n",
            "sets=" + str(self.inputs['general_modeling']['memory']['stlb']['sets']) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/l1_icache]\n",
            "perfect=" + str(self.inputs['general_modeling']['memory']['l1_icache']['perfect']).lower() + "\n",
            "perf_model_type=" + self.inputs['general_modeling']['memory']['l1_icache']['perf_model_type'].to_cfg()
            + "\n",
            "replacement_policy=" +
            self.inputs['general_modeling']['memory']['l1_icache']['replacement_policy'].to_cfg() + "\n",
            "shared_cores=" + str(self.inputs['general_modeling']['memory']['l1_icache']['shared_cores']) + "\n",
            "dvfs_domain=" + self.inputs['general_modeling']['memory']['l1_icache']['dvfs_domain'].to_cfg() + "\n",
            "passthrough=" + str(self.inputs['general_modeling']['memory']['l1_icache']['passthrough']).lower() + "\n",
            "cache_block_size=" + str(
                self.inputs['general_modeling']['memory']['l1_icache']['cache_block_size']) + "\n",
            "prefetcher=" + self.inputs['general_modeling']['memory']['l1_icache']['prefetcher'].to_cfg() + "\n",
            "address_hash=" +
            self.inputs['general_modeling']['memory']['l1_icache']['address_hash'].to_cfg() + "\n",
            "writethrough[]=" + str(self.inputs['general_modeling']['memory']['l1_icache']['writethrough']) + "\n",
            "cache_size[]=" + str(self.inputs['general_modeling']['memory']['l1_icache']['cache_size']) + "\n",
            "writeback_time[]=" + str(self.inputs['general_modeling']['memory']['l1_icache']['writeback_time']) + "\n",
            "associativity[]=" + str(self.inputs['general_modeling']['memory']['l1_icache']['associativity']) + "\n",
            "tags_access_time[]=" + str(
                self.inputs['general_modeling']['memory']['l1_icache']['tags_access_time']) + "\n",
            "next_level_read_bandwidth[]="
            + str(self.inputs['general_modeling']['memory']['l1_icache']['next_level_read_bandwidth'])
            + "\n",
            "ports=" + str(self.inputs['general_modeling']['memory']['l1_icache']['ports']) + "\n",
            "data_access_time[]="
            + str(self.inputs['general_modeling']['memory']['l1_icache']['data_access_time'])
            + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/l1_dcache]\n",
            "perfect=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['perfect']).lower() + "\n",
            "perf_model_type=" +
            self.inputs['general_modeling']['memory']['l1_dcache']['perf_model_type'].to_cfg() + "\n",
            "replacement_policy=" +
            self.inputs['general_modeling']['memory']['l1_dcache']['replacement_policy'].to_cfg() + "\n",
            "shared_cores=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['shared_cores']) + "\n",
            "dvfs_domain=" + self.inputs['general_modeling']['memory']['l1_dcache']['dvfs_domain'].to_cfg() + "\n",
            "passthrough=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['passthrough']).lower() + "\n",
            "cache_block_size=" + str(
                self.inputs['general_modeling']['memory']['l1_dcache']['cache_block_size']) + "\n",
            "prefetcher=" + self.inputs['general_modeling']['memory']['l1_dcache']['prefetcher'].to_cfg() + "\n",
            "address_hash=" + self.inputs['general_modeling']['memory']['l1_dcache']['address_hash'].to_cfg() + "\n",
            "writethrough[]=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['writethrough']) + "\n",
            "cache_size[]=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['cache_size']) + "\n",
            "writeback_time[]=" + str(
                self.inputs['general_modeling']['memory']['l1_dcache']['writeback_time']) + "\n",
            "associativity[]=" + str(
                self.inputs['general_modeling']['memory']['l1_dcache']['associativity']) + "\n",
            "tags_access_time[]=" + str(
                self.inputs['general_modeling']['memory']['l1_dcache']['tags_access_time']) + "\n",
            "next_level_read_bandwidth[]="
            + str(self.inputs['general_modeling']['memory']['l1_dcache']['next_level_read_bandwidth'])
            + "\n",
            "ports=" + str(self.inputs['general_modeling']['memory']['l1_dcache']['ports']) + "\n",
            "data_access_time[]="
            + str(self.inputs['general_modeling']['memory']['l1_dcache']['data_access_time'])
            + "\n\n",
        ])

        if nbr_cache_levels >= 2:
            cfg_file.writelines([
                "[perf_model/l2_cache]\n",
                "perfect=" + str(self.inputs['general_modeling']['memory']['l2_cache']['perfect']).lower() + "\n",
                "perf_model_type=" +
                self.inputs['general_modeling']['memory']['l2_cache']['perf_model_type'].to_cfg() + "\n",
                "replacement_policy=" +
                self.inputs['general_modeling']['memory']['l2_cache']['replacement_policy'].to_cfg() + "\n",
                "shared_cores=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['shared_cores']) + "\n",
                "dvfs_domain=" + self.inputs['general_modeling']['memory']['l2_cache']['dvfs_domain'].to_cfg() + "\n",
                "passthrough=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['passthrough']).lower() + "\n",
                "cache_block_size=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['cache_block_size']) + "\n",
                "prefetcher=" + self.inputs['general_modeling']['memory']['l2_cache']['prefetcher'].to_cfg() + "\n",
                "address_hash=" +
                self.inputs['general_modeling']['memory']['l2_cache']['address_hash'].to_cfg() + "\n",
                "writethrough[]=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['writethrough']) + "\n",
                "cache_size[]=" + str(self.inputs['general_modeling']['memory']['l2_cache']['cache_size']) + "\n",
                "writeback_time[]=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['writeback_time']) + "\n",
                "associativity[]=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['associativity']) + "\n",
                "tags_access_time[]=" + str(
                    self.inputs['general_modeling']['memory']['l2_cache']['tags_access_time']) + "\n",
                "next_level_read_bandwidth[]="
                + str(self.inputs['general_modeling']['memory']['l2_cache']['next_level_read_bandwidth'])
                + "\n",
                "ports=" + str(self.inputs['general_modeling']['memory']['l2_cache']['ports']) + "\n",
                "data_access_time[]="
                + str(self.inputs['general_modeling']['memory']['l2_cache']['data_access_time'])
                + "\n\n",
            ])

        if nbr_cache_levels >= 3:
            cfg_file.writelines([
                "[perf_model/l3_cache]\n",
                "perfect=" + str(self.inputs['general_modeling']['memory']['l3_cache']['perfect']).lower() + "\n",
                "perf_model_type=" +
                self.inputs['general_modeling']['memory']['l3_cache']['perf_model_type'].to_cfg() + "\n",
                "replacement_policy=" +
                self.inputs['general_modeling']['memory']['l3_cache']['replacement_policy'].to_cfg() + "\n",
                "shared_cores=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['shared_cores']) + "\n",
                "dvfs_domain=" + self.inputs['general_modeling']['memory']['l3_cache']['dvfs_domain'].to_cfg() + "\n",
                "passthrough=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['passthrough']).lower() + "\n",
                "cache_block_size=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['cache_block_size']) + "\n",
                "prefetcher=" + self.inputs['general_modeling']['memory']['l3_cache']['prefetcher'].to_cfg() + "\n",
                "address_hash=" +
                self.inputs['general_modeling']['memory']['l3_cache']['address_hash'].to_cfg() + "\n",
                "writethrough[]=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['writethrough']) + "\n",
                "cache_size[]=" + str(self.inputs['general_modeling']['memory']['l3_cache']['cache_size']) + "\n",
                "writeback_time[]=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['writeback_time']) + "\n",
                "associativity[]=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['associativity']) + "\n",
                "tags_access_time[]=" + str(
                    self.inputs['general_modeling']['memory']['l3_cache']['tags_access_time']) + "\n",
                "next_level_read_bandwidth[]="
                + str(self.inputs['general_modeling']['memory']['l3_cache']['next_level_read_bandwidth'])
                + "\n",
                "ports=" + str(self.inputs['general_modeling']['memory']['l3_cache']['ports']) + "\n",
                "data_access_time[]="
                + str(self.inputs['general_modeling']['memory']['l3_cache']['data_access_time'])
                + "\n\n",
            ])

        cfg_file.writelines([
            "[perf_model/dram]\n",
            "latency=" + str(self.inputs['general_modeling']['memory']['dram']['latency']) + "\n",
            "num_controllers=" + str(self.inputs['general_modeling']['memory']['dram']['num_controllers']) + "\n",
            "chips_per_dimm=" + str(self.inputs['general_modeling']['memory']['dram']['chips_per_dimm']) + "\n",
            "controllers_interleaving=" + str(
                self.inputs['general_modeling']['memory']['dram']['controllers_interleaving']) + "\n",
            "per_controller_bandwidth=" + str(
                self.inputs['general_modeling']['memory']['dram']['per_controller_bandwidth']) + "\n",
            "block_size=" + str(self.inputs['general_modeling']['memory']['dram']['block_size']) + "\n",
            "dimms_per_controller=" + str(
                self.inputs['general_modeling']['memory']['dram']['dimms_per_controller']) + "\n\n",
        ])

        cfg_file.writelines([
            "[perf_model/dram_directory]\n",
            "associativity="
            + str(self.inputs['general_modeling']['memory']['dram']['dram_directory']['associativity'])
            + "\n",
            "total_entries="
            + str(self.inputs['general_modeling']['memory']['dram']['dram_directory']['total_entries'])
            + "\n",
            "directory_type="
            + self.inputs['general_modeling']['memory']['dram']['dram_directory']['directory_type'].to_cfg()
            + "\n\n",
        ])

        cfg_file.writelines([
            "[network/emesh_hop_by_hop]\n",
            "link_bandwidth=" + str(self.inputs['general_modeling']['network']['emesh_hop_by_hop']['link_bandwidth'])
            + "\n",
            "concentration=" + str(self.inputs['general_modeling']['network']['emesh_hop_by_hop']['concentration'])
            + "\n",
            "wrap_around=" + str(self.inputs['general_modeling']['network']['emesh_hop_by_hop']['wrap_around'])
            + "\n",
            "hop_latency=" + str(self.inputs['general_modeling']['network']['emesh_hop_by_hop']['hop_latency'])
            + "\n",
            "dimensions=" + str(self.inputs['general_modeling']['network']['emesh_hop_by_hop']['dimensions'])
            + "\n\n",
        ])

        cfg_file.writelines([
            "[network/bus]\n",
            "bandwidth=" + str(self.inputs['general_modeling']['network']['bus']['bandwidth']) + "\n",
            "ignore_local_traffic=" + str(self.inputs['general_modeling']['network']['bus']['ignore_local_traffic'])
            + "\n\n",
        ])

        cfg_file.writelines([
            "[network/emesh_hop_counter]\n",
            "link_bandwidth=" + str(self.inputs['general_modeling']['network']['emesh_hop_counter']['link_bandwidth'])
            + "\n",
            "hop_latency="
            + str(self.inputs['general_modeling']['network']['emesh_hop_counter']['hop_latency'])
            + "\n\n",
        ])

        cfg_file.writelines([
            "[network]\n",
            "memory_model_1=" + self.inputs['general_modeling']['network']['memory_model_1'].to_cfg() + "\n\n",
        ])

        cfg_file.writelines([
            "[network]\n",
            "memory_model_2=" + self.inputs['general_modeling']['network']['memory_model_2'].to_cfg() + "\n\n",
        ])

        cfg_file.writelines([
            "[power]\n",
            "technology_node=" + str(self.inputs['general_modeling']['power']['technology_node']) + "\n",
            "vdd=" + str(
                self.inputs['general_modeling']['power']['vdd']) + "\n\n",
            # "temperature=" + str(self.inputs['general_modeling']['power']['temperature']) + "\n\n",
        ])

        cfg_file.close()

        self.cfg_path = cfg_file_path

    # todo
    def execute(self):
        self.prepare()

        self.execute_simulation()

        self.register_results()

    def prepare(self):
        json_path = PredictedCores.get_json_path(self.inputs['general_modeling']['model_name'])

        self.stash_user_inputs()

        self.set_values_from_json(json_path)

        self.pop_user_inputs()

        self.generate_cfg_from_inputs()

    def execute_simulation(self):
        print (
                self.get_executable_path() + "./run-sniper"
                + " -p " + str(self.get_benchmark_application())
                + " -n " + str(self.get_original_nbr_of_cores())
                + " -i " + str(self.get_benchmark_size())
                + " -c " + str(self.get_cfg_path())
                + " -d " + str(self.get_output_path())
                + "> " + str(self.get_output_path()) + "/sniper_output.out"
        )

        os.system(
            self.get_executable_path() + "./run-sniper"
            + " -p " + str(self.get_benchmark_application())
            + " -n " + str(self.get_original_nbr_of_cores())
            + " -i " + str(self.get_benchmark_size())
            + " -c " + str(self.get_cfg_path())
            + " -d " + str(self.get_output_path())
            + "> " + str(self.get_output_path()) + "/sniper_output.out"
        )

    def register_results(self):
        obj_result = sniper_lib.get_results(resultsdir=self.get_output_path())

        self.config = obj_result['config']

        self.results = obj_result['results']

        json_output_file_path = self.get_output_path() + "/sniper_config.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.config, json_output_file, indent=4)

        json_output_file_path = self.get_output_path() + "/sniper_results.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.results, json_output_file, indent=4)

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

    def get_results(self):
        pass


class McPATAdapter(Adapter):
    """
        This adapter utilises McPAT (an integrated power, area, and timing modeling framework for multithreading,
        multicore, and many-core architectures) to obtain the physical parameters  for a CPU architecture.
    """
    default_params = {
        "number_of_NoCs": "1",
        "homogeneous_ccs": "1",
        "homogeneous_NoCs": "1",
        "temperature": "370",
        "longer_channel_device": "1",
        "power_gating": "1",
        "machine_bits": "64",
        "virtual_address_width": "64",
        "physical_address_width": "52",
        "virtual_memory_page_size": "4096",
        "instruction_length": "64",
        "ALU_duty_cycle": "1",
        "MUL_duty_cycle": "0.3",
        "FPU_duty_cycle": "0.3",
        "ALU_cdb_duty_cycle": "1",
        "MUL_cdb_duty_cycle": "0.3",
        "FPU_cdb_duty_cycle": "0.3",
        "opt_local": "1",
        "opcode_width": "16",
        "number_instruction_fetch_ports": "1",
        "x86": "1",
        "micro_opcode_width": "8",
        "peak_issue_width": "6",
        "fp_issue_width": "2",
        "prediction_width": "1",
        "pipelines_per_core": "1,1",
        "pipeline_depth": "14,14",
        "ALU_per_core": "4",
        "MUL_per_core": "1",
        "FPU_per_core": "2",
        "instruction_buffer_size": "16",
        "decoded_stream_buffer_size": "16",
        "instruction_window_size": "64",
        "archi_Regs_IRF_size": "16",
        "archi_Regs_FRF_size": "32",
        "phy_Regs_IRF_size": "256",
        "phy_Regs_FRF_size": "256",
        "LSU_order": "inorder",
        "store_buffer_size": "96",
        "load_buffer_size": "48",
        "memory_ports": "1",
        "RAS_size": "64",
        "number_of_BPT": "2",
        "buffer_sizes": "16, 16, 16, 16",
        "BTB_config": "4096,4,2,1, 1,3",
        "ports": "1,1,1",
        "horizontal_nodes": "1",
        "vertical_nodes": "1",
        "link_throughput": "1",
        "link_latency": "1",
        "input_ports": "1",
        "output_ports": "1",
        "flit_bits": "256",
        "chip_coverage": "1",
        "link_routing_over_percentage": "0.5",
        "mc_clock": "200",
        "peak_transfer_rate": "3200",
        "block_size": "64",
        "memory_channels_per_mc": "1",
        "number_ranks": "2",
        "req_window_size_per_channel": "32",
        "IO_buffer_size_per_channel": "32",
        "databus_width": "128",
        "addressbus_width": "51",
    }

    def __init__(self):
        Adapter.__init__(self)

        self.input_xml = None
        self.sniper_simulation_path = None

    # todo
    def execute(self):
        time.sleep(6)

    @staticmethod
    def create_param_element(name, value):
        return ElementTree.Element("param", {
            "name": name,
            "value": value,
        })

    @staticmethod
    def create_stat_element(name, value):
        return ElementTree.Element("stat", {
            "name": name,
            "value": value,
        })

    @staticmethod
    def create_ignored_param_element(name):
        return McPATAdapter.create_param_element(name, str(0))

    @staticmethod
    def create_ignored_stat_element(name):
        return McPATAdapter.create_stat_element(name, str(0))

    def create_default_param_element(self, name):
        return McPATAdapter.create_param_element(name, str(self.default_params[name]))

    @staticmethod
    def create_param_elements(name_value_dict):
        param_elements = []

        for name in name_value_dict:
            param_elements.append(McPATAdapter.create_param_element(name, str(name_value_dict[name])))

        return param_elements

    @staticmethod
    def create_stat_elements(name_value_dict):
        stat_elements = []

        for name in name_value_dict:
            stat_elements.append(McPATAdapter.create_stat_element(name, str(name_value_dict[name])))

        return stat_elements

    def create_system_core_element(self, i):
        system_core_element = ElementTree.Element("component", {
            "id": "system.core" + str(i),
            "name": "core" + str(i),
        })

        return system_core_element

    # todo WIP
    def generate_xml_from_sniper_simulation(self):
        sniper_config = json.load(open(self.get_sniper_simulation_path() + "/sniper_config.json"))

        sniper_results = json.load(open(self.get_sniper_simulation_path() + "/sniper_results.json"))

        xml = ElementTree.fromstring('''<?xml version="1.0" encoding="UTF-8"?>
            <component id="root" name="root">
                <component id="system" name="system">
                </component>
            </component>
        ''')

        system = xml.find("component[@id='system']")

        number_of_cores = int(sniper_config["general/total_cores"])

        l2_shared_cores = number_of_l2 = l3_shared_cores = number_of_l3 = 0

        cache_levels = sniper_config["perf_model/cache/levels"]

        if cache_levels >= 2:
            l2_shared_cores = int(sniper_config["perf_model/l2_cache/shared_cores"])

            number_of_l2 = number_of_cores / l2_shared_cores

        if cache_levels >= 3:
            l3_shared_cores = int(sniper_config["perf_model/l3_cache/shared_cores"])

            number_of_l3 = number_of_cores / l3_shared_cores

        total_cycles = 0

        for val in sniper_results["performance_model.cycle_count"]:
            total_cycles = total_cycles + int(val)

        system.extend(self.create_param_elements({
            "number_of_cores": sniper_config["general/total_cores"],
            "number_cache_levels": cache_levels,
            "number_of_L2s": number_of_l2,
            "number_of_L3s": number_of_l3,
            "core_tech_node": sniper_config["power/technology_node"],
            "target_core_clockrate": int(float(sniper_config["perf_model/core/frequency"]) * 1000),
        }))

        system.extend(self.create_stat_elements({
            "total_cycles": total_cycles,
            "busy_cycles": total_cycles,
        }))

        system.extend([
            McPATAdapter.create_ignored_param_element("Private_L2"),
            McPATAdapter.create_ignored_param_element("number_of_L1Directories"),
            McPATAdapter.create_ignored_param_element("number_of_L2Directories"),
            McPATAdapter.create_ignored_param_element("homogeneous_L2s"),
            McPATAdapter.create_ignored_param_element("homogeneous_L1Directories"),
            McPATAdapter.create_ignored_param_element("homogeneous_L2Directories"),
            McPATAdapter.create_ignored_param_element("homogeneous_L3s"),
            McPATAdapter.create_ignored_param_element("interconnect_projection_type"),
            McPATAdapter.create_ignored_param_element("device_type"),
            McPATAdapter.create_ignored_param_element("homogeneous_cores"),
            McPATAdapter.create_ignored_stat_element("idle_cycles"),
            self.create_default_param_element("homogeneous_ccs"),
            self.create_default_param_element("homogeneous_NoCs"),
            self.create_default_param_element("temperature"),
            self.create_default_param_element("number_of_NoCs"),
            self.create_default_param_element("longer_channel_device"),
            self.create_default_param_element("power_gating"),
            self.create_default_param_element("machine_bits"),
            self.create_default_param_element("virtual_address_width"),
            self.create_default_param_element("physical_address_width"),
            self.create_default_param_element("virtual_memory_page_size"),
        ])

        for i in range(0, number_of_cores):
            system.append(self.create_system_core_element(i))
        # <component id="system.core0" name="core0">
        #      <param name="clock_rate" value="400"/>
        #      <param name="vdd" value="1.2"/>
        #      <param name="opt_local" value="1"/>
        #      <param name="instruction_length" value="64"/>
        #      <param name="opcode_width" value="16"/>
        #      <param name="machine_type" value="0"/>
        #      <param name="number_hardware_threads" value="1"/>
        #      <param name="fetch_width" value="10"/>
        #      <param name="number_instruction_fetch_ports" value="1"/>
        #      <param name="decode_width" value="10"/>
        #      <param name="x86" value="1"/>
        #      <param name="micro_opcode_width" value="8"/>
        #      <param name="issue_width" value="4"/>
        #      <param name="peak_issue_width" value="6"/>
        #      <param name="commit_width" value="10"/>
        #      <param name="fp_issue_width" value="2"/>
        #      <param name="prediction_width" value="1"/>
        #      <param name="pipelines_per_core" value="1,1"/>
        #      <param name="pipeline_depth" value="14,14"/>
        #      <param name="ALU_per_core" value="4"/>
        #      <param name="MUL_per_core" value="1"/>
        #      <param name="FPU_per_core" value="2"/>
        #      <param name="instruction_buffer_size" value="16"/>
        #      <param name="decoded_stream_buffer_size" value="16"/>
        #      <param name="instruction_window_scheme" value="0"/>
        #      <param name="instruction_window_size" value="64"/>
        #      <param name="fp_instruction_window_size" value="0"/>
        #      <param name="ROB_size" value="128"/>
        #      <param name="archi_Regs_IRF_size" value="16"/>
        #      <param name="archi_Regs_FRF_size" value="32"/>
        #      <param name="phy_Regs_IRF_size" value="256"/>
        #      <param name="phy_Regs_FRF_size" value="256"/>
        #      <param name="rename_scheme" value="0"/>
        #      <param name="register_windows_size" value="0"/>
        #      <param name="LSU_order" value="inorder"/>
        #      <param name="store_buffer_size" value="96"/>
        #      <param name="load_buffer_size" value="48"/>
        #      <param name="memory_ports" value="1"/>
        #      <param name="RAS_size" value="64"/>
        #      <param name="number_of_BPT" value="2"/>
        #      <stat name="total_instructions" value="23282822"/>
        #      <stat name="int_instructions" value="7241610"/>
        #      <stat name="fp_instructions" value="7241610"/>
        #      <stat name="branch_instructions" value="783721"/>
        #      <stat name="branch_mispredictions" value="5184"/>
        #      <stat name="load_instructions" value="5261387"/>
        #      <stat name="store_instructions" value="1505744"/>
        #      <stat name="committed_instructions" value="23282822"/>
        #      <stat name="committed_int_instructions" value="7241610"/>
        #      <stat name="committed_fp_instructions" value="7241610"/>
        #      <stat name="total_cycles" value="18275571.125"/>
        #      <stat name="idle_cycles" value="627.125"/>
        #      <stat name="busy_cycles" value="18274944"/>
        #      <stat name="ROB_reads" value="24108400"/>
        #      <stat name="ROB_writes" value="24108400"/>
        #      <stat name="rename_reads" value="23282822"/>
        #      <stat name="rename_writes" value="23282822"/>
        #      <stat name="fp_rename_reads" value="0"/>
        #      <stat name="fp_rename_writes" value="0"/>
        #      <stat name="inst_window_reads" value="23282822"/>
        #      <stat name="inst_window_writes" value="23282822"/>
        #      <stat name="inst_window_wakeup_accesses" value="23282822"/>
        #      <stat name="fp_inst_window_reads" value="23282822"/>
        #      <stat name="fp_inst_window_writes" value="23282822"/>
        #      <stat name="fp_inst_window_wakeup_accesses" value="23282822"/>
        #      <stat name="int_regfile_reads" value="7241610"/>
        #      <stat name="float_regfile_reads" value="7241610"/>
        #      <stat name="int_regfile_writes" value="7241610"/>
        #      <stat name="float_regfile_writes" value="7241610"/>
        #      <stat name="function_calls" value="0"/>
        #      <stat name="context_switches" value="0"/>
        #      <stat name="ialu_accesses" value="7241610"/>
        #      <stat name="fpu_accesses" value="7241610"/>
        #      <stat name="mul_accesses" value="7241610"/>
        #      <stat name="cdb_alu_accesses" value="7241610"/>
        #      <stat name="cdb_mul_accesses" value="7241610"/>
        #      <stat name="cdb_fpu_accesses" value="7241610"/>
        #      <stat name="IFU_duty_cycle" value="1.27398601339"/>
        #      <stat name="LSU_duty_cycle" value="0"/>
        #      <stat name="MemManU_I_duty_cycle" value="1.27398601339"/>
        #      <stat name="MemManU_D_duty_cycle" value="0"/>
        #      <stat name="ALU_duty_cycle" value="1"/>
        #      <stat name="MUL_duty_cycle" value="0.3"/>
        #      <stat name="FPU_duty_cycle" value="0.3"/>
        #      <stat name="ALU_cdb_duty_cycle" value="1"/>
        #      <stat name="MUL_cdb_duty_cycle" value="0.3"/>
        #      <stat name="FPU_cdb_duty_cycle" value="0.3"/>
        #
        #      <component id="system.core0.itlb" name="itlb"><param name="number_entries" value="64"/>
        #          <stat name="total_accesses" value="3954162"/>
        #          <stat name="total_misses" value="20"/>
        #          <stat name="conflicts" value="0"/>
        #      </component>
        #
        #      <component id="system.core0.icache" name="icache">
        #          <param name="icache_config" value="8192,32,2,1,3,4,16,1"/>
        #          <param name="buffer_sizes" value="16, 16, 16, 16"/>
        #          <stat name="read_accesses" value="3954162"/>
        #          <stat name="read_misses" value="205221"/>
        #          <stat name="conflicts" value="0"/>
        #      </component>
        #
        #      <component id="system.core0.dtlb" name="dtlb"><param name="number_entries" value="64"/>
        #          <stat name="total_accesses" value="7094619"/>
        #          <stat name="total_misses" value="547"/>
        #          <stat name="conflicts" value="0"/>
        #      </component>
        #
        #      <component id="system.core0.dcache" name="dcache">
        #          <param name="dcache_config" value="8192,32,2,1,3,4,16,1"/>
        #          <param name="buffer_sizes" value="16, 16, 16, 16"/>
        #          <stat name="read_accesses" value="5507084"/>
        #          <stat name="write_accesses" value="1587535"/>
        #          <stat name="read_misses" value="770283"/>
        #          <stat name="write_misses" value="290369"/>
        #          <stat name="conflicts" value="0"/>
        #      </component>
        #
        #      <component id="system.core0.BTB" name="BTB">
        #          <param name="BTB_config" value="4096,4,2,1, 1,3"/>
        #          <stat name="read_accesses" value="783721"/>
        #          <stat name="write_accesses" value="0"/>
        #      </component>
        #  </component>

        self.input_xml = xml

    def get_sniper_simulation_path(self):
        if self.sniper_simulation_path is None:
            return self.get_output_path()

        return self.sniper_simulation_path


class NsgaIIPredDSEAdapter(Adapter):
    """
        This adapter uses a NSGA-II implementation as it's exploration engine, and a heterogeneous multicore CPU
        architecture performance predictor as it's evaluation engine, in order to perform a design space exploration.
    """

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
