import argparse
import subprocess


def application():
    """
    The starting point for the GeneticAncestryTool.
    Many of the commands will be the same as PLINK (documentation: http://zzz.bwh.harvard.edu/plink/reference.shtml)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--bfile', help='Specify .bed, .bim and .fam.', type=str)
    parser.add_argument('--bmerge', nargs='*', help='Merge in a binary fileset.', type=str) # '*'= ≥0 args, '+'= ≥1 args
    parser.add_argument('--make-bed', help='Make .bed, .fam and .bim.', type=None)
    parser.add_argument('--out', help='Specify output root filename.', type=str)

    args = parser.parse_args()
    cmd = 'plink --bfile Tutorial_Matrix --bmerge hapmap_CEU_r23a.bed hapmap_CEU_r23a.bim hapmap_CEU_r23a.fam --out ' \
          'file_hapmap_merged'
    subprocess.run(cmd, shell=True)
    print(args)
