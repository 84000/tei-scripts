#!/usr/bin/env python3

import xml.etree.ElementTree as etree

glossname = "UT22084-061-014-"

tree = etree.parse('input.xml')
root = tree.getroot()
body = root.find('{http://www.tei-c.org/ns/1.0}text').find('{http://www.tei-c.org/ns/1.0}body')

outfile = open('output.xml', 'w', encoding="utf8")
outfile.write("""<?xml version="1.0" encoding="UTF-8"?>\n<list>\n""")

# ugliness
def getCellText(element):
    baseStr = "".join( [ element.text ] + [ etree.tostring(e, encoding="utf8").decode("utf-8") for e in element.getchildren() ] )
    baseStr = baseStr.replace('ns0:', '').replace('xmlns:ns0="http://www.tei-c.org/ns/1.0" ', '')
    baseStr = baseStr.replace("<?xml version='1.0' encoding='utf8'?>\n", '')
    return baseStr

glossletters = 'init'

for table in body.findall('{http://www.tei-c.org/ns/1.0}table'):
    for row in table:
        print(row.tag)
        if row.tag == '{http://www.tei-c.org/ns/1.0}head':
            tag = row.text
            glossletters = tag.lower()[:2]
            continue
        num = int(row.attrib['n'])
        res = "    <item>\n        <gloss>\n            <term xml:id=\"%s%s%d\">%s</term>" % (glossname, glossletters, num, getCellText(row[2]))
        if row[0].text:
            boltn = getCellText(row[0])
            if boltn[-1] != ' ':
               boltn += ' '
            res += "\n            <term xml:lang=\"Bo-Ltn\">%s</term>" % boltn
        if row[1].text:
            res += "\n            <term xml:lang=\"Sa-Ltn\">%s</term>" % getCellText(row[1])
        if len(row) > 3 and row[3].text:
            definition = getCellText(row[3]).strip()
            if definition == '-':
                definition = ''
            res += "\n            <term type=\"definition\">%s</term>" % definition
        if  len(row) > 4 and row[4].text:
            alt = getCellText(row[4])
            if  len(row) > 5 and row[5].text:
                alt += ', '+getCellText(row[5])
            res += "\n            <term type=\"alternative\" xml:lang=\"eng\">%s</term>" % alt
        res += "\n        </gloss>\n    </item>\n"
        outfile.write(res)
outfile.write("</list>\n")
outfile.close()