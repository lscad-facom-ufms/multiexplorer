﻿# -*- coding: utf-8 -*-
import json
import os
import sys
import re
from MultiExplorer.src.config import PATH_SNIPER, PATH_MCPAT
sys.path.append(PATH_SNIPER + '/tools')
import sniper_lib
from typing import Dict, Union, Any, Optional
from xml.dom import minidom
from xml.etree import ElementTree
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.AllowedValues import PredictedCores, \
    SniperCorePipelineKinds, \
    CachePolicies, HashTypes, PerformanceModelTypes, Domains, Prefetchers, DramDirectoryTypes, MemoryModels, \
    Technologies, Applications
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.DSDSE.Nsga2Main import Nsga2Main
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.DSDSE.brute_force.DsDseBruteForce import DsDseBruteForce
from MultiExplorer.src.CPUHeterogeneousMulticoreExploration.Presenters import SniperPresenter
from MultiExplorer.src.Infrastructure.ExecutionFlow import Adapter
from MultiExplorer.src.Infrastructure.Inputs import Input, InputGroup, InputType


class SniperSimulatorAdapter(Adapter):
    """
    This adapter utilises Sniper Multi-Core Simulator to execute a performance evaluation of a CPU architecture
    through simulation.
    """

    def __init__(self):
        Adapter.__init__(self)

        self.presenter = None  # type: Optional[SniperPresenter]

        self.set_inputs([
            Input({
                'label': 'Application',
                'key': 'application',
                'allowed_values': Applications.get_dict(),
                'value': Applications.SPLASH_II_CHOLESKY.value,
            }),
            InputGroup({
                "label": "Original Platform",
                "subtitle": (
                    "This platform will be the starting point for the automatic DSE."
                    + " It will be evaluated through simulation by Sniper and McPAT."
                ),
                "key": "general_modeling",
                "inputs": [
                    Input({
                        "label": "Core Model",
                        "key": "model_name",
                        "is_user_input": True,
                        "required": True,
                        "allowed_values": PredictedCores.get_dict(),
                        "additional_info": PredictedCores.get_info_dict()
                    }),
                    Input({
                        "label": "Number of Cores",
                        "key": "total_cores",
                        "is_user_input": True,
                        "required": True,
                        "type": InputType.Integer,
                        "max_val": 32,
                    }),
                    InputGroup({
                        "label": "Core Specifications",
                        "key": "core",
                        "inputs": [
                            Input({
                                "label": "Global Frequency",
                                "unit": 'MHz',
                                "key": "global_frequency",
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
                                "allowed_values": Technologies.get_dict(),
                                "required": True,
                                "is_user_input": True,
                                'unit': 'nm',
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

        self.inputs['general_modeling']['total_cores'] = int(input_json['General_Modeling']['total_cores'])

        global_frequency = int(input_json['General_Modeling']['core']['global_frequency'])
        self.inputs['general_modeling']['core']['global_frequency'] = global_frequency

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

        if 'block_size' in input_json['General_Modeling']['memory']['dram']:
            self.inputs['general_modeling']['memory']['dram']['block_size'] = \
                input_json['General_Modeling']['memory']['dram']['block_size']

        if 'emesh_hop_by_hop' in input_json['General_Modeling']['network']:
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

        if 'emesh_hop_counter' in input_json['General_Modeling']['network']:
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

    # Returns the float value of the global frequency for the original core in GHz
    def get_global_frequency(self):
        # type: () -> float
        return float(self.inputs['general_modeling']['core']['global_frequency']) / 1000.0

    def generate_cfg_from_inputs(self):
        cfg_file_path = self.get_output_path() + "/sniper_input.cfg"

        cfg_file = open(cfg_file_path, 'w+')

        cfg_file.writelines([
            "#include nehalem\n",
            "[general]\n",
            "total_cores=" + str(self.inputs['general_modeling']['total_cores']) + "\n\n",
        ])

        global_frequency = str(self.get_global_frequency())

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

            dram_lines = [
                "[perf_model/dram]\n",
                "latency=" + str(self.inputs['general_modeling']['memory']['dram']['latency']) + "\n",
                "num_controllers=" + str(self.inputs['general_modeling']['memory']['dram']['num_controllers']) + "\n",
                "chips_per_dimm=" + str(self.inputs['general_modeling']['memory']['dram']['chips_per_dimm']) + "\n",
                "controllers_interleaving=" + str(
                    self.inputs['general_modeling']['memory']['dram']['controllers_interleaving']) + "\n",
                "per_controller_bandwidth=" + str(
                    self.inputs['general_modeling']['memory']['dram']['per_controller_bandwidth']) + "\n",
                "dimms_per_controller=" + str(
                    self.inputs['general_modeling']['memory']['dram']['dimms_per_controller']) + "\n\n",
            ]

            if self.inputs['general_modeling']['memory']['dram']['block_size'] is not None:
                dram_lines.append(
                    "block_size="
                    + str(self.inputs['general_modeling']['memory']['dram']['block_size']) + "\n"
                )

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

        if self.inputs['general_modeling']['network']['emesh_hop_by_hop']['link_bandwidth'] is not None:
            cfg_file.writelines([
                "[network/emesh_hop_by_hop]\n",
                "link_bandwidth=" + str(
                    self.inputs['general_modeling']['network']['emesh_hop_by_hop']['link_bandwidth'])
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

        if self.inputs['general_modeling']['network']['emesh_hop_counter']['link_bandwidth'] is not None:
            cfg_file.writelines([
                "[network/emesh_hop_counter]\n",
                "link_bandwidth=" + str(
                    self.inputs['general_modeling']['network']['emesh_hop_counter']['link_bandwidth'])
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

        self.register_dse_settings()

    def get_processor(self):
        try:
            return PredictedCores.get_processor(self.inputs['general_modeling']['model_name'])
        except ValueError:
            return ""

    def get_input_technology(self):
        return str(self.inputs['general_modeling']['power']['technology_node']) + "nm"

    def get_technology(self):
        return str(self.inputs['general_modeling']['power']['technology_node']) + "nm"

    # This method forwards settings to the DSE Step through a json file
    def register_dse_settings(self):
        try:
            dse_settings_json = json.loads(open(self.get_dse_settings_file_path(), 'r+').read())
        except (OSError, ValueError, IOError):
            dse_settings_json = {}

        str(self.inputs['application'].value).split('-')

        benchmark, application = str(self.inputs['application'].value).split('-')

        dse_settings_json['benchmark'] = benchmark

        dse_settings_json['application'] = application

        dse_settings_json['processor'] = self.get_processor()

        dse_settings_json['technology'] = self.get_technology()

        dse_settings_json['frequency'] = self.get_global_frequency()

        open(self.get_dse_settings_file_path(), 'w+').write(json.dumps(dse_settings_json, sort_keys=True, indent=4))

    def get_dse_settings_file_path(self):
        return self.get_output_path() + "/" + self.get_dse_settings_file_name()

    def get_dse_settings_file_name(self):
        if self.dse_settings_file_name is None:
            return "dse_settings.json"

        return self.get_dse_settings_file_name

    def execute_simulation(self):
        print (
                self.get_executable_path() + "./run-sniper"
                + " -p " + str(self.get_benchmark_application())
                + " -n " + str(self.get_original_nbr_of_cores())
                + " -i " + str(self.get_benchmark_size())
                + " -c " + str(self.get_cfg_path())
                + " -d " + str(self.get_output_path())
                + "> " + str(self.get_output_path()) + "/sniper.out"
        )

        os.system(
            self.get_executable_path() + "./run-sniper"
            + " -p " + str(self.get_benchmark_application())
            + " -n " + str(self.get_original_nbr_of_cores())
            + " -i " + str(self.get_benchmark_size())
            + " -c " + str(self.get_cfg_path())
            + " -d " + str(self.get_output_path())
            + "> " + str(self.get_output_path()) + "/sniper.out"
        )

    def register_results(self):
        obj_result = sniper_lib.get_results(resultsdir=self.get_output_path())

        self.config = obj_result['config']

        self.results = obj_result['results']

        elapsed_time = self.results['performance_model.elapsed_time'][0]

        self.presentable_results = {
            'orig_core': self.get_processor() + "_" + self.get_technology(),
            'total_cores': int(self.config["general/total_cores"]),
            'elapsed_time': (elapsed_time, 'fs'),  # elapsed time is in femtoseconds (fs) (for Snipersim 7.4)
        }

        total_ic = 0

        for ic in self.results['performance_model.instruction_count']:
            total_ic += ic

        self.presentable_results['total_instruction_count'] = (total_ic, 'I')

        self.presentable_results['total_cycle_count'] = (
            round(self.results['performance_model.cycle_count'][0], 2), 'C'
        )

        total_ipc = 0

        for ipc in self.results['ipc']:
            total_ipc += ipc

        self.presentable_results['ipc'] = (round(total_ipc, 2), 'IPC')

        self.presentable_results['performance'] = (round(10.0 ** 15 / elapsed_time, 2), 's^-1')

        self.presenter = SniperPresenter()

        json_output_file_path = self.get_output_path() + "/sniper_config.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.config, json_output_file, indent=4)

        json_output_file_path = self.get_output_path() + "/sniper_results.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.results, json_output_file, indent=4)

        json_output_file_path = self.get_output_path() + "/sniper_presentable_results.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.presentable_results, json_output_file, indent=4)

        try:
            dse_settings_json = json.loads(open(self.get_dse_settings_file_path(), 'r+').read())
        except (OSError, ValueError, IOError):
            dse_settings_json = {}
        dse_settings_json['original_performance'] = self.presentable_results['performance']

        open(self.get_dse_settings_file_path(), 'w+').write(json.dumps(dse_settings_json, sort_keys=True, indent=4))

    def get_original_nbr_of_cores(self):
        return self.inputs["general_modeling"].inputs["total_cores"].value

    def get_benchmark_application(self):
        return self.inputs["application"].value

    def get_executable_path(self):
        if self.use_benchmarks is True:
            return PATH_SNIPER + "/benchmarks/"
        else:
            return PATH_SNIPER + "/"

    def get_benchmark_size(self):
        if self.benchmark_size is None:
            return "test"

        return self.benchmark_size

    def get_cfg_path(self):
        if self.cfg_path is None:
            return PATH_SNIPER + "/config/processor.config"

        return self.cfg_path

    def get_results(self):
        return self.presentable_results


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
        "fetch_width": "10",
        "decode_width": "10",
        "commit_width": "10",
    }

    def __init__(self):
        Adapter.__init__(self)

        self.input_file_name = None

        self.output_file_name = None

        self.results_file_name = None

        self.executable_path = None

        self.sniper_results = None

        self.sniper_config = None

        self.input_xml = None

        self.sniper_simulation_path = None

        self.results = None

        self.presentable_results = None

    def execute(self):
        self.prepare()

        self.execute_simulation()

        self.register_results()

    def write_input_xml_to_file(self):
        xmlstr = minidom.parseString(ElementTree.tostring(self.input_xml.getroot())).toprettyxml(indent="   ")

        with open(self.get_input_file_path(), "w") as f:
            f.write(xmlstr.encode('utf-8'))

    def prepare(self):
        self.generate_xml_from_sniper_simulation()

        self.write_input_xml_to_file()

    def get_executable_path(self):
        if self.executable_path is None:
            return PATH_MCPAT + "/"

        return self.executable_path + "/"

    def get_input_file_name(self):
        if self.input_file_name is None:
            return "mcpat_input.xml"

        return self.input_file_name

    def get_input_file_path(self):
        return self.get_output_path() + "/" + self.get_input_file_name()

    def get_output_file_name(self):
        if self.output_file_name is None:
            return "mcpat.out"

        return self.output_file_name

    def get_results_file_name(self):
        if self.results_file_name is None:
            return "mcpat_results.json"

        return self.results_file_name

    def get_output_file_path(self):
        return self.get_output_path() + "/" + self.get_output_file_name()

    def get_results_file_path(self):
        return self.get_output_path() + "/" + self.get_results_file_name()

    def execute_simulation(self):
        print (
                self.get_executable_path() + "./mcpat"
                + " -infile " + self.get_input_file_path()
                + " -print_level 5 > " + self.get_output_file_path()
        )

        os.system(
            self.get_executable_path() + "./mcpat"
            + " -infile " + self.get_input_file_path()
            + " -print_level 5 > " + self.get_output_file_path()
        )

    def get_results(self):
        return self.presentable_results

    def register_results(self):
        output_file = open(self.get_output_file_path(), 'r')

        self.results = {}

        scope_regex = re.compile('([a-zA-Z \d(/)]+)( \(Count: *\d *\))?:( \d+ cores)? *\n')

        key_value_regex = re.compile('([a-zA-Z *%]*[a-zA-Z]) = ([+-]?\d+\.\d+(e[+-]\d+)?)( ([a-zA-Z\d^]+))?')

        scope = None

        for line in output_file.readlines():
            scope_match = scope_regex.search(line)

            if scope_match is not None:
                scope = scope_match.group(1).strip("\t\n *:").replace(" ", "_").replace("(", "").replace(")", "") \
                    .replace("/", "_").lower()

                self.results[scope] = {}

                continue

            if scope is None:
                continue

            key_value_match = key_value_regex.search(line)

            if key_value_match is None:
                continue

            key, value, measurement_unit = key_value_match.group(1, 2, 5)

            pretty_key = key.strip("\t *:").replace(" ", "_").lower()

            if pretty_key not in self.results[scope]:
                self.results[scope][pretty_key] = float(value), measurement_unit

        results_file = open(self.get_results_file_path(), 'w+')

        results_file.write(json.dumps(self.results, indent=4, sort_keys=True))

        self.presentable_results = {
            'power_density': (
                round(self.results['processor']['power_density'][0], 2),
                'W/mm^2'
            ),
            'area': (
                round(self.results['processor']['area'][0], 2),
                self.results['processor']['area'][1]
            ),
            'core_area': (
                round(self.results['total_cores']['area'][0], 2),
                self.results['core']['area'][1]
            ),
            'ds_area': (
                round(self.results['integer_alus']['area_ds'][0], 2),
                'mm^2'
            ),
            'ds_percentage':  (
                round(self.results['integer_alus']['%ds'][0], 2),
                '%'
            ),
        }

        json_output_file_path = self.get_output_path() + "/mcpat_presentable_results.json"

        with open(json_output_file_path, 'w') as json_output_file:
            json.dump(self.presentable_results, json_output_file, indent=4)

    @staticmethod
    def create_param_element(name, value):
        return ElementTree.Element("param", {
            "name": name,
            "value": str(value),
        })

    @staticmethod
    def create_stat_element(name, value):
        return ElementTree.Element("stat", {
            "name": name,
            "value": str(value),
        })

    @staticmethod
    def create_ignored_param_element(name):
        return McPATAdapter.create_param_element(name, str(0))

    @staticmethod
    def create_ignored_param_elements(name_list):
        ignored_param_elements = []

        for name in name_list:
            ignored_param_elements.append(McPATAdapter.create_ignored_param_element(name))

        return ignored_param_elements

    @staticmethod
    def create_ignored_stat_element(name):
        return McPATAdapter.create_stat_element(name, str(0))

    @staticmethod
    def create_ignored_stat_elements(name_list):
        ignored_stat_elements = []

        for name in name_list:
            ignored_stat_elements.append(McPATAdapter.create_ignored_stat_element(name))

        return ignored_stat_elements

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

    def create_default_param_element(self, name):
        return McPATAdapter.create_param_element(name, str(self.default_params[name]))

    def create_default_param_elements(self, name_list):
        default_param_elements = []

        for name in name_list:
            default_param_elements.append(self.create_default_param_element(name))

        return default_param_elements

    def get_icache_config(self):
        icache_configurations = [
            str(1024 * int(self.sniper_config["perf_model/l1_icache/cache_size"])),
            self.sniper_config["perf_model/l1_icache/cache_block_size"],
            self.sniper_config["perf_model/l1_icache/associativity"],
            "1",
            "3",
            self.sniper_config["perf_model/l1_icache/data_access_time"],
            "16",
            "1",
        ]

        return ",".join(icache_configurations)

    def create_core_icache_component(self, i):
        core_icache_component = ElementTree.Element("component", {
            "id": "system.core" + str(i) + ".icache",
            "name": "core" + str(i),
        })

        core_icache_component.extend([
            McPATAdapter.create_param_element("icache_config", self.get_icache_config()),
            self.create_default_param_element("buffer_sizes"),
        ])

        core_icache_component.extend([
            McPATAdapter.create_stat_element("read_accesses", self.sniper_results["L1-I.loads"][i]),
            McPATAdapter.create_stat_element("read_misses", self.sniper_results["L1-I.load-misses-I"][i]),
            McPATAdapter.create_ignored_stat_element("conflicts"),
        ])

        return core_icache_component

    def get_dcache_config(self):
        dcache_configurations = [
            str(1024 * int(self.sniper_config["perf_model/l1_dcache/cache_size"])),
            self.sniper_config["perf_model/l1_dcache/cache_block_size"],
            self.sniper_config["perf_model/l1_dcache/associativity"],
            "1",
            "3",
            self.sniper_config["perf_model/l1_dcache/data_access_time"],
            "16",
            "1",
        ]

        return ",".join(dcache_configurations)

    def create_core_dcache_component(self, i):
        core_dcache_component = ElementTree.Element("component", {
            "id": "system.core" + str(i) + ".dcache",
            "name": "core" + str(i),
        })

        core_dcache_component.extend([
            McPATAdapter.create_param_element("dcache_config", self.get_dcache_config()),
            self.create_default_param_element("buffer_sizes"),
        ])

        core_dcache_component.extend([
            McPATAdapter.create_stat_element("read_accesses", self.sniper_results["L1-D.loads"][i]),
            McPATAdapter.create_stat_element("write_accesses", self.sniper_results["L1-D.stores"][i]),
            McPATAdapter.create_stat_element("read_misses", self.sniper_results["L1-D.load-misses"][i]),
            McPATAdapter.create_stat_element("write_misses", self.sniper_results["L1-D.store-misses"][i]),
            McPATAdapter.create_ignored_stat_element("conflicts"),
        ])

        return core_dcache_component

    def create_core_itlb_component(self, i):
        core_itlb_component = ElementTree.Element("component", {
            "id": "system.core" + str(i) + ".itlb",
            "name": "core" + str(i),
        })

        core_itlb_component.extend([
            McPATAdapter.create_param_element("number_entries", self.sniper_config["perf_model/itlb/sets"]),
            McPATAdapter.create_stat_element("total_accesses", self.sniper_results["itlb.access"][i]),
            McPATAdapter.create_stat_element("total_misses", self.sniper_results["itlb.miss"][i]),
            McPATAdapter.create_ignored_stat_element("conflicts"),
        ])

        return core_itlb_component

    def create_core_dtlb_component(self, i):
        core_dtlb_component = ElementTree.Element("component", {
            "id": "system.core" + str(i) + ".dtlb",
            "name": "core" + str(i),
        })

        core_dtlb_component.extend([
            McPATAdapter.create_param_element("number_entries", self.sniper_config["perf_model/dtlb/sets"]),
            McPATAdapter.create_stat_element("total_accesses", self.sniper_results["dtlb.access"][i]),
            McPATAdapter.create_stat_element("total_misses", self.sniper_results["dtlb.miss"][i]),
            McPATAdapter.create_ignored_stat_element("conflicts"),
        ])

        return core_dtlb_component

    def create_core_btb_component(self, i):
        core_btb_component = ElementTree.Element("component", {
            "id": "system.core" + str(i) + ".BTB",
            "name": "core" + str(i),
        })

        core_btb_component.append(self.create_default_param_element("BTB_config"))

        core_btb_component.append(McPATAdapter.create_stat_element(
            "read_accesses",
            self.sniper_results["interval_timer.uop_branch"][i])
        )

        core_btb_component.append(McPATAdapter.create_ignored_stat_element("write_accesses"))

        return core_btb_component

    def create_system_core_component(self, i):
        system_core_component = ElementTree.Element("component", {
            "id": "system.core" + str(i),
            "name": "core" + str(i),
        })

        system_core_component.extend(self.create_param_elements({
            "clock_rate": self.get_target_core_clockrate(),
            "vdd": self.sniper_config["power/vdd"],
            "number_hardware_threads": self.sniper_config["perf_model/core/logical_cpus"],
            "issue_width": self.sniper_config["perf_model/core/interval_timer/dispatch_width"],
            "ROB_size": self.sniper_config["perf_model/core/interval_timer/window_size"],
        }))

        system_core_component.extend(self.create_default_param_elements([
            "opt_local",
            "instruction_length",
            "opcode_width",
            "fetch_width",
            "number_instruction_fetch_ports",
            "decode_width",
            "x86",
            "micro_opcode_width",
            "peak_issue_width",
            "commit_width",
            "fp_issue_width",
            "prediction_width",
            "pipelines_per_core",
            "pipeline_depth",
            "ALU_per_core",
            "MUL_per_core",
            "FPU_per_core",
            "instruction_buffer_size",
            "decoded_stream_buffer_size",
            "instruction_window_size",
            "archi_Regs_IRF_size",
            "archi_Regs_FRF_size",
            "phy_Regs_IRF_size",
            "phy_Regs_FRF_size",
            "LSU_order",
            "store_buffer_size",
            "load_buffer_size",
            "memory_ports",
            "RAS_size",
            "number_of_BPT",
        ]))

        system_core_component.extend(self.create_ignored_param_elements([
            "machine_type",
            "instruction_window_scheme",
            "fp_instruction_window_size",
            "rename_scheme",
            "register_windows_size",
        ]))

        system_core_component.append(self.create_core_icache_component(i))

        system_core_component.append(self.create_core_dcache_component(i))

        system_core_component.append(self.create_core_itlb_component(i))

        system_core_component.append(self.create_core_dtlb_component(i))

        system_core_component.append(self.create_core_btb_component(i))

        return system_core_component

    def get_cache_lx_config(self, x):
        lx_settings = [
            str(1024 * int(self.sniper_config["perf_model/l" + str(x) + "_cache/cache_size"])),
            self.sniper_config["perf_model/l" + str(x) + "_cache/cache_block_size"],
            self.sniper_config["perf_model/l" + str(x) + "_cache/associativity"],
            "8",
            "8",
            self.sniper_config["perf_model/l" + str(x) + "_cache/data_access_time"],
            "32",
            "0",
        ]

        return ",".join(lx_settings)

    def create_system_cache_lx_component(self, x, i):
        lx_component = ElementTree.Element("component", {
            "id": "system.L" + str(x) + str(i),
            "name": "L" + str(x) + str(i),
        })

        lx_component.extend([
            McPATAdapter.create_param_element("L" + str(x) + "_config", self.get_cache_lx_config(x)),
            self.create_default_param_element("buffer_sizes"),
            McPATAdapter.create_param_element("clockrate", self.get_target_core_clockrate()),
            McPATAdapter.create_param_element("vdd", self.sniper_config["power/vdd"]),
            self.create_default_param_element("ports"),
            McPATAdapter.create_ignored_param_element("device_type"),
        ])

        lx_component.extend(
            McPATAdapter.create_stat_elements({
                "read_accesses": self.sniper_results["L" + str(x) + ".loads-I"][i],
                "write_accesses": self.sniper_results["L" + str(x) + ".stores"][i],
                "read_misses": self.sniper_results["L" + str(x) + ".load-misses"][i],
                "write_misses": self.sniper_results["L" + str(x) + ".store-misses"][i],
            })
        )

        lx_component.extend(
            McPATAdapter.create_ignored_stat_elements([
                "conflicts",
                "duty_cycle",
            ])
        )

        return lx_component

    def create_system_noc_component(self, i):
        noc_component = ElementTree.Element("component", {
            "id": "system.NoC" + str(i),
            "name": "noc" + str(i),
        })

        noc_component.extend(McPATAdapter.create_param_elements({
            "clockrate": self.get_target_core_clockrate(),
            "vdd": self.sniper_config["power/vdd"],
            "type": self.sniper_config["network/memory_model_1"],
        }))

        noc_component.extend(self.create_default_param_elements([
            "horizontal_nodes",
            "vertical_nodes",
            "link_throughput",
            "link_latency",
            "input_ports",
            "flit_bits",
            "link_routing_over_percentage",
            "output_ports",
            "chip_coverage",
        ]))

        noc_component.extend(McPATAdapter.create_ignored_param_elements([
            "has_global_link",
        ]))

        noc_component.extend(McPATAdapter.create_ignored_stat_elements([
            "total_accesses",
            "duty_cycle",
        ]))

        return noc_component

    def create_system_memory_controller_component(self):
        mc_component = ElementTree.Element("component", {
            "id": "system.mc",
            "name": "mc",
        })

        mc_component.extend(self.create_default_param_elements([
            "mc_clock",
            "peak_transfer_rate",
            "block_size",
            "memory_channels_per_mc",
            "number_ranks",
            "req_window_size_per_channel",
            "IO_buffer_size_per_channel",
            "databus_width",
            "addressbus_width",
        ]))

        mc_component.extend(McPATAdapter.create_ignored_param_elements([
            "vdd",
            "number_mcs",
            "withPHY",
        ]))

        mc_component.extend(McPATAdapter.create_stat_elements({
            "memory_accesses": self.sniper_results["dram-queue.num-requests"][0],
            "memory_reads": self.sniper_results["dram-queue.num-requests"][0] - self.sniper_results["dram.writes"][0],
            "memory_writes": self.sniper_results["dram.writes"][0],
        }))

        return mc_component

    @staticmethod
    def create_system_niu_component():
        niu_component = ElementTree.Element("component", {
            "id": "system.niu",
            "name": "niu",
        })

        niu_component.extend(McPATAdapter.create_ignored_param_elements([
            "type",
            "clockrate",
            "vdd",
            "number_units",
        ]))

        niu_component.extend(McPATAdapter.create_ignored_stat_elements([
            "duty_cycle",
            "total_load_perc",
        ]))

        return niu_component

    @staticmethod
    def create_system_pcie_component():
        pcie_component = ElementTree.Element("component", {
            "id": "system.pcie",
            "name": "pcie",
        })

        pcie_component.extend(McPATAdapter.create_ignored_param_elements([
            "type",
            "withPHY",
            "clockrate",
            "vdd",
            "number_units",
            "num_channels",
        ]))

        pcie_component.extend(McPATAdapter.create_ignored_stat_elements([
            "duty_cycle",
            "total_load_perc",
        ]))

        return pcie_component

    @staticmethod
    def create_system_flashc_component():
        flashc_component = ElementTree.Element("component", {
            "id": "system.flashc",
            "name": "flashc",
        })

        flashc_component.extend(McPATAdapter.create_ignored_param_elements([
            "number_flashcs",
            "type",
            "withPHY",
            "peak_transfer_rate",
            "vdd",
        ]))

        flashc_component.extend(McPATAdapter.create_ignored_stat_elements([
            "duty_cycle",
            "total_load_perc",
        ]))

        return flashc_component

    def get_cache_numbers(self):
        number_of_cores = int(self.sniper_config["general/total_cores"])

        cache_levels = int(self.sniper_config["perf_model/cache/levels"])

        l2_shared_cores = number_of_l2 = l3_shared_cores = number_of_l3 = 0

        if cache_levels >= 2:
            l2_shared_cores = int(self.sniper_config["perf_model/l2_cache/shared_cores"])

            number_of_l2 = number_of_cores / l2_shared_cores

        if cache_levels >= 3:
            l3_shared_cores = int(self.sniper_config["perf_model/l3_cache/shared_cores"])

            number_of_l3 = number_of_cores / l3_shared_cores

        return number_of_cores, cache_levels, l2_shared_cores, number_of_l2, l3_shared_cores, number_of_l3

    def get_total_cycles(self):
        total_cycles = 0

        for val in self.sniper_results["performance_model.cycle_count"]:
            total_cycles = total_cycles + int(val)

        return total_cycles

    def get_target_core_clockrate(self):
        return int(float(self.sniper_config["perf_model/core/frequency"]) * 1000)

    def generate_xml_from_sniper_simulation(self):
        self.sniper_config = json.load(open(self.get_sniper_simulation_path() + "/sniper_config.json", 'r+'))

        self.sniper_results = json.load(open(self.get_sniper_simulation_path() + "/sniper_results.json", 'r+'))

        xml = ElementTree.ElementTree(ElementTree.fromstring('''<?xml version="1.0" encoding="UTF-8"?>
            <component id="root" name="root">
                <component id="system" name="system">
                </component>
            </component>
        '''))

        system = xml.find("component[@id='system']")

        number_of_cores, cache_levels, l2_shared_cores, number_of_l2, l3_shared_cores, number_of_l3 = \
            self.get_cache_numbers()

        total_cycles = self.get_total_cycles()

        system.extend(self.create_param_elements({
            "number_of_cores": self.sniper_config["general/total_cores"],
            "number_cache_levels": cache_levels,
            "number_of_L2s": number_of_l2,
            "number_of_L3s": number_of_l3,
            "core_tech_node": self.sniper_config["power/technology_node"],
            "target_core_clockrate": self.get_target_core_clockrate(),
        }))

        system.extend(self.create_default_param_elements([
            "homogeneous_ccs",
            "homogeneous_NoCs",
            "temperature",
            "number_of_NoCs",
            "longer_channel_device",
            "power_gating",
            "machine_bits",
            "virtual_address_width",
            "physical_address_width",
            "virtual_memory_page_size",
        ]))

        system.extend(McPATAdapter.create_ignored_param_elements([
            "Private_L2",
            "number_of_L1Directories",
            "number_of_L2Directories",
            "homogeneous_L2s",
            "homogeneous_L1Directories",
            "homogeneous_L2Directories",
            "homogeneous_L3s",
            "interconnect_projection_type",
            "device_type",
            "homogeneous_cores",
        ]))

        system.extend(self.create_stat_elements({
            "total_cycles": total_cycles,
            "busy_cycles": total_cycles,
        }))

        system.append(McPATAdapter.create_ignored_stat_element("idle_cycles"))

        for i in range(0, number_of_cores):
            system.append(self.create_system_core_component(i))

        if cache_levels >= 2:
            for i in range(0, number_of_l2):
                system.append(self.create_system_cache_lx_component(2, i))

        if cache_levels >= 3:
            for i in range(0, number_of_l3):
                system.append(self.create_system_cache_lx_component(3, i))

        for i in range(0, int(self.default_params["number_of_NoCs"])):
            system.append(self.create_system_noc_component(i))

        system.append(self.create_system_memory_controller_component())

        system.append(McPATAdapter.create_system_niu_component())

        system.append(McPATAdapter.create_system_pcie_component())

        system.append(McPATAdapter.create_system_flashc_component())

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

        self.project_path = None

        self.dse_settings_file_name = None

        self.dse_settings = None  # type: Optional[Dict[str, Any]]

        self.mcpat_results_json_file_name = None

        self.mcpat_results = None

        self.sniper_results_json_file_name = None

        self.sniper_results = None

        self.inputs = {}  # type: Dict[str, Union[Input, InputGroup]]

        self.profile = None

        self.db = None

        self.results = None

        self.presentable_results = None

        self.set_inputs([
            Input({
                'label': 'Run brute force aswell',
                'key': 'run_brute_force',
                "is_user_input": True,
                "required": False,
                'type': InputType.Checkbutton,
                'value': True,
            }),
            InputGroup({
                'label': "Exploration Space",
                'subtitle': (
                    "Define the limitations for core heterogeneity."
                    + " The platforms produced by the automatic DSE will often contain two different core models."
                    + " You are able to restrict the number of cores used of both models."
                ),
                'key': 'exploration_space',
                'inputs': [
                    Input({
                        'label': 'Minimal number of cores from the original model',
                        'key': 'original_cores_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                    Input({
                        'label': 'Number of cores that may be from another model',
                        'key': 'ip_cores_for_design',
                        "is_user_input": True,
                        "required": True,
                        'type': InputType.IntegerRange,
                        'min_val': 1,
                        'max_val': 31,
                    }),
                ],
            }),
            InputGroup({
                'label': "Constraints",
                'key': 'constraints',
                'inputs': [
                    Input({
                        'label': 'Maximum Power Density',
                        'unit': 'V/mm²',
                        'key': 'maximum_power_density',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Maximum Area',
                        'unit': 'mm²',
                        'key': 'maximum_area',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                    }),
                    Input({
                        'label': 'Technology',
                        'key': 'technology',
                        'allowed_values': Technologies.get_dict(),
                        "is_user_input": False,
                        "required": False,
                    }),
                ],
            }),
            InputGroup({
                'label': "NSGA-II Parameters",
                'key': 'nsga_parameters',
                'inputs': [
                    Input({
                        'label': 'Crossing Rate',
                        'unit': '%',
                        'key': 'mutation_strength',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 50.0,
                    }),
                    Input({
                        'label': 'Mutation Rate',
                        'unit': '%',
                        'key': 'mutation_rate',
                        'type': InputType.Float,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 10.0,
                    }),
                    Input({
                        'label': 'Population Size',
                        'key': 'num_of_individuals',
                        'type': InputType.Integer,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 10
                    }),
                    Input({
                        'label': 'Number of Generations',
                        'key': 'num_of_generations',
                        'type': InputType.Integer,
                        "is_user_input": True,
                        "required": True,
                        "default_value": 150
                    }),
                ],
            }),
        ])

        self.dse_engine = None

        self.brute_force = None  # type: Optional[DsDseBruteForce]

    def execute(self):
        self.prepare()

        self.dse_engine.run()

        self.register_results()

        if self.inputs['run_brute_force'].value is True:
            self.brute_force.run()

            self.register_brute_force_results()

    def register_brute_force_results(self):
        if not self.brute_force:
            return

        self.presentable_results['brute_force_solutions'] = {}

        for solution in self.brute_force.viable_solutions:
            title = (
                str(solution['amount_orig_core'])
                + "x " + solution["orig_processor"]
                + " & " + str(solution['amount_ip_core'])
                + "x " + solution['ip_core']['id']
            )

            self.presentable_results['brute_force_solutions'][title] = {
                'title': title,
                'nbr_ip_cores': solution["amount_ip_core"],
                'nbr_orig_cores': solution["amount_orig_core"],
                'ip_core': solution["ip_core"]["id"],
                'orig_core': solution["orig_processor"],
                'total_nbr_cores': solution["amount_ip_core"] + solution["amount_orig_core"],
                'total_area': round(solution["area"], 2),
                'performance': round(solution["performance_pred"], 2),
                'power_density': round(solution["power_density"], 2)
            }

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

        if self.inputs['run_brute_force'].value is True:
            self.brute_force = DsDseBruteForce(settings)

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
