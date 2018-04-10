import argparse
import sys
from parsing import parsing_plink
from wrapper.wrapper_util import call_plink, format_wrapper_args, get_bed_bim_fam_from_bfile


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
    parser.add_argument('--snp_ref', help='Specify snp reference file to convert data from SNP IDs to rsIDs.', type=str)
    parser.add_argument('--no-web', help='PLINK arg to run without the internet.', type=bool)

    args = parser.parse_args()
    if len(sys.argv) == 1:
        print(parser.print_help())
        sys.exit()

    args = format_wrapper_args(args)

    args_dict = args.__dict__
    input_binary_files = get_bed_bim_fam_from_bfile(args.bfile)

    print("Cleaning bim file {}.bim\n".format(args.bfile))
    parsing_plink.clean_bim(input_binary_files['bim'], args.bfile, args.snp_ref)
    print('Running PLINK with args:')
    for arg in vars(args):
        print('--' + arg + ' =', getattr(args, arg))
    print()

    run_plink(commandline_args=args_dict)
    inital_run_logfile = "{}.log".format(args.out)
    initial_run_missnp = "{}.missnp".format(args.out)

    print("Merging initial .log file: [ {} ] with .missnip file: [ {} ]\n".format(inital_run_logfile,
                                                                                  initial_run_missnp))
    parsing_plink.merge_log_to_missnp(args.out)

