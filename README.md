NIST Repository:
Python tools for OpenFOAM simulations of filament shapes in embedded 3D printing
Version 1.0.0

Authors:
  Leanne Friedrich
    National Institute of Standards and Technology, MML
    Leanne.Friedrich@nist.gov
  Jonathan E. Seppala
    National Institute of Standards and Technology, MML
    Jonathan.Seppala@nist.gov

Contact:
  Leanne Friedrich
    Leanne.Friedrich@nist.gov

Description:

In embedded 3D printing, a nozzle is embedded into a support bath and extrudes filaments or droplets into the bath. Using OpenFOAM, we simulated the extrusion of filaments and droplets into a moving bath. OpenFOAM is an open source computational fluid dynamics solver. This repository contains the following Python tools:

- Tools for generating input files for OpenFOAM v1912 or OpenFOAM v8 tailored to a nozzle extruding a filament into a static support bath.
- Tools for monitoring the status of OpenFOAM simulations and aborting them if they are too slow.
- Tools for moving output files between storage locations. (For example, it can automatically move all files to a server, but only necessary files to your hard drive)
- Tools for generating images and tables from the 3D time series.
- Tools for compiling images into videos.
- Tools for analyzing, summarizing, and plotting data.

-------------------
General Information
-------------------

Version 1.0.0 was generated: April 2020 - April 2021.

--------------
Data Use Notes
--------------

This code is publicly available according to the NIST statements of copyright,
fair use and licensing; see 
https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software

You may cite the use of this code as follows:
Friedrich, L., & Seppala, J.E. (2021), OpenFOAM simulations of filament shapes in embedded 3D printing, Version 1.0.0, National Institute of Standards and Technology, [DOI] (Accessed XXXX-XX-XX)

The OpenFOAM input file tools are compatible with OpenFOAM v1912 and OpenFOAM v8. Between the two version, OpenFOAM did change the syntax on a couple of input variables, so you may need to update ncreate3d.py for future versions of OpenFOAM. Between the two versions, OpenFOAM also modified the way they output paraview files. In v1912, OpenFOAM generated a .vtm file and folder for each time step, and compiled all of the timesteps into a .vtm.series file that could easily be imported into Paraview. In v8, OpenFOAM generates a .vtk file for each time step but does not generate a .series file. folderparser.py has a function generateVTKSeries that generates these .series files, which make it easy to load the whole time series in Paraview.

----------
References
----------

This code is described in:
  Friedrich, L., & Seppala, J.E. (2021) Simulated filament shapes in embedded 3D printing, submitted for publication

-------------
Data Overview
-------------

This data follows the basic storage structure established by OpenFOAM.

The files included in this publication use the following hierarchy:

- *README.md*

- *LICENSE*

- *config.py*
    - for importing packages and setting environmental variables, e.g. folders

- *folderparser.py*
    - Functions for handling files and folders used in OpenFOAM simulations of embedded 3D printing of single filaments. Written for OpenFOAM v1912 and OpenFOAM 8. folderparser identifies log files from interFoam, etc. and collects information into csv tables
	
- *requirements.txt*
    - List of required packages, for use with virtual environments. This file can be used with virtualenv for easy import of dependencies.

- **configs/**
    - *config.yml*
	- set path.logs (log folder), path.log_config (logging config yml path), path.c (path to C folder holding OpenFOAM docs), path.e (path to E folder holding OpenFOAM docs), path.server (path to server folder holding OpenFOAM docs), and path.fig (path to figure folder)

    - *environment.yml*
	- set up virtual environment

    - *logging.yml*
	- set up log generation

- **logs/**
    - for holding logs

- **paraviewscripts/**
    - pvpython scripts for generating images and tables. These run on pvpython.exe. Some scripts use packages that are not native to pvpython.exe and require a virtual environment. We use virtualenv to implement this.

    - *comboscript.py*
	- Collecting interface points into csvs from vtk files and generating images from vtk files. Scripting for many folders and many images and tables.

    - *linescript.py*
	- Collecting line traces through the bath in vtk files. Scripting for many folders and many images and tables.

    - *paraview_csv.py*
	- Functions for collecting interface points into csvs from vtk files

    - *paraview_general.py*
	- Functions for importing vtk files of simulated filaments.

    - *paraview_line.py*
	- Functions for collecting line traces through the bath in vtk files
            
    - *paraview_screenshots.py*
	- Functions for generating images of filaments from vtk files.

- **pythonscripts/**
    - python tools for generating and analyzing OpenFOAM files. These are written for python3.

    - *donescript.py*
	- Functions for moving folders between computers, servers, for OpenFOAM simulations of embedded 3D printing of single filaments.

    - *foldermover.py*
	- Functions for moving folders between computers, servers, for OpenFOAM simulations of embedded 3D printing of single filaments.

    - *folderscraper.py*
	- Functions for generating legends for OpenFOAM simulations of embedded 3D printing of single filaments. Written for OpenFOAM v1912 and OpenFOAM 8. Scrapes input files for input variables.

    - *interfacemetrics.py*
	- Functions for analyzing simulated single filaments

    - *interfacemetrics_yielding.ipynb*
	- Jupyter notebook for analyzing OpenFOAM simulation data, for the yielding dataset

    - *interfacemetrics_viscsweep.ipynb*
	- Juptyer notebook for analyzing OpenFOAM simulation data, for the viscosity sweep dataset (Friedrich, L., & Seppala, J.E. (2021) Simulated filament shapes in embedded 3D printing, submitted for publication)

    - *interfacePlots.py*
	- All of the plotting functions for plotting interface measurements. (plot_general, plot_line, plot_metrics, plot_pic, plot_slices, and plot_steady)

    - *movescript.py*
	- Moves folders to server. Loops continuously.

    - *ncreate3d.py*
	- Functions to generate OpenFOAM input files for a nozzle in a 3D bath

    - *noz3dscript.ipynb*
	- Jupyter notebook for generating OpenFOAM input files.

    - *plot_general.py*
	- Plotting tools for analyzing OpenFOAM single filaments

    - *plot_line.py*
	- Functions for plotting line traces from Paraview

    - *plot_metrics.py*
	- Functions for plotting overall metrics, such as simulation time, folder name, simulation rate, cross-sectional area...

    - *plot_pic.py*
	- Functions for plotting images of filaments and baths
	
    - *plot_slices.py*
	- Functions for plotting cross-sections

    - *plot_steady.py*
	- Functions for plotting steady state metrics

    - *videoscript.py*
	- Script for combining images into videos. Loops continuously every 6 hours.

---------------
Version History
---------------

4/09/2021: v1.0.0

--------------------------
METHODOLOGICAL INFORMATION
--------------------------


This dataset is linked with the paper and dataset linked at the top of this document. Typical workflow for a Windows desktop for a single parent folder (e.g. HBHBsweep) was as follows:

1a. In JupyterLab, generate input files using noz3dscript.ipynb and ncreate3d.py. For each simulation, this generates legend.csv, geometry.csv, case, 0, constant, system, Allclean, Allrun, Continue. For the parent folder, this generates mesh and geometry files. 
1b. (optional file generation) Move files to server and other computers, if needed.

2. In Ubuntu, edit the bash script runallfiles.sh to include appropriate number of processes, correct list of folders. In Ubuntu, run runallfiles.sh in background. This starts the simulations running. (bash runallfiles.sh &). OpenFOAM will generate 0.1, 0.2, ..., VTK, and logs during this process.

3a. In Anaconda powershell or JupyterLab, run donescript.py on each computer while simulations are running (python3 donescript.py [parentfolder]). This watches the simulations and aborts them using case/system/controlDict if they are too slow. In newer versions, donescript.py is implemented inside of runallfiles.sh.
3b. (optional file management) Modify movescript.py to look at relevant folders. In Anaconda powershell or JupyterLab, run movescript.py on each computer while simulations are running or after they are done (python3 movescript.py X, where X is the number of hours to wait between loops). This moves simulation results to the server.

4a. Modify comboscript.py to include relevant folders and desired image types. Turn on waiting to let this script run continuously. In Command Prompt, run ([path]\pvpython.exe [path]\comboscript.py). Do this while simulations are running or after they are done. This generates images and interfacePoints.
4b. (optional image generation) Modify videoscript.py to look at relevant folders. In Anaconda powershell or JupyterLab, run videoscript.py to consolidate images into videos (python3 videoscript.py). Do this while images are being generated or after they are done. 

5a. In JupyterLab, use interfacemetrics_viscsweep.ipynb to generate sliceSummaries.csv, steadyPositions.csv, and steadyTimes.csv.
5b. In JupyterLab, use interfacemetrics_viscsweep.ipynb to make plots.

