#!/usr/bin/env python3

import re

outfile = open('output.xml', 'w', encoding="utf8")

outfile.write("""<?xml-model href="../../../schema/84000-ODD.rnc" type="application/relax-ng-compact-syntax"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0">\n""")

lineNums = {
	1: 'title_bo',
	2: 'title_en',
	3: 'title_sk',
	4: 'longtitle_bo',
	5: 'longtitle_bo_ltn',
	6: 'longtitle_en',
	7: 'longtitle_sk',
	8: 'ref_biblScope',
	9: 'author',
	10: 'version_date'
}

def write_header(header_lines):
	with open("template.xml", "r", encoding="utf8") as inf:
		template = inf.read()
	linenum = 0
	args = {
		'title_bo': 'XXX',
		'title_en': 'XXX',
		'title_sk': 'XXX',
		'longtitle_bo': 'XXX',
		'longtitle_bo_ltn': 'XXX',
		'longtitle_en': 'XXX',
		'longtitle_sk': 'XXX',
		'translatorMain': 'XXX',
		'version': 'XXX',
		'date': 'XXX',
		'id': 'XXX',
		'ref': 'XXX',
		'biblScope': 'XXX'
	}
	for line in header_lines:
		line = re.sub(r'<(?:\/)*(hi|pb|p)([^>]*)(?:\/)*>', '', line)
		line = re.sub(r'\s*\n\s*', ' ', line)
		line = line.strip()
		if line == '' or line == 'insert CC logo':
			continue
		linenum = linenum+1
		if linenum in lineNums:
			arg = lineNums[linenum]
			if arg == 'ref_biblScope':
				splitted = line.split(',',1)
				args['ref'] = splitted[0].strip()
				args['biblScope'] = splitted[1].strip()
			elif arg == 'version_date':
				splitted = line.split(',',1)
				args['version'] = splitted[0].strip()
				args['date'] = splitted[1].strip()
			elif arg == 'author':
				splitted = line.split('<lb/>',1)
				line = splitted[0]
				splitted = line.split('by',1)
				line = splitted[1].strip()
				args['translatorMain'] = line
			else:
				args[arg] = line
	for k, v in args.items():
		template = template.replace('__'+k+'__', v)
	outfile.write(template)

with open("input.xml", "r", encoding="utf8") as ins:
	header_lines = []
	in_header = False
	after_header = False
	unfinished_line = False
	for line in ins:
		stripped_line = line.strip()
		if stripped_line == '<body>':
			in_header = True
			continue
		elif stripped_line == '<p>Contents</p>':
			in_header = False
			after_header = True
			write_header(header_lines)
		if in_header:
			if unfinished_line:
				header_lines[-1] = header_lines[-1]+line
			else:
				header_lines.append(line)
			if stripped_line.endswith("</p>"):
				unfinished_line = False
			else:
				unfinished_line = True
		elif after_header:
			line = line.replace('&lt;', '<').replace('&gt;', '>')
			line = re.sub(r'\sxml:space="[^"]*"', '', line)
			outfile.write(line)

outfile.close()