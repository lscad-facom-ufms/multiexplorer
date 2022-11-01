MultiExplorer Tool
===================
Muliexplorer is a framework that provides a processor chip design by putting together performance simulation, 
physical estimation, and design space exploration steps.

MultiExplorer uses Sniper as a performance simulator and McPAT as physical estimator. 

The design space exploration (DSE) is performed by a NSGA2-based algorithm.

MultiExplorer assumes that all processor designs are dark silicon aware so that it uses the power density as a
constraint in the DSE step.To know more about MultiExplorer and its Dark-Silicon aware - DSE approach please refer
to our paper:

SANTOS, R.;DUENHA, L.; SILVA, A. C. S.; BIGNARDI, T.; SOUSA, M.; TEDESCO, L.; MELGAREJO JUNIOR, J.; AZEVEDO, R.; ORDONEZ, E. D. M.. 
Dark-Silicon Aware Design Space Exploration. JOURNAL OF PARALLEL AND DISTRIBUTED COMPUTING, v. 120, 2018, pp 295-306, ISSN 0743-7315.

Dependencies
============
Currently **MultiExplorer** has native support only for **Linux** distributions. **Ubuntu 18.04** is recommended.

But you can use **MultiExplorer** in any platform that supports [Docker](https://www.docker.com/), by running it in
a container.

This is highly advisable even when using Linux distros, as our **Docker** environment will be easier to set up and maintain.

If you are using the container on a Windows environment, you will need to use
[Xming](http://www.straightrunning.com/XmingNotes/), so **Docker** can access the graphic display.

Other software requirements are:
- [Sniper 7.4](http://snipersim.org)
  - [Sniper's Benchmarks](https://snipersim.org/w/Download_Benchmarks) 
- [Python 2.7](https://www.python.org/download/releases/2.7/)

It's advisable you use the same versions for **python** libs as listed in our **pip** requirements file 
(*requirements.txt*).

Using the Docker Environment
============================
As long as **Docker** is installed and running in your platform, you can use **MultiExplorer** in a container.

`$ docker-compose up -d`

`$ docker exec -it <<container_name>> bash`

How to Install ?
================
The first step is to acquire a stable version of MultiExplorer from a release in the
[repository](https://github.com/lscad-facom-ufms/MultiExplorer.git)

Then you can use our **GNU Make** script for the basic setup.

`$ make`

Important setting files are:
- *.env*: you must set the DISPLAY variable if you want to use the GUI (only required for **Docker** environments)
- *MultiExplorer/src/config.py*: you will need proper path settings (much easier in the **Docker** environments)

Using the GUI (Graphic User Interface)
======================================
**MultiExplorer** now has a graphic user interface.

Run `$ python ME.py` to use it.

If you are using **Docker** in a Windows environment, remember to run [Xming](http://www.straightrunning.com/XmingNotes/),
and disable authentication.

If you are using **Docker** in a Linux environment, running `$ xhost +` will likewise disable authentication, allowing
the use of the display by software in the container.

Using the command line
=========================
There are many input examples available in the "input-examples" folder.
You should run one of the .json files in that folder.
For example:

`$ python MultiExplorer/src/MultiExplorer.py input-examples/quark.json`

Just wait the simulation steps finish. All the output files will be in the rundir folder. Note that MultiExplorer will create a folder 
for your design and simulation,5n the *rundir* folder, following the order: PerformanceSimulatorJSONInputApplicationDate_Time. 
Example: SniperSimQuarkCholesky20210205_104802

Output files
=========================
These files will be in the *rundir* folder after running MultiExplorer from the command line:

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

If you are using the GUI, results are presented directly through it, but input and output files can still be found
in the *rundir* folder for each run, in the folder corresponding to the selected execution flow
(e.g.: */rundir/Multicore_CPU_Heterogeneous_DSDSE*).

Issues
=========================
If you have issues when running MultiExplorer, report them at our github
[issues](https://github.com/lscad-facom-ufms/multiexplorer/issues).

Please notice that we will be focusing on code issues. Set up difficulties can be almost always avoided using
**Docker**, so if you are having difficulties with a native set up, try that first.

Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com

Attributions
==========================
Icons used in our GUI were obtained through [Flaticon](https://www.flaticon.com/).

<a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Alfredo Hernandez - Flaticon</a>

<a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Alfredo Hernandez - Flaticon</a>
