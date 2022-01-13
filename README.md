MultiExplorer Tool
===================
Muliexplorer is a framework that provides a processor chip design by putting together performance simulation, physical estimation, and 
design space exploration steps. MultiExplorer uses Sniper as the performance simulator and McPAT as the physical estimator. The design space exploration (DSE) is performed by a NSGA2-based algorithm. In this current version, Muliexplorer also adopts a brute-force (bf) algorithm to explore all viable alternatives to the design. The bf has been used as a validation step to our DSE approach. MultiExplorer assumes that all processor designs are dar silicon aware so that it uses the power density as a constraint in the DSE step.To know more about MultiExplorer and its Dark-Silicon aware - DSE approach please refers to our paper:

SANTOS, R.;DUENHA, L.; SILVA, A. C. S.; BIGNARDI, T.; SOUSA, M.; TEDESCO, L.; MELGAREJO JUNIOR, J.; AZEVEDO, R.; ORDONEZ, E. D. M.. 
Dark-Silicon Aware Design Space Exploration. JOURNAL OF PARALLEL AND DISTRIBUTED COMPUTING, v. 120, 2018, pp 295-306, ISSN 0743-7315.


Dependencies
============
To properly execute MultiExplorer, be sure to have all these softwares:
- [gcc multilib](https://howtoinstall.co/pt/gcc-multilib) (required to compile Sniper)
- [g++ multilib](https://howtoinstall.co/pt/g++-multilib) (required to compile Sniper)
- [Sniper 7.4](http://snipersim.org)
  - [Sniper's Benchmarks](https://snipersim.org/w/Download_Benchmarks) 
- [Python 2.7](https://www.python.org/download/releases/2.7/)
  - [lxml](https://lxml.de/installation.html)
  - [python-configparser](https://docs.python.org/2/library/configparser.html)
  - [scikit-learn 0.19.1](https://scikit-learn.org/stable/install.html)

It's advisable you use the same versions for python libs as listed in our requirements.txt

How to Install ?
================
The first step is to acquire a stable version of MultiExplorer from a release in the [repository](https://github.com/lscad-facom-ufms/MultiExplorer.git)

If you don't want to install every dependency yourself, you may run "make install" as root. It will simply run a couple of "apt-get install" and "pip2 install" for you.

Sniper installation you will have to handle by yourself, since it's not readily available, and it's simple not possible to simply wget it and run it's installation through scripting.

You will also have to set the SNIPER_PATH in your "MultiExplorer/src/config.py" file. If you are not sure how to create this file, run "make config". It will create the file and all you have to do is open it and fill with your real PATH values.

MultiExplorer also requires [McPAT](https://github.com/HewlettPackard/mcpat), but it's already bundled into MultiExplorer, since it's license allows it, and you don't have to worry about installing it.


Run your first simulation
=========================
There are many input examples available in the "input-examples" folder.
You should run one of the .json files in that folder.
For example:

$ python MultiExplorer/src/MultiExplorer.py input-examples/quark.json

Just wait the simulation steps finish. All the output files will be in the rundir folder. Note that MultiExplorer will create a folder 
for your design and simulation,5n the rundir folder, following the order: PerformanceSimulatorJSONInputApplicationDate_Time. 
Example: SniperSimQuarkCholesky20210205_104802


Output files
=========================
These files will be in the rundir folder after running MultiExplorer:

ArchComparison.csv:  a csv file with physical and performance results from the original and the proposed design.          

MCPATPhysicalResults.txt: McPAT physical estimates (area, power, etc.) of the original design.
               
outputBruteForce.csv: a csv file with all the configurations obtained from our BF DS-DSE algorithm.
      
performanceReport.txt: outputs of the performance simulator.     

populationResults.csv: a csv file with all the configurations from our NSGA2-based DS-DSE algorithm.
    
sim.info: log file of the benchmark compilation.

sim.out: output of the performance simulator.

SniperPerformanceResults.txt: log file of the performance simulator

SniperSimQuarkCholesky_mcpatInput.xml: input file for the Physical estimator (McPAT).

**There may be additional files, reserved for future use in MultiExplorer.


Issues
=========================
If you have issues when running MultiExplorer


Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com
