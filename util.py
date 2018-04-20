import os
import subprocess
import logging


def get_root_path(path):
    return '/'.join(path.split('/')[:-1]) + '/'


def get_filename(path):
    return path.split('/')[-1]


def call_plink(plink_args, command_key=''):
    """
    Makes a system call to plink given a dictionary of arguments for plink.
    :param command_key:
    :param plink_args:
    """
    run_logging_string = 'Running PLINK command [ {} ] with args:'.format(command_key)
    print('\n', '*' * len(run_logging_string), '\n', run_logging_string)
    for key, value in plink_args.items():
        print('--' + key + ' =', value)
    print()
    plink_command = 'plink '
    for arg, arg_value in plink_args.items():
        # print(arg, arg_value)
        # argument_value = getattr(plink_args, arg)
        if arg_value is not None:
            if arg_value != '':
                if 'bmerge' == arg:
                    arg_value = list(get_bed_bim_fam_from_bfile(arg_value).values())
                    # print(arg_value)
                    arg_value.sort()
                    arg_value = ' '.join(arg_value)
                elif 'bfile' == arg:
                    arg_value = '{} {}'.format(arg_value, '--make-bed')
                arg_as_plink_flag = '--{} {} '.format(arg, arg_value)
                plink_command += arg_as_plink_flag
            else:
                plink_command += '--{} '.format(arg)

    print(plink_command)
    try:
        subprocess.check_output(plink_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(logging.exception("Error running plink while [ {} ]".format(command_key)))
        print(e.output)


def validate_wrapper_args(args, parent_dir):
    if args.bfile == 'sample_data/dataset_sample' and ''.join(args.bmerge) == 'sample_data/hapmap_sample':
        args.bfile = os.path.join(parent_dir, args.bfile)
        args.bmerge = os.path.join(parent_dir, args.bmerge)
        args.out = os.path.join(parent_dir, args.out)

    # if args.make_bed is not None:
    #     args.make_bed = ''
    if args.noweb is not None:
        args.noweb = ''
    return args


def get_bed_bim_fam_from_bfile(bfile):
    # print('bfile', bfile)
    filenames_dict = dict()
    filenames_dict['bed'] = bfile + '.bed'
    filenames_dict['bim'] = bfile + '.bim'
    filenames_dict['fam'] = bfile + '.fam'
    return filenames_dict


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
    where each corresponding *.bed, *.bim, and *.fam must together on a line in that specific order. This function
    takes an input of a directory of files and returns a file output like the example above that will later be run
    through PLINK.
    :param input_files_directory:
    """
    temp_plink_input_filename = 'plink_input.txt' # this should later be deleted, once the PLINK run is done
    for dirpath, dirnames, filenames in os.walk(input_files_directory):
        print()