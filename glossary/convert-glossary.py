#!/usr/bin/env python3

import csv

glossname = "UT22084-061-014-"

outfile = open('output.xml', 'w', encoding="utf8")

outfile.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")

with open("input.csv", "r", encoding="utf8") as ins:
    glosscsvreader = csv.reader(ins, delimiter=',', quotechar='"')
    glossidx = 0
    glossletters = 'init'
    outfile.write("<list>\n")
    for row in glosscsvreader:
        row[0] = row[0].strip()
        row[1] = row[1].strip()
        row[2] = row[2].strip()
        # remove BOM
        if row[0].startswith(u'\ufeff'):
            row[0] = row[0][1:]
        if row[0] == 'Tibetan':
            glossidx = 0
            if (glossletters == 'init'):
                glossletters = 'te'
            elif (glossletters == 'te'):
                glossletters = 'pe'
            elif (glossletters == 'pe'):
                glossletters = 'pl'
            continue
        glossidx = glossidx+1
        res = "    <item>\n        <gloss>\n            <term xml:id=\"%s%s%d\">%s</term>" % (glossname, glossletters, glossidx, row[2])
        if row[0]:
            boltn = row[0]
            if boltn[-1] != ' ':
               boltn += ' '
            res += "\n            <term xml:lang=\"Bo-Ltn\">%s</term>" % boltn
        if row[1]:
            res += "\n            <term xml:lang=\"Sa-Ltn\">%s</term>" % row[1]
        if row[3]:
            definition = row[3].strip()
            if definition == '-':
                definition = ''
            res += "\n            <term type=\"definition\">%s</term>" % definition
        if 4 in row and row[4]:
            if 5 in row and row[5]:
                row[4] += ', '+row[4]
            res += "\n            <term type=\"alternative\" xml:lang=\"eng\">%s</term>" % row[4]
        res += "\n        </gloss>\n    </item>\n"
        outfile.write(res)
    outfile.write("</list>\n")

outfile.close()
