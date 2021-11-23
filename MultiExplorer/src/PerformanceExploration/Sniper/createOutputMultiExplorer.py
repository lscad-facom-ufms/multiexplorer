#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, re, sys , os, math

PATH_IN= os.path.dirname(os.path.realpath(__file__))
PATH_OUT_SNIPER=os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../support/sniper/tools')
import sniper_lib

#open PerformanceMap.json
performanceMap= json.loads(open(os.path.dirname(os.path.realpath(__file__)) + "/PerformanceMap.json").read())

physicalParameters=["number_of_cores","number_of_L1Directories","number_of_L2Directories","number_of_L2s", "Private_L2", "Private_L3",
"number_of_L3s", "number_of_NoCs","homogeneous_cores", "homogeneous_L2s", "homogeneous_L1Directories",  "homogeneous_L2Directories",  "homogeneous_L3s",  
"homogeneous_ccs",  "homogeneous_NoCs",  "core_tech_node","target_core_clockrate", "temperature", "number_cache_levels","interconnect_projection_type", 
"device_type", "longer_channel_device", "power_gating", "machine_bits", "virtual_address_width", "physical_address_width", "virtual_memory_page_size",

"clock_rate", "vdd","opt_local",  "opcode_width", "machine_type",  "number_hardware_threads","fetch_width","number_instruction_fetch_ports", 
"decode_width","x86", "micro_opcode_width", "issue_width","peak_issue_width", "commit_width","fp_issue_width", "prediction_width", 
"pipelines_per_core","pipeline_depth","ALU_per_core", "MUL_per_core", "FPU_per_core", "instruction_buffer_size", "decoded_stream_buffer_size", 
"instruction_window_scheme", "instruction_window_size", "fp_instruction_window_size", "ROB_size","archi_Regs_IRF_size", "archi_Regs_FRF_size", 
"phy_Regs_IRF_size", "phy_Regs_FRF_size", "rename_scheme", "register_windows_size", "LSU_order", "store_buffer_size", "load_buffer_size", 
"memory_ports", "RAS_size", "number_of_BPT","number_entries","icache_config","buffer_sizes","dcache_config","BTB_config",

"L2_config","clockrate","vdd","ports","device_type","L3_config","type", "horizontal_nodes","vertical_nodes", "has_global_link","link_throughput",
"link_latency","input_ports","output_ports","flit_bits","chip_coverage","link_routing_over_percentage",

"mc_clock","peak_transfer_rate","block_size","number_mcs","memory_channels_per_mc","number_ranks","withPHY","req_window_size_per_channel",
"IO_buffer_size_per_channel","databus_width","addressbus_width","number_units","number_flashcs"
]
default= {
        "number_of_L1Directories":"0",
        "number_of_L2Directories":"0",
        "number_of_NoCs":"1",
        "homogeneous_cores":"0",
        "homogeneous_L2s":"0",
        "homogeneous_L1Directories":"0", 
        "homogeneous_L2Directories":"0", 
        "homogeneous_L3s":"0",
        "homogeneous_ccs":"1", 
        "homogeneous_NoCs":"1", 
        "temperature":"370",
        "interconnect_projection_type":"0",
        "device_type":"0",
        "longer_channel_device":"1",
        "power_gating":"1",
        "machine_bits":"64",
        "virtual_address_width":"64",
        "physical_address_width":"52",
        "virtual_memory_page_size":"4096",


        "instruction_length":"64",
        "fp_rename_reads":"0",
        "fp_rename_writes":"0",
        "function_calls":"0",
        "context_switches":"0",
        "LSU_duty_cycle":"0",
        "MemManU_D_duty_cycle":"0",
        "ALU_duty_cycle":"1",
        "MUL_duty_cycle":"0.3",
        "FPU_duty_cycle":"0.3",
        "ALU_cdb_duty_cycle":"1",
        "MUL_cdb_duty_cycle":"0.3",
        "FPU_cdb_duty_cycle":"0.3",

	    
        "opt_local": "1", 
        "opcode_width": "16",
        "machine_type": "0", 
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
        "instruction_window_scheme": "0",
        "instruction_window_size": "64",
        "fp_instruction_window_size": "0",
        "archi_Regs_IRF_size": "16",
        "archi_Regs_FRF_size": "32",
        "phy_Regs_IRF_size": "256",
        "phy_Regs_FRF_size": "256",
        "rename_scheme": "0",
        "register_windows_size": "0",
        "LSU_order": "inorder",
        "store_buffer_size": "96",
        "load_buffer_size": "48",
        "memory_ports": "1",
        "RAS_size": "64",
        "number_of_BPT": "2",

        "conflicts":"0",
        "buffer_sizes": "16, 16, 16, 16",
        "BTB_config": "4096,4,2,1, 1,3",
        "duty_cycle":"0",
        "ports":"1,1,1",
        "device_type":"0",

        "horizontal_nodes":"1",
        "vertical_nodes":"1",
        "has_global_link":"0",
        "link_throughput":"1",
        "link_latency":"1",
        "input_ports":"1",
        "output_ports":"1",
        "flit_bits":"256",
        "chip_coverage":"1",
        "link_routing_over_percentage":"0.5",

        "mc_clock": "200",
        "peak_transfer_rate": "3200",
        "block_size": "64",
        "number_mcs": "0",
        "memory_channels_per_mc": "1",
        "number_ranks": "2",
        "withPHY": "0",
        "req_window_size_per_channel": "32",
        "IO_buffer_size_per_channel": "32",
        "databus_width": "128",
        "addressbus_width": "51",

        "number_units":"0",

        "number_flashcs":"0"

}
def get_number_of_caches(level):
    if config.has_key("perf_model/l%s_cache/shared_cores"%level):
        if int(config["perf_model/l%s_cache/shared_cores"%level])==1:
            #amount of caches is same of total_cores
            #print "aqui q ta o erro, cache level %s , ta gerando %s caches"%(level,int(config["general/total_cores"]))
            number_caches= int(config["general/total_cores"])
            return int(number_caches)
        else:
            return 1
    return 0
def outputConvert():
    global obj_result
    global results
    global config
    global total_cores
    obj_result = sniper_lib.get_results(resultsdir = os.getcwd())
    #extract performanceResults
    results= obj_result["results"]
    #extract descriptionProcessor
    config= obj_result["config"]

    total_cores= config["general/total_cores"]

    dictOut={}

    def stageDict(dictOut):
        list_parameters=[]
        for region in dictOut:
            if region != 'system':
                list_parameters.append(region)
                dictOut["system"][region]= dictOut[region]
        
        #it throught the list for removing de keys of dictionary
        for region in list_parameters:
            del dictOut[region]

    

    for region in performanceMap:
        #core
        if region.find("system.core")!=-1:
            for indCore in range(0, int(total_cores)):
                newRegion= re.sub('\$', str(indCore), region)

                dictOut[newRegion]={}

                for paramName in performanceMap[region]:
                    #case is a parameter of type system.core$...
                    if paramName.find("system")!=-1:
                        newParamName=re.sub("\$", str(indCore), paramName)
                        dictOut[newRegion][newParamName]={}
                        
                        for subParam in performanceMap[region][paramName]:
                            if subParam in physicalParameters:
                                inserct(performanceMap[region][paramName], dictOut[newRegion][newParamName], subParam, config, indCore)
                            else:
                                inserct(performanceMap[region][paramName], dictOut[newRegion][newParamName], subParam, results, indCore)                                  
                    
                    else:
                        if performanceMap[region][paramName]=="thread.instructions_by_core[$]":
                            ParamList= re.findall("[a-zA-Z_|.|-]+", performanceMap[region][paramName])
                            dictOut[newRegion][paramName]= results[ParamList[0]+'['+str(indCore)+']'][indCore]
                        else:
                            if paramName in physicalParameters:
                                inserct(performanceMap[region], dictOut[newRegion], paramName, config, indCore)
                            else:
                                inserct(performanceMap[region], dictOut[newRegion], paramName, results, indCore)

        #cache l2 
        elif region.find("system.L2$")!=-1:
            levels=int(config["perf_model/cache/levels"])
            if levels>3:
                print "McPAT supports up to 3 caches levels"
                break
            if levels>=2:
                number_cache= get_number_of_caches(2)
                for n in range(0, number_cache):
                    newRegion='system.L2%s'%n
                    dictOut[newRegion]={}

                    for paramName in performanceMap[region]:
                        if paramName in physicalParameters:
                            inserct(performanceMap[region], dictOut[newRegion], paramName, config, n)
                        else:
                            inserct(performanceMap[region], dictOut[newRegion], paramName, results, n)
                        
        #cache l3
        elif region.find("system.L3$")!=-1:
            levels=int(config["perf_model/cache/levels"])
            if levels>3:
                print "McPAT supports up to 3 caches levels"
                break
            if levels==3:
                number_cache= get_number_of_caches(3)
                for n in range(0, number_cache):
                    newRegion='system.L3%s'%n
                    dictOut[newRegion]={}

                    for paramName in performanceMap[region]:
                        if paramName in physicalParameters:
                            inserct(performanceMap[region], dictOut[newRegion], paramName, config, n) 
                        else:
                            inserct(performanceMap[region], dictOut[newRegion], paramName, results, n)

        #anothers
        else:
            dictOut[region]={}
            for paramName in performanceMap[region]:
                #checking if is a physicalParameters or stat
                if paramName in physicalParameters:
                    inserct(performanceMap[region], dictOut[region], paramName, config)
                else:
                    inserct(performanceMap[region], dictOut[region], paramName, results)

    stageDict(dictOut)     
 
    return writerJsonFile(dictOut)        
            
    

def inserct(dictMap, dictAux, paramName, attribute, indCore=-1):
    #if is in default dictionary
    if default.has_key(paramName):
        dictAux[paramName]= default[paramName]
        
    #if is a parameter of cache's configurations
    elif re.search('_config', paramName)!=None:
        valueString=""
        for element in dictMap[paramName]:
            if re.match('\w+(/\w)+',element)!=None:
                if re.search('cache_size', element)!=None:
                    if isinstance(attribute[element], dict):
                        #checking, if it is key 'indCore'
                        if attribute[element].has_key(indCore):
                            valueString+=str(int(attribute[element][indCore])*1024)
                        #except, get the firs key of dict
                        else:
                            valueString+=str(int(attribute[element][0])*1024)
                    #if don't is a dict
                    else:
                        valueString+=str(int(attribute[element])*1024)
                # case, is cache_block_size, associativity, data_access_time
                else:
                    if isinstance(attribute[element], dict):
                        #checking, if it is key 'indCore'
                        if attribute[element].has_key(indCore):
                            valueString+=","+str(int(attribute[element][indCore]))
                        #except, get the firs key of dict
                        else:
                             valueString+=","+str(int(attribute[element][0]))
                    #if don't is a dict
                    else:
                        valueString+=","+attribute[element]
                    
            else:
                valueString+=",%s"%element

        dictAux[paramName]=valueString

    #if is as "identifier":"0"
    elif dictMap[paramName]=="0":
        dictAux[paramName]=0
    
    #if is as "identifier":""
    elif dictMap[paramName]=="":
        #cheking if is a parameter of L2 
        if paramName=="number_of_L2s":
            dictAux[paramName]= str(get_number_of_caches(2))
        if paramName=="number_of_L3s":
            dictAux[paramName]= str(get_number_of_caches(3))

    #if have a +...+
    elif dictMap[paramName].find("+...+")!=-1:
        parameter= dictMap[paramName].split("+...+")[0]
        
        sum=0
        #atribute, may be a config dictionary or results
        for x in attribute[parameter]:
            sum=sum+x
        
        dictAux[paramName]= sum
    
    #find a " - "
    elif dictMap[paramName].find(" - ")!=-1:
        listInd= re.findall("[\d+]",dictMap[paramName])
        listParam= re.findall("[a-zA-Z_|.|-]+", dictMap[paramName])
        
        if len(listInd)!=0:
            ind1= int(listInd[0])
            ind2= int(listInd[1])
            dictAux[paramName]=  abs(attribute[listParam[0]][ind1] -  attribute[listParam[2]][ind2])
        else:
            ind1= indCore
            ind2= indCore
            dictAux[paramName]=  abs(attribute[listParam[0]][indCore] - attribute[listParam[2]][indCore])

    
    #if paramName is Private_L\d
    elif re.match("Private_L\d", paramName)!=None:
        if attribute[dictMap[paramName]]==1:
            dictAux[paramName]=1
        else:
            dictAux[paramName]=0
    
    #case, when it get a greater clock
    elif paramName == "target_core_clockrate" or paramName == "clockrate" or paramName == "clock_rate":
        if isinstance(attribute[dictMap[paramName]], dict):
            dictionary=attribute[dictMap[paramName]]
            key=max(dictionary, key=dictionary.get)

            dictAux[paramName]=int(float(dictionary[key])*1000) #Ghz to Mhz
        else:
            dictAux[paramName]=int(float(attribute[dictMap[paramName]])*1000) #Ghz to Mhz
    
    # if is identifier/identifier/...                       
    elif re.match('\w+(/\w)+',dictMap[paramName])!=None:

        if not attribute.has_key(dictMap[paramName]):
            dictAux[paramName]= '10'#default

        elif isinstance(attribute[dictMap[paramName]], dict):
            dictionary= attribute[dictMap[paramName]]
            
            if dictionary.has_key(indCore):
                if paramName=='clock_rate':
                    dictAux[paramName]=int(float(dictionary[indCore])*1000)
                else:
                    dictAux[paramName]=dictionary[indCore]
            else:
                dictAux[paramName]='4' #default

        else:         
            dictAux[paramName]=attribute[dictMap[paramName]]
    
    #if is a pattern, as "number_cores*thread.instruction_count[$]"
    elif dictMap[paramName].find("*")!=-1:
        
        str1= dictMap[paramName].split('*')[1]
        listInd= re.findall("[\d+]",dictMap[paramName])
        listParam= re.findall("[a-zA-Z_|.|-]+", str1)
        
        if len(listInd)!=0:
            ind= int(listInd[0])
            dictAux[paramName]= int(total_cores)*attribute[listParam[0]][ind]
        else:
            dictAux[paramName]= int(total_cores)*attribute[listParam[0]][indCore]
    #if is a pattern, as * (divided) *
    elif dictMap[paramName].find("(divided)")!=-1:
        str1= dictMap[paramName].split("(divided)")[0]
        listInd= re.findall("[\d+]",dictMap[paramName])
        listParam= re.findall("[a-zA-Z_|.|-]+", str1)

        if len(listInd)!=0:
            ind= int(listInd[0])
            dictAux[paramName]= attribute[listParam[0]][ind]/int(total_cores)
        else:
            dictAux[paramName]= attribute[listParam[0]][indCore]/int(total_cores)
    
        
    # if is a pattern "identifier[\d+]"
    else:
        #listInd= re.findall("[\d+]",dictMap[paramName])
        listParam= re.findall("[a-zA-Z0-9_|.|-]+", dictMap[paramName])
        #if len(listInd)!=0:
            #ind= int(listInd[0])
        dictAux[paramName]= attribute[listParam[0]][indCore]
        #else:
            #dictAux[paramName]= attribute[listParam[0]][indCore]        

def writerJsonFile(dictOut):
    strJson= json.dumps(dictOut, indent= 4, sort_keys=True)
    outFile= open(os.getcwd() + '/out.json', 'w')
    outFile.write(strJson)
    # print strJson
    return os.getcwd() + '/out.json'


    

if __name__=="__main__":
    outputConvert()

    
