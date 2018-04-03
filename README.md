# Genetic Ancestry Tool

## Overview
Automate the process of merging genotype data with HapMap using PLINK. 
This automation is done using a python wrapper around PLINK and EIGENSTRAT (linked below).

# Importing 

## Software Dependencies/Requirements
* **Linux/Unix**
* **[Python 3](https://www.python.org/downloads/)**
* **[PLINK](http://zzz.bwh.harvard.edu/plink/)**
* **EIGENSTRAT (A specific software tool within a larger package, EIGENSOFT)** **[Download](https://data
.broadinstitute.org/alkesgroup/EIGENSOFT/), [Code/Examples/Docs](https://github.com/DReichLab/EIG/tree/master/EIGENSTRAT)**

## Main Application Parameters
* `--bfile` _Specify .bed, .bim and .fam._
* `--bmerge` _Merge in a binary fileset._
* `--make-bed` _Make .bed, .fam and .bim._
* `--out` _Specify output root filename._

## Running the application
#####To run the main applcation (GeneticAncestryTool):
* Navigate to the top level directory `cd ../GeneticAncestryTool`
* 
