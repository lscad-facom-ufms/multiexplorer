import json
import re
import sys
import os
import math
from pprint import pprint
from copy import deepcopy
from collections import Counter


def memoryModel(dictList, cores):
    ARRAY_ATTR = ['cache_size', 'associativity', 'data_access_time', 'tags_access_time', 'writethrough', 'writeback_time', 'next_level_read_bandwidth']
    # print 'Memory Model'
    MEMORY_TEMPLATE = {"perfect": [],
                       "passthrough": [],
                       "cache_block_size": [],
                       "cache_size": [],
                       "associativity": [],
                       "ports": [],
                       "address_hash": [],
                       "replacement_policy": [],
                       "data_access_time": [],
                       "tags_access_time": [],
                       "perf_model_type": [],
                       "writethrough": [],
                       "writeback_time": [],
                       "dvfs_domain": [],
                       "shared_cores": [],
                       "prefetcher": [],
                       "next_level_read_bandwidth": []}
    newMemory = deepcopy(MEMORY_TEMPLATE)
    # Putting all values together, in the same attribute
    for m in newMemory:
        for d in dictList:
            if m == 'shared_cores':
                newMemory[m] = (cores / len(dictList))
            else:
                newMemory[m].append(d[m])
    # Keep the higher average value for non-array attributes
    for m in newMemory:
        if not m in ARRAY_ATTR and type(newMemory[m]) == list:
            # Count occurences of each value and get the higher
            newMemory[m] = sorted(Counter(newMemory[m]),
                                  key=Counter(newMemory[m]).get)[0]

    # print "NewMemory",newMemory
    return newMemory


def prepareMemory(memoryDictionary, cores):

    # Treating Cache Memory
    newMemDict = {}
    sortedMem = {}
    cacheLevel = memoryDictionary['cache']['levels']
    # pprint(memoryDictionary)
    for i in xrange(1, cacheLevel + 1):
        if i == 1:
            sortedMem["l" + str(i) + "_dcache"] = []
            sortedMem["l" + str(i) + "_icache"] = []
        else:
            sortedMem["l" + str(i) + "_cache"] = []

        for mem in memoryDictionary.keys():
            matchTest = re.match(r"l" + str(i) + "_(d|i)?cache-", mem)
            if matchTest:
                if matchTest.group(1) == 'd':
                    sortedMem[
                        "l" + str(i) + "_dcache"].append(memoryDictionary[mem])
                elif matchTest.group(1) == 'i':
                    sortedMem[
                        "l" + str(i) + "_icache"].append(memoryDictionary[mem])
                else:
                    sortedMem[
                        "l" + str(i) + "_cache"].append(memoryDictionary[mem])
                memoryDictionary.pop(mem, None)

                # print i, mem
                # sortedMem[i].append(memoryDictionary[mem])
    # pprint(sortedMem)
    for i in sortedMem:
        # print i, len(sortedMem[i])
        newMemDict[i] = memoryModel(sortedMem[i], cores)
    # pprint(newMemDict)

    # Treating Main MemoryMemory
    newMemDict['dram_directory'] = memoryDictionary['dram']['dram_directory']
    memoryDictionary['dram'].pop('dram_directory', None)
    newMemDict['dram'] = memoryDictionary['dram']
    memoryDictionary.pop('dram', None)

    # Complete with the not changed sections

    newMemDict.update(memoryDictionary)
    # pprint(newMemDict)

    return newMemDict
