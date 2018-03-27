# add bad id's from log to missnp file

import sys
from itertools import islice

log = open('/Users/andreagarretto/GeneticAncestryTool/parsing/log.txt', 'r')
missnp = open('/Users/andreagarretto/GeneticAncestryTool/parsing/missnp.txt', 'a')

def merge_log_to_missnp(logfile,missnpfile):
    missnpfile.write('\n')
    skipped = islice(logfile, 15, None) #start iterating after header
    for line in skipped:
        id = line.split('rs',1)[1]  #gets the snp id
        id = id.strip('\n')
        id=id.strip("'.")
        missnpfile.write('rs' +id+'\n')  #append to missnp file
