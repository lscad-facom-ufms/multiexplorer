MultiExplorer-VM Tool - version 1.0
===================
Muliexplorer-VM is a framework that that has a workflow to provide virtual machine configurations according to the users’ requirements and applications constraints. MultiExplorer-VM uses CloudSim as the cloud simulator. The design space exploration (DSE) is performed by a NSGA2-based algorithm. In this current version, Muliexplorer-VM also adopts a brute-force (bf) algorithm to explore all viable alternatives to the design. The bf has been used as a validation step to our DSE approach. To know more about Multiexplorer-VM and DSE approach please refers to our paper:

SANTOS, R.;DUENHA, L.; SILVA, A. C. S.; BIGNARDI, T.; SOUSA, M.; TEDESCO, L.; MELGAREJO JUNIOR, J.; AZEVEDO, R.; ORDONEZ, E. D. M.. 
Dark-Silicon Aware Design Space Exploration. JOURNAL OF PARALLEL AND DISTRIBUTED COMPUTING, v. 120, 2018, pp 295-306, ISSN 0743-7315.


Dependencies
============
To properly execute Multiexplorer, be sure to have all these softwares:
- [Python 2.7](https://www.python.org/download/releases/2.7/)
  - [lxml](https://lxml.de/installation.html)
  - [python-configparser](https://docs.python.org/2/library/configparser.html)
  - [scikit-learn 0.19.1](https://scikit-learn.org/stable/install.html)

It's advisable you use the same versions for python libs as listed in our requirements.txt

How to Install ?
================
The first step is to acquire a stable version of Multiexplorer-VM from the [repository](https://github.com/lscad-facom-ufms/MultiExplorerVM.git)

If you don't want to install every dependency yourself, you may run "make install" as root. It will simply run a couple of "apt-get install" and "pip2 install" for you.



Run your first simulation
=========================
After starting the Multiexplorer VM, open a terminal window and type:

$ cd ds-repo

There are many input examples available in the input-examples folder. You should run one of the .json files in that folder. For example:

$ python MultiExplorer/src/MultiExplorer.py input-examples/c5.large-0.json

Just wait the simulation steps finish. All the output files will be in the rundir folder. Note that Multiexplorer will create a folder 
for your design and simulation,5n the rundir folder, following the order: JSONInputApplicationDate_Time. 
Example: c5.large-58129049020220707_095623


Output files
=========================
These files will be in the rundir folder after running MUltiexplorer:
               
outputBruteForce.csv: a csv file with all the configurations obtained from our BF DS-DSE algorithm.

populationResults.csv: a csv file with all the configurations from our NSGA2-based DS-DSE algorithm.

**May there are other files that are reserved for future use in Multiexplorer.


Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com
