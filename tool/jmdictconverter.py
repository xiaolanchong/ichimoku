# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET

def getEntities(fileName):
    entities = {}
    with open(fileName, encoding='utf-8') as xml:
        for line in xml.readlines():
            m = re.match('<!ENTITY\s+(\S+)\s+"(.+)">', line, re.S)
            if m:
                entities[m.groups()[1]] = m.groups()[0]
    return entities

def dumpDictionary(items):
    with open('jdict_out.txt', 'w', encoding='utf-8') as outFile:
        for item in items:
            s = '{0:<10} {1} ({2}) {3}\n'.format(item[0], item[1], ','.join(item[2]), '/'.join(item[3]))
            outFile.write(s)

def getMixedRecords(kanjiKanaRecords):
    if len(kanjiKanaRecords) == 1:
        return [(kanjiKanaRecords[0], kanjiKanaRecords[0])]
    else:
        return [(kanjiKanaRecords[i], kanjiKanaRecords[-1]) for i in range(0, len(kanjiKanaRecords) - 1)]

def main():
    fileName = 'JMdict_e.xml'
    #fileName = 'test.xml'
    entities = getEntities(fileName)

    parser = ET.XMLParser(target=ET.TreeBuilder())
    tree = ET.parse(fileName, parser)
    root = tree.getroot()
    items = []
    for entry in root.findall('entry')[1:1000]:
        kanjiKanaNames = []
        for kanji in entry.findall('k_ele/keb'):
            kanjiKanaNames.append(kanji.text)
        kanaItems = entry.findall('r_ele/reb')
        for kana in kanaItems:
            kanjiKanaNames.append(kana.text)
        records = getMixedRecords(kanjiKanaNames)

        pos = []
        for partOfSpeech in entry.findall('sense/pos'):
            pos.append(entities[partOfSpeech.text])

        translations = []
        for meaning in entry.findall('sense/gloss'):
            translations.append(meaning.text)

        for name, reading in records:
            items.append((name, reading, translations, meaning))
    dumpDictionary(items)

if __name__ == '__main__':
    main()