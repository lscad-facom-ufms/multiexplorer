MultiExplorer Tool - version 1.0
===================
Muliexplorer is a framework that provides a processor chip design by putting together performance simulation, physical estimation, and 
design space exploration steps. MultiExplorer uses Sniper and GPGPU-sim as the performance simulator and McPAT as the physical estimator. The design space exploration (DSE) is performed by a NSGA2-based algorithm. In this current version, Muliexplorer also adopts a brute-force (bf) algorithm to explore all viable alternatives to the design. The bf has been used as a validation step to our DSE approach. Multiexplorer assumes that all processor designs are dar silicon aware so that it uses the power density as a constraint in the DSE step.To know more about Multiexplorer and its Dark-Silicon aware - DSE approach please refers to our paper:

SANTOS, R.;DUENHA, L.; SILVA, A. C. S.; BIGNARDI, T.; SOUSA, M.; TEDESCO, L.; MELGAREJO JUNIOR, J.; AZEVEDO, R.; ORDONEZ, E. D. M.. 
Dark-Silicon Aware Design Space Exploration. JOURNAL OF PARALLEL AND DISTRIBUTED COMPUTING, v. 120, 2018, pp 295-306, ISSN 0743-7315.


Dependencies
============
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

If you want to install Multiexplorer source codes in your host machine without a VM. Be sure to have all these softwares:
- [Sniper](http://snipersim.org)
- [McPAT](http://www.hpl.hp.com/research/mcpat/)
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [lxml](http://lxml.de/)
- [gpgpu-sim](https://github.com/gpgpu-sim/gpgpu-sim_distribution)


How to Install ?
================
This is a Multiexplorer-VM package based on Ubuntu 14 ready to use Multiexplorer. All dependencies, benchmarks suites, and input examples are available from the ds-repo folder. 


Run your first simulation
=========================
After installing the multiexplorer and  gpgpu-sim, open the terminal window and type:

$ cd multiexplorer

There are many input examples available in the input-examples folder. You should run one of the .json files in that folder. For example:

$ python MultiExplorer/src/MultiExplorer.py input-examples/gtx480.json

Just wait the simulation steps finish. All the output files will be in the rundir folder. Note that Multiexplorer will create a folder 
for your design and simulation,in the rundir folder, following the order: JSONInput_Application-Date_Time. 
Example: GTX480_clock-2022-05-28-41-17:38:41-11930


<!-- Output files
=========================
These files will be in the rundir folder after running Multiexplorer:
         

MCPATPhysicalResults.txt: McPAT physical estimates (area, power, etc.) of the original design.
               
outputBruteForce.csv: a csv file with all the configurations obtained from our BF DS-DSE algorithm.
      
BFSOutput.txt: outputs of the performance simulator. 

BFSstderr.txt: the performance simulator error.     

populationResults.csv: a csv file with all the configurations from our NSGA2-based DS-DSE algorithm.

SniperPerformanceResults.txt: log file of the performance simulator

SniperSimQuarkCholesky_mcpatInput.xml: input file for the Physical estimator (McPAT).

**May there are other files that are reserved for future use in Multiexplorer. -->


Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com
