import argparse
import sys
from parsing import parsing_plink
from wrapper.wrapper_util import call_plink, format_wrapper_args


def run_plink(commandline_args):
    """
    Given an arg parse argument object, parse the plink commands specified. For example, if you want to do a
    `bmerge`, this function will handle that according to plink. This function may be useless the more I think about
    it. It might become useful if we have to run eigenstrat from the command line. Not totally sure yet.
    :param commandline_args:
    """
    if commandline_args['bmerge'] is not None:
        call_plink(commandline_args)


def application():
    """
    The starting point for the GeneticAncestryTool.
    Many of the commands will, and should probably, be the same as PLINK (documentation:
    http://zzz.bwh.harvard.edu/plink/reference.shtml)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--bfile', help='Specify .bed, .bim and .fam.', type=str)
    parser.add_argument('--bmerge', nargs='+', help='Merge in a binary fileset.',
                        type=str)  # '*'= ≥0 args, '+'= ≥1 args
    parser.add_argument('--make-bed', nargs='*', help='Make .bed, .fam and .bim.', type=bool)
    parser.add_argument('--out', help='Specify output root filename.', type=str)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        print(parser.print_help())
        sys.exit()

    args = format_wrapper_args(args)

    args_dict = args.__dict__

    print("Cleaning bim file {}.bim\n".format(args.bfile))
    input_bim = args.bfile + '.bim'
    input_bed = args.bfile + '.bam'
    input_fam = args.bfile + '.fam'
    parsing_plink.clean_bim()
    print('Running PLINK with args:')
    for arg in vars(args):
        print('--' + arg + ' =', getattr(args, arg))
    print()

    run_plink(commandline_args=args.__dict__)
    inital_run_logfile = "{}.log".format(args.out)
    initial_run_missnp = "{}.missnp".format(args.out)

    print("Merging initial .log file: [ {} ] with .missnip file: [ {} ]\n".format(inital_run_logfile,
                                                                                  initial_run_missnp))
    # parsing_plink.merge_log_to_missnp(inital_run_logfile, initial_run_missnp)

