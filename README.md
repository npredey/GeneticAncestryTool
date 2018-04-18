# Genetic Ancestry Tool

## Overview
Automate the process of merging genotype data with HapMap using PLINK. 
This automation is done using a python wrapper around PLINK and EIGENSTRAT (linked below).

## Software Dependencies/Requirements
* **Linux/Unix**
* **[Python 3+](https://www.python.org/downloads/)**
    * Developed using 3.6.3, but should work on anything after about 3.4.
* **[PLINK](http://zzz.bwh.harvard.edu/plink/)**
* **EIGENSTRAT (A specific software tool within a larger package, EIGENSOFT) [Download](https://data.broadinstitute.org/alkesgroup/EIGENSOFT/),
 [Code/Examples/Docs](https://github.com/DReichLab/EIG/tree/master/EIGENSTRAT)** 
    * **NOTE: EIGENSTRAT is for Linux only. If you run the application and use EIGENSTRAT, it must be on a Linux 
    machine**

## Main Application Parameters
* `--bfile` _Specify .bed, .bim and .fam._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--bmerge` _Merge in a binary fileset._ [Example](http://zzz.bwh.harvard.edu/plink/dataman.shtml#bmerge)
* `--make-bed` _Make .bed, .fam and .bim. **(ON HOLD)**_ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--out` _Specify output root filename._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#plink)
* `--snp_ref` _Specify snp reference file to convert data from SNP IDs to rsIDs._
* `--noweb` _Run PLINK without the internet._ [Example](http://zzz.bwh.harvard.edu/plink/binary.shtml)

# Importing 
To import the project from GitHub, open a terminal session and type only one of either of these commands in the 
directory you want the repository:
~~~
git clone https://github.com/npredey/GeneticAncestryTool.git
git fork https://github.com/npredey/GeneticAncestryTool.git
~~~

# Scripts 
* `parsing_plink.py`
    * Contains methods to perform the following actions:
        * Merging `*.log` and `*.missnp` files.
        * Removing '.'s from the input `*.bim` files.
        * Swapping SNP_IDs for rsID's (this is a command line argument flag).
* `GeneticAncestryTool.py`
    * The script that calls the `application()` method of `wrapper.py` to run the wrapper script.
* `wrapper.py`
    * Reads in the command line arguments (above).
    * Cleans input `*.bim` files from the HapMap and input dataset using `parsing_plink.py` methods.
    * Calls PLINK to perform an initial merge after the input data is cleaned. This also creates new intermediary files.
    * Parses the `.log` file output from the initial merge and the corresponding `.missnp` file to collect any 
    problematic (duplicate, multiple, etc.) rsID's that will later be excluded from the final merge.
    * Extracts rsID's from the input files after the merging of the `.log` and `.missnp`. This is outputted to 
    intermediary files (`*.bed`, `*.bim`, and `*.fam`).
    * Once the input data files are thoroughly inspected, a final merge is done.
    * KAVINA'S PART
    
* `util.py`
    * Utility script that holds common methods between the various scripts.

# Input Data
## `*.bed`, `*.bim`, and `*.fam` Files
* Place the genotype and HapMap data together in the same directory. Intermediary files will be created, so it is 
recommended that these input files be together in an otherwise empty directory.
* Provide the full path to each file, unless you copy the code in the project directory. See the example code for an 
explanation.

## Running the application
##### To run the main applcation (GeneticAncestryTool):
* Navigate to the top level directory `cd ../GeneticAncestryTool`
* 
