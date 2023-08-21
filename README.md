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

User Manual
===========
MultiExplorer has a user manual available:

[English Version](https://drive.google.com/file/d/1XCgdApa8Pm0iUacygrTmWGyWXquhjOuU/view?usp=drive_link)

[Versão em Português](https://drive.google.com/file/d/1JYvdxGZpFAuLS1jU-EBfLuURGj3zWxiP/view?usp=drive_link)

How to Install ?
================
The first step is to acquire a stable version of MultiExplorer from a release in the
[repository](https://github.com/lscad-facom-ufms/MultiExplorer.git)

Important setting files are:
- *.env*: you must set the DISPLAY variable if you want to use the GUI (only required for **Docker** environments)
- *MultiExplorer/src/config.py*: you will need proper path settings

Then you can use our **GNU Make** script for the basic setup.

`$ make`

Using a **Docker** container is advised.
We maintain a pre-compiled version of Sniper-8.0 for use in the Docker environment
[precompiled_sniper](https://drive.google.com/file/d/1aXNxy6OZ7NjP1XUgnhOGuTFAUePtwZkW/view) that you will also need to run MultiExplorer in this preset environment.

Using the Docker Container
============================
As long as **Docker** is installed and running, you can use **MultiExplorer** in a Docker container.

We have a pre-compiled version of Sniper and benchmarks, that will work in the
container: [pre-compiled sniper-8.0](https://drive.google.com/file/d/1GiQGrqf2AhLcd1fX9bfhGLvXP78YsnD3/view?usp=share_link).
Download it and extract it in this folder.

Our docker environment requires a ".env" file, including information about what
DISPLAY to connect to when running the GUI. A "example.env" is included, so you can just copy it
or run:

`$ make config`

After the ".env" file is ready, you can start the container and ssh into it using the following commands:

`$ docker-compose up -d`

`$ docker exec -it <<container_name>> bash`

When the container is built, there's still requirements to be installed, so you should run `$ make`.

After all requirements are installed and ready (including Sniper) you can start the GUI application by running:

`$ python ME.py`

If you are using **Docker** in a Windows environment, remember to run [Xming](http://www.straightrunning.com/XmingNotes/),
and disable authentication.

Even if you are running the container in a Linux environment, you still need to disable authentication on xhost
by running `$ xhost +`

Dependencies
============
Currently **MultiExplorer** has native support only for **Linux** distributions. **Ubuntu 18.04** is recommended.

But you can use **MultiExplorer** in any platform that supports [Docker](https://www.docker.com/), by running it in
a container.

This is highly advisable even when using Linux distros, as our **Docker** environment will be easier to set up and maintain.

If you are using the container on a Windows environment, you will need to use
[Xming]https://sourceforge.net/projects/vcxsrv/), so **Docker** can access the graphic display.

Other software requirements are:
- [Sniper 8.0](http://snipersim.org)
  - [Sniper's Benchmarks](https://snipersim.org/w/Download_Benchmarks)  
- [Python 2.7](https://www.python.org/download/releases/2.7/)

In case you want to take a shortcut from compiling Sniper and it's benchmarks, you can get a pre-compiled version . We have a pre-compiled version of Sniper with benchmarks, if you use the Docker environment.
- [Pre-Compiled Sniper with Benchmarks for the Docker Environment](https://drive.google.com/file/d/1aXNxy6OZ7NjP1XUgnhOGuTFAUePtwZkW/view)

It's advisable you use the same versions for **python** libs as listed in our **pip** requirements file 
(*requirements.txt*).

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

Command Line Output Files
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

Disclaimer About Python 2.7
=========================
Some tools and libs used by MultiExplorer still use Python 2.7, so there's no fixed schedule on the upgrade to Python 3.

We very much would like to advance to Python 3, but moving away from these resources or upgrading them to Python 3 ourselves proved not feasible right now. But this upgrade is still a long term objective of the MultiExplorer project.

Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com

Attributions
==========================
Icons used in our GUI were obtained through [Flaticon](https://www.flaticon.com/).

<a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Alfredo Hernandez - Flaticon</a>

<a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Alfredo Hernandez - Flaticon</a>
