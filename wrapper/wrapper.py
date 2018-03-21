import argparse
import subprocess


def call_plink(plink_args):
    """
    Makes a system call to plink given an arg parse object for plink.
    :param plink_args:
    """
    plink_command = 'plink '
    args_iterable = vars(plink_args)
    for arg in args_iterable:
        argument_value = getattr(plink_args, arg)
        if argument_value is not None:
            arg_as_plink_flag = '--{} {} '.format(arg, argument_value)
            plink_command += arg_as_plink_flag
        else:
            plink_command += '--{} '.format(arg)

    subprocess.run(plink_command, shell=True)


def run_plink(commandline_args):
    """
    Given an arg parse argument object, parse the plink commands specified. For example, if you want to do a
    `bmerge`, this function will handle that according to plink. This function may be useless the more I think about
    it. It might become useful if we have to run eigenstrat from the command line. Not totally sure yet.
    :param commandline_args:
    """
    if commandline_args.bmerge is not None:
        call_plink(commandline_args)


def application():
    """
    The starting point for the GeneticAncestryTool.
    Many of the commands will, and should probably, be the same as PLINK (documentation:
    http://zzz.bwh.harvard.edu/plink/reference.shtml)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--bfile', help='Specify .bed, .bim and .fam.', type=str)
    parser.add_argument('--bmerge', nargs='*', help='Merge in a binary fileset.', type=str) # '*'= ≥0 args, '+'= ≥1 args
    parser.add_argument('--make-bed', nargs='*', help='Make .bed, .fam and .bim.', type=bool)
    parser.add_argument('--out', help='Specify output root filename.', type=str)

    args = parser.parse_args()
    args.bmerge = ' '.join(args.bmerge)

    #args_dict = args.__dict__
    #print(args_dict)
    # for k in args.__dict__:
    #     print(k, args.__dict__[k])

    print('Running plink with args:')
    for arg in vars(args):
        print('--' + arg + ' =', getattr(args, arg))

    run_plink(commandline_args=args)
