#!/usr/bin/env python


import os
from argparse import ArgumentParser
from xml.etree import ElementTree


def parseArgs():
	parser = ArgumentParser(description='Summarizes Bruker MALDI-TOF XML '
	'output file into a tab-delimited format where each line is a separate '
	'isolate containing isolate IDs along with their corresponding molecular '
	'weights and peak intensities', add_help=False)
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
	ifh = os.path.abspath(os.path.expanduser(opt.infile))

	extrn = []
	tree  = ElementTree.parse(ifh)
	for s in tree.findall('Analytes'):
		sample = ''
		for a in s.findall('Analyte'):
			sample = 'CSID={}\tMALDI-UUID={}\t'.format(
				a.get('externId'), a.get('internId'))
			for l in a.findall('Peaklist'):
				sample += 'PeakIntensityScale={}\tUUID={}\t'.format(
					l.get('intensityScale'), l.get('uuid'))
				for peaks in l.findall('Peaks'):
					for p in peaks.findall('Peak'):
						sample += '({},{})\t'.format(
							p.get('mass'), p.get('intensity'))
			extrn.append(sample.rstrip())

	if opt.outfile is None:
		for extracted in extrn:
			print extracted
	else:
		fo = os.path.abspath(os.path.expanduser(opt.outfile))
		with open(fo, 'w') as ofh:
			ofh.write('\n'.join(extrn))

if __name__ == '__main__':
	main()