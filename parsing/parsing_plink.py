#!/usr/bin/env python
import sys
import os
import re
import constants.filename_constants as constants
from wrapper.wrapper_util import get_root_path, get_filename

sys.path.append(os.path.dirname(os.getcwd()))

import wrapper.wrapper_util


def merge_log_to_missnp(output_file):
    """
    Takes in a .log file and a .missnp file and merges them together. There should be a separate output file of the
    two files merged together.
    :return: The name of the merged files, or an empty string if the log file and a .missnp file is not present.
    :rtype: String
    :param output_file: The output flag passed in as a command line argument.
    """
    print(constants.MERGED_LOG_MISSNP)
    output_file_root_dir = get_root_path(output_file)
    output_file_name = get_filename(output_file)

    input_logfile = '{}.log'.format(output_file).replace('//', '/')
    print('this is the input logfile', input_logfile)
    input_missnp = '{}.missnp'.format(output_file)
    merged_missnp_output = '{}_{}'.format(output_file, 'MERGED_LOG_MISSNP.txt')
    merged_missnp_output_lines = list()
    missing_logfile = False
    missing_missnp_file = False

    try:
        with open(input_missnp, 'r') as missnp:
            merged_missnp_output_lines += missnp.readlines()
    except FileNotFoundError:
        missing_missnp_file = True
        print('.missnp file [ {} ] does not exist. Excluding from merge...'.format(input_missnp))

    # missnpfile.write('\n')
    # A good way to test this code is to call these functions within this file with hardcoded file paths for the time
    # being.
    try:
        with open(input_logfile, 'r') as logfile_in:
            for line in logfile_in:
                if line.startswith('Warning:'):
                    rs_id = re.search('rs[0-9]+', line)  # regular expression to grab rsID's
                    if rs_id:
                        rs_id = rs_id.group(0)
                        # id = line.split('rs', 1)[1]  # gets the snp id
                        rs_id = rs_id.strip('\n')
                        rs_id = rs_id.strip("'.")
                        merged_missnp_output_lines.append(rs_id + '\n')  # append to missnp file
    except FileNotFoundError:
        print('Log file [ {} ] does not exist. '.format(input_logfile))
        missing_logfile = True

    if (missing_missnp_file and missing_logfile) or len(merged_missnp_output_lines) < 1:
        return ''
    else:
        with open(merged_missnp_output, 'w+') as merged_output:
                for line in merged_missnp_output_lines:
                    merged_output.write(line)
        return merged_missnp_output


def remove_dots_from_dataset(dataset):
    """
    Removes '.' from the binary file input.
    :rtype: str
    :param dataset: The path to the .bed .bim .fam files whose '.' as rsIDs to be removed.
    """
    root_path = wrapper.wrapper_util.get_root_path(dataset)
    dataset_filename = wrapper.wrapper_util.get_filename(dataset)

    output_file = '{}{}_{}'.format(root_path, dataset_filename, 'NO_DOTS')
    temp_snpfile = 'dotfile_temp.txt'
    temp_file = open(temp_snpfile, 'w+')
    temp_file.write('.')
    temp_file.close()

    # remove_dotIDs = {'bfile': dataset, 'exclude': temp_snpfile, 'out': output_file, 'make-bed': ''}
    remove_dotIDs = {'bfile': dataset, 'exclude': temp_snpfile, 'out': output_file}
    wrapper.wrapper_util.call_plink(remove_dotIDs, command_key='Exclude . SNPs')
    os.remove(temp_snpfile)
    return output_file


def clean_bim(bimfile_input, snp_ref):
    """
    "Cleans" a .bim file by swapping
    :param bimfile_input: The .bim file to be cleaned.
    :param dataset: The binary file as a parameter from the command line argument.
    :param snp_ref: The SNP reference file that converts SNP ID's to rsID's
    """
    # plink --bimfile dataset --snp .  #remove . id's from bimfile
    # temp_snpfile = 'clean_bim_temp.txt'
    # temp_file = open(temp_snpfile, 'w+')
    # temp_file.write('.')
    # temp_file.close()
    #
    # remove_dotIDs = {'bfile': dataset, 'exclude': temp_snpfile, 'out': 'dataset_out', 'make-bed': ''}
    # wrapper.wrapper_util.call_plink(remove_dotIDs, command_key='Exclude . SNPs')
    # os.remove(temp_snpfile)
    snp_dict = dict()

    if snp_ref is not None:
        snp_ref_r = open(snp_ref, 'r')
        snp_ref_lines = snp_ref_r.readlines()
        for line in snp_ref_lines:
            if '#' in line:  # if it's the header row
                continue
            row = line.split(',')
            snp_dict[row[1]] = row[2]  # add snpID and rsID to dictionary

        bimfile_input_r = open(bimfile_input, 'r')
        bimfile_lines = bimfile_input_r.readlines()
        good_snpID_output_file = open('snpID.txt', 'a')  # file to write out snpIDs that dont have an rsID

        for line in bimfile_lines:
            split_line = line.split('\t')  # split by tabs
            if not split_line[1].startswith('rs'):  # if not an rs id
                if (split_line[1] in snp_dict.keys() and snp_dict[split_line[1]] != '---') \
                        or split_line[1] not in snp_dict.keys():
                    good_snpID_output_file.write(split_line[1] + '\n')
                else:  # replace snpID with rsID
                    split_line[1] = snp_dict[split_line[1]]

        good_snpID_output_file.close()  # https://stackoverflow.com/questions/7395542/is-explicitly-closing-files-important

#
# bimfile_input = '/homes/hwheeler/Data/example_PLINK_files/dataset1.bim'
# dataset = '/homes/hwheeler/Data/example_PLINK_files/dataset1'
# snp_ref = '/homes/hwheeler/Data/example_PLINK_files/GenomeWideSNP_6.na35.annot.csv'
#
# clean_bim(bimfile_input, dataset, snp_ref)
# merge_log_to_missnp('/homes/agarretto/results_dset1_phase1_all/merged_data')
