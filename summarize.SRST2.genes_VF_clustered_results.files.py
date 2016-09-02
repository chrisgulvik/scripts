#!/usr/bin/env python


import pandas as pd
import sys
from argparse import ArgumentParser
from Bio import SeqIO

def parseArgs():
	parser = ArgumentParser(
		description='Summarizes SRST2 genes output files where all genes '
		'from the database used are listed as present or not as well as an '
		'abbreviated output file where only genes present in at least one '
		'sample are listed')
	parser.add_argument('-db', '--database', required=True,
		help='multi-FastA file used as a database to generate clustered '
		'results files')
	parser.add_argument('-i', '--infiles', required=True,
		help='comma-separated list of genes_clustered_results files from '
		'SRST2; use \"-\" to read from stdin, e.g., '
		'from `ls *__genes__*VF_clustered__results.txt | tr \'\n\' \',\' | '
		'sed \'s/,$//g\' |`')
	parser.add_argument('-o', '--outbase', default='Summary_genes',
		help='output file base where \'_full.tab\' and \'_abbreviated.tab\' '
		'are appended [./Summary_genes]')
	return parser.parse_args()

def main():
	args = parseArgs()

	# Parse all gene names in db
	db_genes = []
	vf_db = SeqIO.parse(args.database, 'fasta')
	for record in vf_db:
		db_genes.append(record.description.split('__')[1])

	# Handle input filenames
	if args.infiles == '-':
		input_files = str(sys.stdin.readlines()).lstrip('\'[').rstrip(']\'').split(',')
	else:
		input_files = args.infiles.split(',')
	if len(input_files) < 2:
		sys.exit('ERROR: more than one file must be given to summarize')

	with open(args.outbase + '_full.tab', 'w') as o:
		# Output header
		o.write('Sample\t')
		for vf in db_genes:
			o.write(vf + '\t')
		o.write('\n')

		# Output summary info from each input file
		for infile in input_files:
			with open(infile) as i:
				hits = {}
				for s in i.readlines()[1].rstrip().split('\t'):
					hits[s.split('_')[0]] = s
				o.write('{}\t'.format(infile.split('__')[0]))
				for vf in db_genes:
					if vf in hits:
						o.write(hits[vf] + '\t')
					else:
						o.write('-\t')
				o.write('\n')

	# Output summary where at least one gene is found in the sample set
	d = pd.read_table(args.outbase + '_full.tab', dtype=str)
	d = d.loc[:, (d != '-').sum() > 0]
	d.to_csv(args.outbase + '_abbreviated.tab', index=False, sep='\t',
		encoding='utf-8')

	print 'Summarized {} files...'.format(len(input_files))

if __name__ == '__main__':
	main()
