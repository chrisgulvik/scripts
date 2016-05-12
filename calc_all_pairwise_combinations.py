#!/usr/bin/env python

import sys
import itertools


items = []
with open(sys.argv[1], 'r') as infile:
	for line in infile:
		items.append(line.split('\t')[0].rstrip('\n')) # only use 1st column data

unique_items = set() # discard duplicate tuples
for i in itertools.combinations(items, 2):
	if i[0] != i[1]:
		unique_items.add(i)
sorted_unique_items = sorted(unique_items, key=lambda tupl:tupl[0])
for u in sorted_unique_items:
	print '\t'.join(map(str, (u)))
print 'found {} unique combinations excluding self-to-self'.format(str(len(unique_items)))
