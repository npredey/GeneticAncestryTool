# Genetic Ancestry Tool

## Overview
Automate the process of merging genotype data with HapMap using PLINK. 
This automation is done using a python wrapper around PLINK and EIGENSTRAT (linked below).

## Software Dependencies/Requirements
* **Linux/Unix**
* **[Python 3+](https://www.python.org/downloads/)**
    * Developed using 3.6.3, but should work on anything after about 3.4.
* **[PLINK](http://zzz.bwh.harvard.edu/plink/)**
* **[Matplotlib](https://matplotlib.org/)**
* **[Pandas](https://pandas.pydata.org/)**
* **[NumPy](http://www.numpy.org/)**


## Main Application Parameters
* `--bfile` _Specify .bed, .bim and .fam._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--bmerge` _Merge in a binary fileset._ [Example](http://zzz.bwh.harvard.edu/plink/dataman.shtml#bmerge)
* `--make-bed` _Make .bed, .fam and .bim. **(ON HOLD)**_ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--out` _Specify output root filename._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#plink)
* `--snp_ref` _Specify snp reference file to convert data from SNP IDs to rsIDs._
* `--noweb` _Run PLINK without the internet._ [Example](http://zzz.bwh.harvard.edu/plink/binary.shtml)
* `--maf` _Runs minor allele frequency pruning on file prior to PCA_ [Example](http://zzz.bwh.harvard.edu/plink/thresh.shtml)
* `--indep-pairwise` _Runs LD pruning on file prior to PCA_ [Example](http://zzz.bwh.harvard.edu/plink/summary.shtml)
* `--pca` _Runs Principal Component Analysis on file_ [Example](https://www.cog-genomics.org/plink/1.9/strat)

# Importing 
To import the project from GitHub, open a terminal session and type only one of either of these commands in the 
directory you want the repository:
~~~
git clone https://github.com/npredey/GeneticAncestryTool.git
git fork https://github.com/npredey/GeneticAncestryTool.git
~~~

# Scripts 
* `pca.py`
    * Contains methods for plotting principal components and generating `*.eigenvec` files for a dataset.
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
    * Calls PLINK to perform an initial merge after the input data is cleaned. This also creates new intermediary 
    files that are used to generate the principal components. These are not deleted after the program is finished, 
    but they are safe to delete after a program run because they are generated each new time.
    * Parses the `.log` file output from the initial merge and the corresponding `.missnp` file to collect any 
    problematic (duplicate, multiple, etc.) rsID's that will later be excluded from the final merge. 
    * Extracts rsID's from the input files after the merging of the `.log` and `.missnp`. This is outputted to 
    intermediary files (`*.bed`, `*.bim`, and `*.fam`).
    * Once the input data files are thoroughly inspected, a final merge is run.
    * Merged files are run in plink with the following commands to run PCA, with ld pruning is done prior to running 
    PCA:
    ~~~
    plink --bfile nameoffiles --maf 0.05 --make-bed 
    plink --bfile nameoffiles --indep-pairwise 50 5 0.3 --out outputname
    plink --bfile nameoffiles --extract outputname.prune.in --out newoutputname -make--bed 
    ~~~
    * This is followed by performing Principal Component Analysis (PCA) on the data:
    ~~~
    plink --bfile newoutputname --pca
    ~~~
    * PCA gives the output files `plink.eigenvec` and `plink.eigenval`. The `plink.eigenvec` file is run through a python 
    script to add the population information of the individuals to the `plink.eigenvec` file. 
    * A new `*.eigenvec` file is generated and it includes the population information. This new file is then plotted in 
    python to generate the final PCA Plot output. 
    
* `util.py`
    * Utility script that holds common methods between the various scripts.

# Input Data
## `*.bed`, `*.bim`, and `*.fam` Files
* Place the genotype and HapMap data together in the same directory. Intermediary files will be created, so it is 
recommended that these input files be together in an otherwise empty directory.
* Provide the full path to each file, unless you copy the code in the project directory. See the example code for an 
explanation.

## Example
##### To run the main applcation (GeneticAncestryTool):
* Navigate to the top level directory `cd ../GeneticAncestryTool`
* In the terminal, run the following command
~~~
./GeneticAncestryTool.py --bfile sample_data/dataset_sample --bmerge sample_data/hapmap_sample --out sample_data/merged_sample_data
~~~
* Once the run is finished, the directory `sample_data/` should now be:
~~~
dataset_sample.bed
dataset_sample.bim
dataset_sample.fam
dataset_sample_RS_ONLY.bed
dataset_sample_RS_ONLY.bim
dataset_sample_RS_ONLY.fam
dataset_sample_RS_ONLY.log
dataset_sample_RS_ONLY.nosex
hapmap_sample.bed
hapmap_sample.bim
hapmap_sample.fam
merged_sample_data.bed
merged_sample_data.bim
merged_sample_data.fam
merged_sample_data.log
merged_sample_data.nosex
~~~

## Output Files
* Like the example above, the ouput of the files will include:
    * `.bed`, `.bim`, `.fam` files of the following datasets:
        * Genotype and HapMap data with only rs ID's (.."_RS_ONLY")
* PCA Plot from Principal Component Analysis 
    * PCA Plot output maps genetic ancestry of subpopulations in comparison to one another. PCA plot depicts how closely related specific subpopulations are to one another regarding a specific trait. 


