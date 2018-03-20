import argparse


def application():
    """
    The starting point for the GeneticAncestryTool.
    Many of the commands will be the same as PLINK (documentation: http://zzz.bwh.harvard.edu/plink/reference.shtml)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--bfile', help='Specify .bed, .bim and .fam.', type=str)
    parser.add_argument('--bmerge', help='Merge in a binary fileset.', type=str)
    parser.add_argument('--make-bed', help='Make .bed, .fam and .bim.', type=str)
    parser.add_argument('--out', help='Specify output root filename.', type=str)

    args = parser.parse_args()
    print(args)
