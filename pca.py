import re


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

    # o=open("/homes/kmunshi/plink_output.eigenvec", "w+")
    with open(eigenvec_output_name, 'w+') as eigenvec_out:
        for line in eigenvec_in_data:
            line_split = re.split(' ', line.strip())
            # print(line_split)
            # info = line.split('\t')
            if line_split[1] in population_dict.keys():
                line_split.append(population_dict[line_split[1]])
                eigenvec_out.write(' '.join(line_split) + '\n')


def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np

    if type not in ('bright', 'soft'):
        print('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap
