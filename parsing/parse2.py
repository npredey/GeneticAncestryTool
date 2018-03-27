# remove . id's from bim file
import sys

def clean_bim(bimfile):
    for line in bim.readlines():
        l = line.split('\t')  #split by tabs
        if l[1] != '.':
            edited_bim.write(line)
