#!/usr/bin/env python


from argparse import ArgumentParser

def parseArgs():
	parser = ArgumentParser(description='Given File 1, swap a column '
		'with key-values from File 2. Prints to stdout.', add_help=False)
	req = parser.add_argument_group('Required')
	req.add_argument('-1', '--file1', required=True, metavar='FILE',
		help='TSV file to parse')
	req.add_argument('-2', '--file2', required=True, metavar='FILE',
		help='TSV file where 1st col is key to find and 2nd col is value to'
		' replace with')
	opt = parser.add_argument_group('Optional')
	opt.add_argument('-h', '--help', action='help',
		help='show this help message and exit')
	opt.add_argument('-ih1', '--ignore-header1', default=False,
		action='store_true', help='ignores first row (header) line in File 1')
	opt.add_argument('-ih2', '--ignore-header2', default=False,
		action='store_true', help='ignores first row (header) line in File 2')
	opt.add_argument('-c', '--col', metavar='INT', default='1', type=int,
		help='column number in File 1 to swap key-value pairs [1]')
	return parser.parse_args()

def main():
	opts = parseArgs()
	f1 = os.path.abspath(opts.file1)
	f2 = os.path.abspath(opts.file2)

	d = {}
	with open(f2, 'rU') as ifh2:
		if opts.ignore_header2:
			next(ifh2)
		for line in ifh2:
			ln = line.rstrip('\n').split('\t')
			d[ln[0]] = ln[1]
	d['NULL'] = '-' #rid of ugly NULL from SQL db, replace with hyphen

	with open(f1, 'rU') as ifh1:
		if opts.ignore_header1:
			next(ifh1)
		for line in ifh1:
			ln = line.rstrip('\n').split('\t')
			v = d[ln[opts.col - 1]]
			ln[opts.col - 1] = v
			print '\t'.join(ln)

if __name__ == '__main__':
	main()