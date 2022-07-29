# Release Sheet Table Automation

EGM722: Programming for GIS and Remote Sensing at Ulster University

## 1. Background:

As a principal contractor of telecommunications, Viberoptix Ltd are responsible for the design and build 
of full-fibre networks across Great Britain. One of the final steps in the design process for any area, is 
to provide a Release Sheet. This document comprises of a list of property addresses, which have been planned 
to, and subsequent information regarding the specific equipment and network route from which each premise is 
to be supplied.

The current, inefficient production time of Release Sheets have inhibited the overall design process. 

The aim of this project is to produce a script which will auto-generate a Release Sheet, thereby removing 
the repetitive task of doing so manually, cutting down time and cost requirements for each new area. Meanwhile, 
producing and documenting the script in a way which provides a basis for future collaboration throughout the design 
department, in the use and development of the script. 

Further information on Viberoptic Ltd can be found [here](https://www.viberoptix.com/).

## 2. Setup and Installation:

Git offers an efficient platform for geospatial software developers to collaborate and manage source code (Anbaroğlu, 2021). The developed Python script, with the required test data, and setup files are all contained within the published GitHub ‘arc_clone’ repository. Once the repository has been forked, GitHub’s Desktop application can provide a user-friendly graphical interface to aid in the setup and editing scripts. Here, the arc_clone repository can be cloned as a localised, offline copy.

Anaconda, and the Anaconda Navigator similarly provide a graphical user interface aiding in the setup and management of coding environments. Utilising Anaconda, a new environment can be setup based of the environment.yml found within the cloned repository file. 
Once the repository has been cloned, and the required environment has been created the developed Python script can easily be run through a PyCharm, or similar integrated development environments (IDE). 

For now, the script requires a minor change to run successfully. Once opened in an IDE, replace the source folder path "C:/Users/pjbog/arc_clone/DATA/project.gdb" with the unique folder path where the localised repository has been cloned to. These changes are located on lines 7, 85, 105, 124, 143, 164 and 215. This alteration in the script can be carried out quite easily using ctrl + r, replacing all instance of "C:/Users/pjbog/arc_clone/DATA/project.gdb" with the new folder path.
Python and Arcpy are the main dependencies to run the finalised script. In the environment.yml file, ‘notebook’ has also been listed as a dependency. However, this addition is intended to ease the process of future collaborated developments.  

As the script was developed to carry out a very niche function, test data has been provided. Located within the ‘DATA’ folder in the GitHub repository. 

## 3. ⚠️ Trouble Shooting ⚠️

> **As the script was developed using Arcpy 2.9, the code will not be compatible with hardware with earlier versions of ArcGIS installed. Therefore, to ensure the script runs smoothly, please ensure that the installed version of ArcGIS is 2.9 or later.**

With older version of ArcGIS, some tools may require their script to be re-written. To convert tool scripts to previous version please see https://pro.arcgis.com/en/pro-app/latest/tool-reference/main/arcgis-pro-tool-reference.htm

Hardware with ArcGIS version 2.9 should have no issues running the script.

If a newer version of ArcGIS is installed, when creating an environment with the dependencies set out in the environment.yml file, version compatibility between the script and the environment can cause issues. To ensure version compatibility, an environment can be created using command prompt, run as administrator. 

To create an environment using an admistrative command prompt please follow the step below. Setting up the coding environment this way will automatically install the environment dependency version which matches the installed version of ArcGIS.

### 1. Change Directory to folder path - changing 'C:\Users\pjbog\arc_clone' to your unique folder path
```
cd C:\Users\pjbog\arc_clone
```

### 2. View directoy, ensuring it contains the cloned repository folder and files
```
dir
```

### 3. Create environment using the environment.yml file 
```
Conda env create -f environment.yml
```
However, creating the environment in this way can cause further issues such as ‘Conda not recognised as internal or external command’. This error can be overcome by running ‘where conda’ within your anaconda prompt and adding the shown folder paths to your PATH environment variable under the advance system settings. Once added, follow the previous steps using the administrative command prompt to setup the required environment. 

For further error corrections and advice, please see the following forums for help revolving GitHub, GIS and Python.

-	https://github.com/orgs/community/discussions/
-	https://gis.stackexchange.com/
-	https://discuss.python.org/
