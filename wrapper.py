import argparse
import sys
import parsing_plink
from util import *
import logging


def application():
    """
    The starting point for the GeneticAncestryTool.
    Many of the commands will, and should probably, be the same as PLINK (documentation:
    http://zzz.bwh.harvard.edu/plink/reference.shtml)
    """
    PARENT_DIR = os.path.abspath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser()

    parser.add_argument('--bfile', help='Specify .bed, .bim and .fam.', type=str, required=True)
    parser.add_argument('--bmerge', help='Merge in a binary fileset.',
                        type=str)  # '*'= greater than or equal to 0 args, '+'= more than or equal to 1 args
    # parser.add_argument('--make-bed', nargs='*', help='Make .bed, .fam and .bim.', type=bool)
    parser.add_argument('--out', help='Specify output root filename.', type=str, required=True)
    parser.add_argument('--snp-ref', help='Specify snp reference file to convert data from SNP IDs to rsIDs.', type=str)
    parser.add_argument('--noweb', help='PLINK arg to run without the internet.', action='store_true')
    parser.add_argument('--n', help='Flag for extracting a set amount of rsIDs from the dataset. Use if the files are '
                                    'large or for benchmarking/testing purposes.', type=int, default=0)

    args = parser.parse_args()
    ORIGINAL_BFILE = args.bfile
    input_root_dir = get_root_path(args.bfile)
    if len(sys.argv) == 1:
        print(parser.print_help())
        sys.exit()

    args = validate_wrapper_args(args, PARENT_DIR)
    args_dict = args.__dict__

    input_binary_files = get_bed_bim_fam_from_bfile(args.bfile)
    # print(input_binary_files)

    if args.snp_ref:
        print('swapping')

    logging.log(logging.INFO, "Extracting only rsID's from [ {} ] files\n".format(args.bfile))
    bfile_only_rsID = parsing_plink.get_rsIDs_from_dataset(args.bfile, args.n)
    bmerge_only_rsID = parsing_plink.get_rsIDs_from_dataset(args.bmerge, args.n)

    only_rsID_binary_files = get_bed_bim_fam_from_bfile(bfile_only_rsID)
    logging.log(logging.INFO, "Cleaning bim file {}.bim\n".format(args.bfile))
    # parsing_plink.clean_bim(only_rsID_binary_files['bim'], args.snp_ref)

    args_dict['bfile'] = bfile_only_rsID
    args_dict['bmerge'] = bmerge_only_rsID

    call_plink(plink_args=args_dict, command_key='First Merge after clean and extracting rsIDs')
    inital_run_logfile = "{}.log".format(args.out)
    initial_run_missnp = "{}.missnp".format(args.out)

    print("Merging initial .log file: [ {} ] with .missnip file: [ {} ]\n".format(inital_run_logfile,
                                                                                  initial_run_missnp))

    # args_out_full_path = '{}{}'.format(get_root_path(args.bfile), args.out)
    merged_missnp_log_filepath = parsing_plink.merge_log_to_missnp(args.out)

    # plink --bfile 1kg_phase1_all --exclude dset3_merged-merge.missnp --make-bed --out 1kg_phase1_all_dset3_tmp

    rsID_only_bfile_output_name_after_exclude = '{}_{}'.format(bfile_only_rsID, 'exc_missnp_log')
    hapmap_output_after_exclude = '{}_{}'.format(args.bmerge, 'exc_missnp_log')
    if merged_missnp_log_filepath:  # output name is blank so we will not exclude it from the files
        exclude_merged_missnp_log_args = {
            'bfile': args.bfile,
            'exclude': merged_missnp_log_filepath,
            # 'make-bed': '',
            'out': rsID_only_bfile_output_name_after_exclude
        }

        call_plink(plink_args=exclude_merged_missnp_log_args, command_key='Excluding merged log and *.missnp file from '
                                                                          'dataset')
        exclude_merged_missnp_log_args['bfile'] = args.bmerge
        exclude_merged_missnp_log_args['out'] = hapmap_output_after_exclude
        call_plink(plink_args=exclude_merged_missnp_log_args, command_key='Excluding merged log and *.missnp file from '
                                                                          'HapMap')

        # --bfile dataset3_tmp --bmerge 1kg_phase1_all_dset3_tmp --make-bed --out dset3_merged_tmp
        final_merge_args = {
            'bfile': rsID_only_bfile_output_name_after_exclude,
            'bmerge': hapmap_output_after_exclude,
            # 'make-bed': '',
            'out': args.out
        }
        call_plink(final_merge_args, 'Performing final merge of dataset [ {} ] and HapMap [ {} ].'.format(args.bfile,
                                                                                                          args.bmerge))
    merged_file_name = args.out

    # plink --bfile nameoffiles --maf 0.05 --make-bed

    merged_file_name_aftermaf = '{}_MAF'.format(merged_file_name)
    maf_args = {
        'bfile': merged_file_name,
        'maf': '0.05',
        'out': merged_file_name,
    }
    call_plink(maf_args, command_key='Running multiple allele frequency on dataset [ {} ]'.format(merged_file_name))

    # plink --bfile nameoffiles --indep-pairwise 50 5 0.3 --out outputname

    after_maf_ld_pruning = '{}_PRUNED'.format(merged_file_name_aftermaf)
    ld_prune_args = {
        'bfile': merged_file_name,
        'indep-pairwise': '50 5 0.3',
        'out': merged_file_name
    }
    call_plink(ld_prune_args, command_key='Running LD Pruning on dataset [ {} ]'.format(merged_file_name_aftermaf))
    # plink --bfile nameoffiles --extract outputname.prune.in --out newoutputname -make--bed
    # after_prune_pca = '{}_PCA'.format(ORIGINAL_BFILE)
    extracted_pruned = args.out
    prune_in_file = '{}.prune.in'.format(args.out)

    extract_args = {
        'bfile': merged_file_name,
        'extract': prune_in_file,
        'out': merged_file_name
    }
    call_plink(extract_args, command_key='Extracting pruned data from dataset [ {} ]'.format(args.bfile))

    # plink --bfile extracted_file --pca --out pca_file

    pca_file = '{}_PCA'.format(ORIGINAL_BFILE)
    extract_args = {
        'bfile': merged_file_name,
        'pca': '',
        'out': pca_file
    }
    call_plink(extract_args, command_key='Running PCA on dataset [ {} ]'.format(extracted_pruned))
