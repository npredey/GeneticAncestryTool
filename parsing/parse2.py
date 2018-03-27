# remove . id's from bim file
import sys

bim = open('/Users/andreagarretto/GeneticAncestryTool/parsing/bim.txt', 'r')
edited_bim = open('/Users/andreagarretto/GeneticAncestryTool/parsing/edited_bim.bim', 'w')

def clean_bim(bimfile):
    for line in bim.readlines():
        l = line.split('\t')  #split by tabs
        if l[1] != '.':
            edited_bim.write(line)
