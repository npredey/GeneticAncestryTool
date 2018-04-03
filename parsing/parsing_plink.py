#!/usr/bin/env python




def merge_log_to_missnp(logfile, missnpfile):
    """
    Takes in a .log file and a .missnp file and merges them together. There should be a separate output file of the
    two files merged together.
    :rtype: String: Filename of the merged log and missnp file.
    :param logfile:
    :param missnpfile:
    """
    missnpfile.write('\n')
    # A good way to test this code is to call these functions within this file with hardcoded file paths for the time
    # being.
    for line in logfile:
        if line.startswith('Warning:'):
            id = line.split('rs', 1)[1]  # gets the snp id
            id = id.strip('\n')
            id = id.strip("'.")
            missnpfile.write('rs' + id + '\n')  # append to missnp file


def clean_bim(bimfile_input, dataset, snp_ref):
    # plink --bimfile dataset --snp .  #remove . id's from bimfile

    snp_dict = {}
    for line in snp_ref.readlines():
        if '#' in line:  # if it's the header row
            continue
        row = line.split(',')
        snp_dict[row[1]] = row[2]  # add snpID and rsID to dictionary

    bimfile_lines = bimfile_input.readlines()
    good_snpID_output_file = open('snpID.txt', 'a')  # file to write out snpIDs that dont have an rsID

    for line in bimfile_lines:
        split_line = line.split('\t')  # split by tabs
        if not split_line[1].startswith('rs'):  # if not an rs id
            if (split_line[1] in snp_dict.keys() and snp_dict[split_line[1]] != '---') or split_line[1] not in snp_dict.keys():
                good_snpID_output_file.write(split_line[1] + '\n')
            else:  # replace snpID with rsID
                line[1] = snp_dict[split_line[1]]

    good_snpID_output_file.close()  # https://stackoverflow.com/questions/7395542/is-explicitly-closing-files-important
