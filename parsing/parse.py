import sys
from itertools import islice

log = open('/Users/andreagarretto/GeneticAncestryTool/parsing/log.txt', 'r')
missnp = open('/Users/andreagarretto/GeneticAncestryTool/parsing/missnp.txt', 'a')

missnp.write('\n')
skipped = islice(log, 15, None) #start iterating after header
for line in skipped:
    id = line.split('rs',1)[1]  #gets the snp id
    id = id.strip('\n')
    id=id.strip("'.")
    missnp.write('rs' +id+'\n')  #append to missnp file
