#!/usr/bin/env python


import sys
import os
from argparse import ArgumentParser


def parseArgs():
	parser = ArgumentParser(description='Extracts the content saved in '
	'<Analytes> nodes from a Bruker MALDI-TOF XML output file.'
	' Retains XML formatting.', add_help=False)
	req = parser.add_argument_group('Required')
	req.add_argument('-i', '--infile', required=True, metavar='FILE',
		help='input XML file')
	opt = parser.add_argument_group('Optional')
	opt.add_argument('-h', '--help', action='help',
		help='show this help message and exit')
	opt.add_argument('-o', '--outfile', metavar='FILE',
		default=None, help='output file [stdout]')
	return parser.parse_args()

def main():
	opt = parseArgs()
	fi  = os.path.abspath(os.path.expanduser(opt.infile))

	extrn = []
	fnd = False
	with open(fi, 'r') as ifh:
		for ln in ifh:
			if fnd:
				extrn.append(ln.rstrip())
			if ln.rstrip() == '<Analytes>':
				fnd = True
			elif ln.rstrip() == '</Analytes>':
				fnd = False
	if len(extrn) > 0:
		del extrn[-1]
	else:
		sys.exit('ERROR: <Analytes> absent from input file')

	if opt.outfile is None:
		for extracted in extrn:
			print extracted
	else:
		fo = os.path.abspath(os.path.expanduser(opt.outfile))
		with open(fo, 'w') as ofh:
			ofh.write('\n'.join(extrn))

if __name__ == '__main__':
	main()