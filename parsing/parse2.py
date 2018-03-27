# remove . id's from bim file
import sys

def clean_bim(bimfile,dataset,snp_ref):
    plink --bimfile dataset --snp .  #remove . id's from bimfile

    snp_dict={}
    for line in snp_ref.readlines():
        if '#' in line: #if it's the header row
            continue   #skip
        row = line.split(',')
        snp_dict[row[1]] = row[2]    #add snpID and rsID to dictionary

    lines = bim.readlines()
    f=open('snpID.txt','a')  #file to write out snpIDs that dont have an rsID
    for line in lines:
        l = line.split('\t')  #split by tabs
        if l[1].startswith('rs') == False:  #if not an rs id
            if (l[1] in snp_dict.keys() and snp_dict[l[1]] != '---') or l[1] not in snp_dict.keys():
                f.write(l[1]+'\n')
            else: #replace snpID with rsID
                line[1]= snp_dict[l[1]]
