# Genetic Ancestry Tool

## Overview
Automate the process of merging genotype data with HapMap using PLINK. 
This automation is done using a python wrapper around PLINK and EIGENSTRAT (linked below).

## Software Dependencies/Requirements
* **Linux/Unix**
* **[Python 3+](https://www.python.org/downloads/)**
    * Developed using 3.6.3, but should work on anything after about 3.4.
* **[PLINK](http://zzz.bwh.harvard.edu/plink/) 1.9**
* **[R](https://www.r-project.org/) 3.5.0**


## Main Application Parameters
* `--bfile` _Specify .bed, .bim and .fam._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--bmerge` _Merge in a binary fileset._ [Example](http://zzz.bwh.harvard.edu/plink/dataman.shtml#bmerge)
* `--make-bed` _Make .bed, .fam and .bim. **(ON HOLD)**_ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#bed)
* `--out` _Specify output root filename._ [Example](http://zzz.bwh.harvard.edu/plink/data.shtml#plink)
* `--snp_ref` _Specify snp reference file to convert data from SNP IDs to rsIDs._
* `--noweb` _Run PLINK without the internet. (For testing; inactive)_ [Example](http://zzz.bwh.harvard.edu/plink/binary
.shtml)
* `--n` _Flag for extracting a set amount of rsIDs from the dataset. Use if the files are large or for benchmarking/testing purposes.'_
## PLINK specific commands
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
    * A new `*.eigenvec` file is generated and it includes the population information and iid's. 
    * The R script `plotting.R` plots the final `.eigenvec` file and outputs it in the top level directory as `Rplots
    .pdf`.
    
* `util.py`
    * Utility script that holds common methods between the various scripts.
* `pca.py`
    * Contains method to get the population information and iid's from the static `.ped` file that we will add to the
     `.eigenvec` file that is generated after running PCA in PLINK.
    * Calls the R script that is used for plotting.

## Other Files
* `20130606_g1k.ped`
    * The pedigree file that contains the Individual ID's (iid's) and the population information to aid in plotting 
    the final `.eigenvec` file. That is, we determine the population, if it exists, from this file and will color our
     data based on that.
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
dataset_sample_PCA.eigenval
dataset_sample_PCA.eigenvec
dataset_sample_PCA.log
dataset_sample_PCA.nosex
dataset_sample_PCA_PLOT_DATA.eigenvec
dataset_sample_RS_ONLY.bed
dataset_sample_RS_ONLY.bim
dataset_sample_RS_ONLY.fam
dataset_sample_RS_ONLY.log
dataset_sample_RS_ONLY.nosex
dataset_sample_RS_ONLY_exc_missnp_log.bed
dataset_sample_RS_ONLY_exc_missnp_log.bim
dataset_sample_RS_ONLY_exc_missnp_log.fam
dataset_sample_RS_ONLY_exc_missnp_log.log
dataset_sample_RS_ONLY_exc_missnp_log.nosex
hapmap_sample_RS_ONLY.bed
hapmap_sample_RS_ONLY.bim
hapmap_sample_RS_ONLY.fam
hapmap_sample_RS_ONLY.log
hapmap_sample_RS_ONLY_exc_missnp_log.bed
hapmap_sample_RS_ONLY_exc_missnp_log.bim
hapmap_sample_RS_ONLY_exc_missnp_log.fam
hapmap_sample_RS_ONLY_exc_missnp_log.log
merged_sample_data.bed
merged_sample_data.bim
merged_sample_data.fam
merged_sample_data.log
merged_sample_data.nosex
merged_sample_data_MAF.bed
merged_sample_data_MAF.bim
merged_sample_data_MAF.fam
merged_sample_data_MAF.log
merged_sample_data_MAF.nosex
merged_sample_data_MAF.prune.in
merged_sample_data_MAF.prune.out
merged_sample_data_MAF_EXTRACT.bed
merged_sample_data_MAF_EXTRACT.bim
merged_sample_data_MAF_EXTRACT.fam
merged_sample_data_MAF_EXTRACT.log
merged_sample_data_MAF_EXTRACT.nosex
merged_sample_data_MERGED_LOG_MISSNP.txt
~~~
* Running the command below will generate the plot for the sample. Passing the final eigenvec file will create the plot.
* We don't need to do this because we are using `os.system` instead of `subprocess`.
~~~
Rscript --vanilla plotting.R sample_data/dataset_sample_PCA_PLOT_DATA.eigenvec
~~~
* Explanation of files:
    * `_RS_ONLY` contains the original datasets with only rsID's
    * `_exc_missnp_log` are files excluding the merged `missnp` and `log` files.
    * `_MAF` are files that have been pruned with the `--maf` PLINK argument
    * `_MAF_EXTRACT` files have the `prune.in` files removed after the MAF.
    * `_PCA` is the data after running principal component analysis
    * `_PCA_PLOT_DATA` is data for the R script to plot the Principal Components.
## Output Files
* Files with structure that resemble those from above.
* PCA Plot from Principal Component Analysis 
    * PCA Plot output maps genetic ancestry of subpopulations in comparison to one another. PCA plot depicts how closely related specific subpopulations are to one another regarding a specific trait.
    * The PCA plot is outputted as `Rplots.pdf` in the top level directory of the program. 


