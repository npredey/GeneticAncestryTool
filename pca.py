import re
import subprocess


def create_pca_data(eigenvec_input_file, tg_ped_file, eigenvec_output_name):
    """

    :param tg_ped_file: Data from the thousand genome project that we will append the eigenvec_input data on
    population to.
    :param eigenvec_output_name: The name of the output eigenvec file we will perform pca on.
    :param eigenvec_input_file: The eigenvec file used to create the PCA data.
    :rtype: object
    """
    # f = open("/homes/hwheeler/Data/1000_Genomes_Ref_hg19/20130606_g1k.ped", "r")
    # f = open(tg_ped_file, "r")
    with open(tg_ped_file, 'r') as tg_ped_in:
        tg_data = tg_ped_in.readlines()
    population_dict = dict()

    # d[tupule(line)] = line
    for line in tg_data[1:]:
        # line=data
        # print(line)

        line_split = re.split('\t', line)
        # info=line.split('\t')
        population_dict[line_split[1]] = line_split[6]

    # e = open("/homes/kmunshi/plink.eigenvec", "r")
    with open(eigenvec_input_file, 'r') as eigenvec_in:
        eigenvec_in_data = eigenvec_in.readlines()

    # o=open("/homes/kmunshi/plink_output2.eigenvec", "w+")
    with open(eigenvec_output_name, 'w+') as eigenvec_out:
        for line in eigenvec_in_data:
            line_split = re.split(' ', line.strip())
            # print(line_split)
            # info = line.split('\t')
            if line_split[1] in population_dict.keys():
                line_split.append(population_dict[line_split[1]])
                eigenvec_out.write(' '.join(line_split) + '\n')
            else:
                line_split.append(" GWAS")
                eigenvec_out.write(' '.join(line_split) + '\n')


def plot_components(eigenvec_file):
    """
    Function to call R script to plot the data.
    :param eigenvec_file: The .eigenvec file that holds the components with population.
    """
    r_command = 'Rscript --vanilla plotting.R {}'.format(eigenvec_file, shell=True)
    subprocess.check_output(r_command)
