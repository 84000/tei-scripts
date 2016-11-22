#!/usr/bin/env python3

import re

outfile = open('output.xml', 'w', encoding="utf8")

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
	'biblScope': 'XXX',
	'summary': '',
	'acknowledgments': '',
	'introduction': '',
	'body': '',
	'bibliography': '',
	'glossary': 'XXX'
}

def fill_header_args(header_lines):
	global args
	linenum = 0
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

with open("input.xml", "r", encoding="utf8") as ins:
	header_lines = []
	step = 'init'
	substep = 'body'
	unfinished_line = False
	for line in ins:
		line = line.replace('&lt;', '<').replace('&gt;', '>')
		line = re.sub(r'\[F\. ([^\]]+)\]', r'<ref cRef="\1"/>', line)
		line = line.replace('<p><milestone unit="chunk"/>', '<milestone unit="chunk"/>\n                    <p>')
		line = line.replace('<hi rend="endnote_reference"><note place="end"><p rend="endnote text">','<note place="end">')
		line = line.replace('</p></note></hi>','</note>')
		line = re.sub(r'\sxml:space="[^"]*"', '', line)
		stripped_line = line.strip()
		if stripped_line == '<body>':
			step = 'header'
			continue
		elif stripped_line == '<p>Contents</p>':
			step = 'toc'
			fill_header_args(header_lines)
			header_lines = None
		if step == 'header':
			if unfinished_line:
				header_lines[-1] = header_lines[-1]+line
			else:
				header_lines.append(line)
			if stripped_line.endswith("</p>"):
				unfinished_line = False
			else:
				unfinished_line = True
		elif step == 'toc':
			if stripped_line == '<p><pb/></p>':
				step = 'aftertoc'
		elif step == 'aftertoc':
			no_tag_line = stripped_line.replace('<p>', '').replace('</p>', '').replace('<pb/>', '').strip()
			if no_tag_line == 'Summary':
				substep = 'summary'
			elif no_tag_line == 'Acknowledgments':
				substep = 'acknowledgments'
			elif no_tag_line == 'Introduction':
				substep = 'introduction'
			elif no_tag_line == '<hi rend="allcaps">The Translation</hi>':
				substep = 'body'
			elif no_tag_line == 'Bibliography':
				substep = 'bibliography'
			elif no_tag_line == '</body>':
				step = 'ignore'
			else:
				args[substep] = args[substep]+line
	with open("template.xml", "r", encoding="utf8") as inf:
		template = inf.read()
	for k, v in args.items():
		template = template.replace('__'+k+'__', v)
	outfile.write(template)

outfile.close()