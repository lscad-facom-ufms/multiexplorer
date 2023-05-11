import json
import os, subprocess, signal
import sys
import re
import ast
import imp
from copy import deepcopy
import shutil

try:
    imp.find_module('configparser')
    from configparser import ConfigParser as iniParser
except ImportError:
    print "The configparser library is not installed."
    print "Try $ pip install configparser to install"
    exit()


# Import from any relative path
importPath = os.path.dirname(os.path.realpath(__file__)) + '/../SimulationTool'
sys.path.insert(0, importPath)

from SimulationTool import SimulationTool


class MPSoCBench(SimulationTool):

    """docstring for MPSoCBench"""
    destfile= None
    def __init__(self, jsonFile, paramMap, outJson):
        super(MPSoCBench, self).__init__(jsonFile, paramMap, outJson)
        self.resultInput = {'proc': "", 'mem': ""}
        # Opens the jSON file with all parameters to map the input
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + paramMap) as data_file:
            self.paramMap = json.load(data_file)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + outJson) as data_file:
            self.outJson = json.load(data_file)
        self.outputJson = None

        

    # Translate the MultiExplorer input as a set of m2s files.
    def parse(self):


        print "===== PARSING ======"

        # Opens the jSON file and stores it as a dict
        with open(self.jsonFile) as data_file:
            self.data = json.load(data_file)

        ###Gets some of the information needed to run ###
        # Input Configuration for the processor
        processorConfig = self.data['General_Modeling']
        
        teste= self.data['Preferences']['processor']
        self.sim_tool_path= self.data['Preferences']['sim_tool_path']
        
        # Number of Cores <n>
        self.numberOfCores = int(self.data['General_Modeling']['total_cores'])
        
        p= self.sim_tool_path
        files= { p+'/processors/arm/arm_nonblock.ac',
                 p+'/processors/powerpc/powerpc_nonblock.ac',
                 p+'/processors/sparc/sparc_nonblock.ac',
                 p+'/processors/mips/mips_nonblock.ac',
                 p+'/processors/arm/arm_block.ac',
                 p+'/processors/powerpc/powerpc_block.ac',
                 p+'/processors/sparc/sparc_block.ac',
                 p+'/processors/mips/mips_block.ac'
               }

        memI= self.data['General_Modeling']['memory']['l1_icache-0']
        memD= self.data['General_Modeling']['memory']['l1_dcache-0']
        vars= {'associativity_ic': memI['associativity'],
               'number_of_blocks_ic': str(int(memI['cache_size'])/int(memI['cache_block_size'])),
               'block_size_ic': memI['cache_block_size'],
               'writing_policy_ic': 'wt',
               'replacement_policy_ic': memI['replacement_policy'],

               'associativity_dc': memD['associativity'],
               'number_of_blocks_dc': str(int(memD['cache_size'])/int(memD['cache_block_size'])),
               'block_size_dc': memD['cache_block_size'],
               'writing_policy_dc': 'wt',
               'replacement_policy_dc': memD['replacement_policy'],
              }
        if (vars['associativity_ic']=='1'):
            vars['associativity_ic']= 'dm'

        if (vars['associativity_dc']=='1'):
            vars['associativity_dc']= 'dm'
        
        for f in files:
            self.replaceByTemplate(vars, f+".template", f)
        
        
        pass

    def replaceByTemplate(self, vars, template, fileOut):
        with open(template, "rt") as fin:
            with open(fileOut, "wt") as fout:
                for line in fin:
                    for key in vars:
                        line= line.replace('{{'+key+'}}', str(vars[key]))
                    fout.write(line)
        pass

    def execute(self, configs=None):

        exports = "export PATH=/home/gpgpu-sim/MPSoCBench/compilers/mips-newlib-elf/bin:$PATH && \
export PATH=/home/gpgpu-sim/MPSoCBench/compilers/arm-newlib-eabi/bin:$PATH && \
export PATH=/home/gpgpu-sim/MPSoCBench/compilers/powerpc-newlib-elf/bin:$PATH && \
export PATH=/home/gpgpu-sim/MPSoCBench/compilers/sparc-newlib-elf/bin:$PATH"

        #exports = "export PATH=/home/gpgpu-sim/MPSoCBench-2.2/tools/compilers/mips-newlib-elf/bin:$PATH && \
#export PATH=/home/gpgpu-sim/MPSoCBench-2.2/tools/compilers/arm-newlib-eabi/bin:$PATH && \
#export PATH=/home/gpgpu-sim/MPSoCBench-2.2/tools/compilers/powerpc-newlib-elf/bin:$PATH && \
#export PATH=/home/gpgpu-sim/MPSoCBench-2.2/tools/compilers/sparc-newlib-elf/bin:$PATH"


        commandLine= "cd "+self.sim_tool_path+"/ && " + exports +" && ./MPSoCBench"
        commandLine+= " -n=" + str(self.data['General_Modeling']['total_cores'])
        commandLine+= " -p=" + self.data['Preferences']['processor']
        commandLine+= " -s=" + self.data['Preferences']['application']
        commandLine+= " -i=" + self.data['Preferences']['interconnection']        

        self.resultMpsoc= self.sim_tool_path+'/rundir/'+self.data['Preferences']['processor']+'.'+self.data['Preferences']['interconnection']+'.'+str(self.data['General_Modeling']['total_cores'])+'.'+self.data['Preferences']['application']+'/output.json'

        print "RESULT OF MPSOCBENCH WILL STORED IN"+self.resultMpsoc
        
        #outname = "Resultado_" + self.inputName.replace('Input_', "")
        #commandLine += " --x86-config " + os.getcwd() + '/' + self.inputName + ".ini"
        
        print(commandLine)

        #subprocess.check_output(commandLine + " -b", shell=True).decode("UTF-8") 
        #subprocess.call(commandLine+ ' -r', shell=True)

        

        os.system(commandLine+ ' -b')

        #print ret 
        os.system(commandLine+ ' -r')

        #self.outputNamePath = {outname: os.getcwd() + '/' + outname, outname + "_cmdOutput.txt": os.getcwd(
        #) + '/' + outname + "_cmdOutput.txt", outname + "_mem": os.getcwd() + '/' + outname + "_mem"}
        
        pass
    
    def convertResults(self):
        print "===== CONVERTING RESULTS ======"
        ##############################################
        #        START convertResults Function       #
        ##############################################

        # Load config files
        with open(self.jsonFile) as data_file:
            inputJson = json.load(data_file)


        srcfile = os.path.dirname(os.path.realpath(__file__))+'/performanceMips.json'
        self.destfile = os.path.dirname(os.path.realpath(__file__))+'/result.json'


        #shutil.copy(srcfile, self.destfile)


        with open(srcfile) as data_file:
            outJson = json.load(data_file)

        with open(self.resultMpsoc) as data_file:
            mpsoc = json.load(data_file)
            
        #TODO obter essa informacao
        outJson['system']['number_of_cores']= str(inputJson['General_Modeling']['total_cores'])
        outJson['system']['target_core_clockrate']= str(inputJson['General_Modeling']['core']['global_frequency'])
        
        archBits='32'

        totalAll= 0
        for ii in range(0,inputJson['General_Modeling']['total_cores']):
            i= str(ii)
            # gerar esse dado no mpsocbench
            total= int(mpsoc['processors'][ii]['instruction']['basic_alu'])+int(mpsoc['processors'][ii]['instruction']['br'])+int(mpsoc['processors'][ii]['instruction']['j'])+int(mpsoc['processors'][ii]['instruction']['ld'])+int(mpsoc['processors'][ii]['instruction']['mul'])+int(mpsoc['processors'][ii]['instruction']['st'])
            totalAll= totalAll + total

            outJson['system']['system.core'+i]= {}
            outJson['system']['system.core'+i]['id']=i;
            outJson['system']['system.core'+i]['total_instructions']= str(total)
            outJson['system']['system.core'+i]['int_instructions']= mpsoc['processors'][ii]['instruction']['basic_alu']
            outJson['system']['system.core'+i]['fp_instructions']= '0'
            outJson['system']['system.core'+i]['branch_instructions']= mpsoc['processors'][ii]['instruction']['br']
            outJson['system']['system.core'+i]['branch_mispredictions']= '0'
            outJson['system']['system.core'+i]['load_instructions']= mpsoc['processors'][ii]['instruction']['ld']
            outJson['system']['system.core'+i]['store_instructions']= mpsoc['processors'][ii]['instruction']['st']
            outJson['system']['system.core'+i]['committed_instructions']= outJson['system']['system.core'+i]['total_instructions']
            outJson['system']['system.core'+i]['committed_int_instructions']= mpsoc['processors'][ii]['instruction']['basic_alu']
            outJson['system']['system.core'+i]['committed_fp_instructions']= '0'
            outJson['system']['system.core'+i]['vdd']=inputJson['General_Modeling']['power']['vdd']
            

            #TODO obter essa informacao
            outJson['system']['system.core'+i]['total_cycles']= outJson['system']['system.core'+i]['total_instructions']
            outJson['system']['system.core'+i]['idle_cycles']= outJson['system']['system.core'+i]['total_instructions']
            outJson['system']['system.core'+i]['busy_cycles']= outJson['system']['system.core'+i]['total_instructions']
            outJson['system']['system.core'+i]['ROB_reads']= '0'
            outJson['system']['system.core'+i]['ROB_writes']= '0'
            outJson['system']['system.core'+i]['rename_reads']= '0'
            outJson['system']['system.core'+i]['rename_writes']= '0'
            outJson['system']['system.core'+i]['fp_rename_reads']= '0'
            outJson['system']['system.core'+i]['fp_rename_writes']= '0'
            outJson['system']['system.core'+i]['inst_window_reads']= '0'
            outJson['system']['system.core'+i]['inst_window_writes']= '0'

            #verificar essas informacoes
            outJson['system']['system.core'+i]['int_regfile_reads']= str(int(mpsoc['processors'][ii]['instruction']['basic_alu'])*2)
            outJson['system']['system.core'+i]['float_regfile_reads']= '0'
            outJson['system']['system.core'+i]['int_regfile_writes']= mpsoc['processors'][ii]['instruction']['basic_alu']
            outJson['system']['system.core'+i]['float_regfile_writes']= '0'
            outJson['system']['system.core'+i]['function_calls']= '0'
            outJson['system']['system.core'+i]['context_switches']= '0'
            outJson['system']['system.core'+i]['ialu_accesses']= mpsoc['processors'][ii]['instruction']['basic_alu']
            outJson['system']['system.core'+i]['fpu_accesses']= '0'
            outJson['system']['system.core'+i]['mul_accesses']= mpsoc['processors'][ii]['instruction']['mul']

            outJson['system']['system.core'+i]['clock_rate']= str(inputJson['General_Modeling']['core']['global_frequency'])
            outJson['system']['system.core'+i]['number_hardware_threads']= '1'

            #TODO todo esse bloco
            outJson['system']['system.core'+i]['decode_width']= '10'
            outJson['system']['system.core'+i]['issue_width']='4'
            outJson['system']['system.core'+i]['commit_width']= '10'
            outJson['system']['system.core'+i]['ROB_size']= '128'
            outJson['system']['system.core'+i]['RAS_size']= '64'


            #Default values
            outJson['system']['system.core'+i]['inst_window_wakeup_accesses']= '0'
            outJson['system']['system.core'+i]['fp_inst_window_reads']= '0'
            outJson['system']['system.core'+i]['fp_inst_window_writes']= '0'
            outJson['system']['system.core'+i]['fp_inst_window_wakeup_accesses']= '0'

            outJson['system']['system.core'+i]['cdb_alu_accesses']= '0'
            outJson['system']['system.core'+i]['cdb_mul_accesses']= '0'
            outJson['system']['system.core'+i]['cdb_fpu_accesses']= '0'

            outJson['system']['system.core'+i]['opt_local']= '1'
            outJson['system']['system.core'+i]['instruction_length']= archBits
            outJson['system']['system.core'+i]['opcode_width']= '16'
            outJson['system']['system.core'+i]['machine_type']= '0'
            outJson['system']['system.core'+i]['fetch_width']= '10'
            outJson['system']['system.core'+i]['number_instruction_fetch_ports']= '1'

            #TODO o valor x86 estava em 1
            outJson['system']['system.core'+i]['x86']= '0'
            outJson['system']['system.core'+i]['micro_opcode_width']= '8'
            outJson['system']['system.core'+i]['peak_issue_width']= '6'
            outJson['system']['system.core'+i]['fp_issue_width']= '2'
            outJson['system']['system.core'+i]['prediction_width']= '1'
            outJson['system']['system.core'+i]['pipelines_per_core']= '1,1'
            outJson['system']['system.core'+i]['pipeline_depth']= '14,14'
            outJson['system']['system.core'+i]['ALU_per_core']= '4'
            outJson['system']['system.core'+i]['MUL_per_core']= '1'
            outJson['system']['system.core'+i]['FPU_per_core']= '1'
            outJson['system']['system.core'+i]['instruction_buffer_size']= '16'
            outJson['system']['system.core'+i]['decoded_stream_buffer_size']= '16'
            outJson['system']['system.core'+i]['instruction_window_scheme']= '1'
            outJson['system']['system.core'+i]['instruction_window_size']= archBits
            outJson['system']['system.core'+i]['fp_instruction_window_size']= '0'
            outJson['system']['system.core'+i]['archi_Regs_IRF_size']= '16'
            outJson['system']['system.core'+i]['archi_Regs_FRF_size']= '32'
            outJson['system']['system.core'+i]['phy_Regs_IRF_size']= '256'
            outJson['system']['system.core'+i]['phy_Regs_FRF_size']= '256'
            outJson['system']['system.core'+i]['rename_scheme']= '0'
            outJson['system']['system.core'+i]['register_windows_size']= '0'
            outJson['system']['system.core'+i]['LSU_order']= 'inorder'
            outJson['system']['system.core'+i]['store_buffer_size']= '96'
            outJson['system']['system.core'+i]['load_buffer_size']= '48'
            outJson['system']['system.core'+i]['memory_ports']= '1'
            outJson['system']['system.core'+i]['number_of_BPT']= '2'
            #End Default values

            # BTB - Branch target predictor
            outJson['system']['system.core'+i]['system.core'+i+'.BTB']= {}
            outJson['system']['system.core'+i]['system.core'+i+'.BTB']['read_accesses']= 0
            outJson['system']['system.core'+i]['system.core'+i+'.BTB']['write_accesses']= 0
            outJson['system']['system.core'+i]['system.core'+i+'.BTB']['BTB_config']= 0

            #"system.core$.BTB": {
            #    "read_accesses": " Core $ Thread 0 /BTB.Reads",
            #    "write_accesses": " Core $ Thread 0 /BTB.Writes",
            #    "BTB_config": "4096,8, Config.BranchPredictor /BTB.Assoc,1,1,3"
            #}


            # Dados de duty copiados do gerado pelo sniper
            IPC_core= 1
            outJson['system']['system.core'+i]['IFU_duty_cycle']= str(IPC_core)
            outJson['system']['system.core'+i]['LSU_duty_cycle']= '0'
            outJson['system']['system.core'+i]['MemManU_I_duty_cycle']= str(IPC_core)
            outJson['system']['system.core'+i]['MemManU_D_duty_cycle']= '0'
            outJson['system']['system.core'+i]['ALU_duty_cycle']= '1'
            outJson['system']['system.core'+i]['MUL_duty_cycle']= '0.3'
            outJson['system']['system.core'+i]['FPU_duty_cycle']= '0.3'
            outJson['system']['system.core'+i]['ALU_cdb_duty_cycle']= '1'
            outJson['system']['system.core'+i]['MUL_cdb_duty_cycle']= '0.3'
            outJson['system']['system.core'+i]['FPU_cdb_duty_cycle']= '0.3'




            # Cache IC
            outJson['system']['system.core'+i]['system.core'+i+'.icache']= {}
            outJson['system']['system.core'+i]['system.core'+i+'.icache']['read_accesses']=  str(mpsoc['processors'][ii]['cacheIC']['read_hit']+mpsoc['processors'][ii]['cacheIC']['read_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.icache']['read_misses']=  str(mpsoc['processors'][ii]['cacheIC']['read_miss'])

            outJson['system']['system.core'+i]['system.core'+i+'.itlb']= {}
            outJson['system']['system.core'+i]['system.core'+i+'.itlb']['conflicts']= str(mpsoc['processors'][ii]['cacheIC']['evictions'])
            outJson['system']['system.core'+i]['system.core'+i+'.itlb']['number_entries']= str(inputJson['General_Modeling']['memory']['itlb']['sets'])
            outJson['system']['system.core'+i]['system.core'+i+'.itlb']['total_accesses']= str(mpsoc['processors'][ii]['cacheIC']['read_hit']+mpsoc['processors'][ii]['cacheIC']['read_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.itlb']['total_misses']= str(mpsoc['processors'][ii]['cacheIC']['read_miss'])


            #TODO
            outJson['system']['system.core'+i]['system.core'+i+'.icache']['conflicts']= str(mpsoc['processors'][ii]['cacheIC']['evictions'])

            mem= inputJson['General_Modeling']['memory']['l1_icache-0']
            outJson['system']['system.core'+i]['system.core'+i+'.icache']['icache_config']= str(mem['cache_size']*1024)+','+str(mem['cache_block_size'])+','+str(mem['associativity'])+',1, 3,'+str(mem['data_access_time'])+',16,1'
            outJson['system']['system.core'+i]['system.core'+i+'.icache']['buffer_sizes']= '16,16,16,16'


             # Cache DC
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']= {}
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['read_accesses']=  str(mpsoc['processors'][ii]['cacheDC']['read_hit']+mpsoc['processors'][ii]['cacheDC']['read_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['read_misses']=  str(mpsoc['processors'][ii]['cacheDC']['read_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['write_accesses']=  str(mpsoc['processors'][ii]['cacheDC']['write_hit']+mpsoc['processors'][ii]['cacheDC']['write_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['write_misses']=  str(mpsoc['processors'][ii]['cacheDC']['write_miss'])

            outJson['system']['system.core'+i]['system.core'+i+'.dtlb']= {}
            outJson['system']['system.core'+i]['system.core'+i+'.dtlb']['conflicts']= str(mpsoc['processors'][ii]['cacheDC']['evictions'])
            outJson['system']['system.core'+i]['system.core'+i+'.dtlb']['number_entries']= str(inputJson['General_Modeling']['memory']['dtlb']['sets'])
            outJson['system']['system.core'+i]['system.core'+i+'.dtlb']['total_accesses']= str(mpsoc['processors'][ii]['cacheDC']['read_hit']+mpsoc['processors'][ii]['cacheDC']['read_miss']+mpsoc['processors'][ii]['cacheDC']['write_hit']+mpsoc['processors'][ii]['cacheDC']['write_miss'])
            outJson['system']['system.core'+i]['system.core'+i+'.dtlb']['total_misses']= str(mpsoc['processors'][ii]['cacheDC']['read_miss']+mpsoc['processors'][ii]['cacheDC']['write_miss'])


            #TODO
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['conflicts']= str(mpsoc['processors'][ii]['cacheDC']['evictions'])

            mem= inputJson['General_Modeling']['memory']['l1_dcache-0']


            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['dcache_config']= str(mem['cache_size']*1024)+','+str(mem['cache_block_size'])+','+str(mem['associativity'])+',1, 3,'+str(mem['data_access_time'])+',16,1'
            outJson['system']['system.core'+i]['system.core'+i+'.dcache']['buffer_sizes']= '16,16,16,16'

            #End Cache

            #End processor info

        #NOC

        outJson['system']['total_cycles']= str(totalAll)
        outJson['system']['busy_cycles']= str(totalAll)

        #TODO tmp
        outJson['system']['system.NoC0']['clockrate']= inputJson['General_Modeling']['core']['global_frequency']
        outJson['system']['system.NoC0']['vdd']= inputJson['General_Modeling']['power']['vdd']
        outJson['system']['system.mc']['memory_accesses']= str(mpsoc['memory']['memory_read']+mpsoc['memory']['memory_write'])
        outJson['system']['system.mc']['memory_reads']= str(mpsoc['memory']['memory_read'])
        outJson['system']['system.mc']['memory_writes']= str(mpsoc['memory']['memory_write'])



        
        
        #TODO
        outJson['system']['system.mc']['mc_clock']= '200'
        outJson['system']['system.mc']['peak_transfer_rate']= str(inputJson['General_Modeling']['core']['global_frequency'])
        outJson['system']['system.mc']['block_size']= str(inputJson['General_Modeling']['memory']['tlb']['block_size'])
        outJson['system']['system.mc']['number_mcs']= '2'
        outJson['system']['system.mc']['memory_channels_per_mc']= '1'
        
        outJson['system']['system.mc']['vdd']= inputJson['General_Modeling']['power']['vdd']


        outJson['system']['core_tech_node']=inputJson['General_Modeling']['power']['technology_node']
        outJson['system']['temperature']=inputJson['General_Modeling']['power']['temperature']

        outJson['system']['number_cache_levels']='1'

        outJson['system']['machine_bits']=archBits
        

        with open(self.destfile, 'w') as outfile:
            json.dump(outJson, outfile, indent=4, sort_keys=True)    

        print " =============== END convertResults Function ============= "
        ##############################################
        #        END convertResults Function         #
        ##############################################

    def writeResults(self):
        pass









    def getOutputJson(self):

        return self.destfile
        #return os.path.realpath(__file__) + "performanceMips.json"


  

if __name__ == "__main__":
    m = MPSoCBench(sys.argv[1], "paramMap.json", "PerformanceMap_new.json")
    m.parse()
    m.execute()
    m.convertResults()
