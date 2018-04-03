import os
import subprocess


def call_plink(plink_args):
    """
    Makes a system call to plink given a dictionary of arguments for plink.
    :param plink_args:
    """
    plink_command = 'plink '
    for arg, arg_value in plink_args.items():
        print(arg, arg_value)
        # argument_value = getattr(plink_args, arg)
        if arg_value is not None:
            if arg_value != '':
                arg_as_plink_flag = '--{} {} '.format(arg, arg_value)
                plink_command += arg_as_plink_flag
            else:
                plink_command += '--{} '.format(arg)

    print(plink_command)
    subprocess.run(plink_command, shell=True)


def format_wrapper_args(args):
    if args.bmerge is not None:
        args.bmerge = ' '.join(args.bmerge)
    if args.make_bed is not None:
        args.make_bed = ''
    return args


def format_multiple_file_input(input_files_directory):
    """
    When merging multiple files, per http://zzz.bwh.harvard.edu/plink/dataman.shtml#mergelist, the files must be in the
    following format:
        fB.ped fB.map
        fC.ped fC.map
        fD.ped fD.map
        fE.bed fE.bim fE.fam
        fF.bed fF.bim fF.fam
        fG.bed fG.bim fG.fam
        fH.bed fH.bim fH.fam
    where each corresponding *.bed, *.bim, and *.bam must together on a line in that specific order. This function
    takes an input of a directory of files and returns a file output like the example above that will later be run
    through PLINK.
    :param input_files_directory:
    """
    temp_plink_input_filename = 'plink_input.txt' # this should later be deleted, once the PLINK run is done
    for dirpath, dirnames, filenames in os.walk(input_files_directory):
        print()