# -*- coding: utf-8 -*-
# part of speech mapper

import re
import sys
import os.path

sys.path.append(os.path.abspath('..'))
from mecab.dictionary import Dictionary
from textproc.jdictprocessor import JDictProcessor

allPartsOfSpeech = \
"""
adj-f, adj-i, adj-ku, adj-na, adj-nari, adj-no,
adj-pn, adj-shiku, adj-t, adv, adv-to, aux, aux-adj, aux-v,
conj, ctr, int, n, n-adv, n-pref, n-suf, n-t, num, on-mim,
pn, pref, prt, suf, v1, v2a-s, v2h-s, v2r-s, v2y-s, v4b, v4h,
v4k, v4r, v5aru, v5b, v5g, v5k, v5k-s, v5m, v5n, v5r, v5r-i,
v5s, v5t, v5u, v5u-s, vi, vk, vn, vr, vs, vs-c, vs-i, vs-s, vt, vz
"""
allPartsOfSpeech = [ a.strip() for a in allPartsOfSpeech.split(',')]
#print(allPartsOfSpeech)

def getEntryAttributes(entry):
    proc = JDictProcessor()
    return proc.getWordAttributes(entry)

def isPartOfSpeech(dictionary, word, posId):
    return posId in set(getPartOfSpeech(dictionary, word))

def getPartOfSpeech(dictionary, word):
    try:
        res = dictionary.exactMatchSearch(word)
    except UnicodeEncodeError as e:
        #print(word, e)
        return set([])
    if res is None:
        return set([])
    else:
        return set([token.partOfSpeechId for token in res])

def equalWords(entry1, entry2):
    entry1 = entry1.split('|||')[2]
    entry2 = entry2.split('|||')[2]
    #completely equal ?
    if entry1 == entry2:
        return True
    # one is contained into the other?
    if entry1.find(entry2) != -1 or entry2.find(entry1) != -1:
        return True
    # the same parts of speech
    pos1 = getEntryAttributes(entry1)
    pos2 = getEntryAttributes(entry2)
    if pos1.intersection(allPartsOfSpeech) == pos2.intersection(allPartsOfSpeech):
        return True
    return False

def getRecords():
    dictionary = Dictionary(os.path.join(os.path.abspath('..'), 'data', 'sys.zip'))
    with open('../data/dict.txt', 'r', encoding='utf-8') as f:
     #   posSet = set()
        overallDict = {}
        prevLine = ''
        for line in f.readlines():
            if prevLine == line.strip():
                continue
            line = line.strip()
            prev = line
            tokens = line.split('|||')
            entry = tokens[2]
            if len(tokens[0]):
                #overallDict[tokens[0]] = 1 + overallDict.get(tokens[0], 0)
                zzz = overallDict.get(tokens[0], [])
                zzz.append(line)
                overallDict[tokens[0]] = zzz
            elif len(tokens[1]):
                #overallDict[tokens[1]] = 1 + overallDict.get(tokens[1], 0)
                zzz = overallDict.get(tokens[1], [])
                zzz.append(line)
                overallDict[tokens[1]] = zzz
        #dumpBinaryHomonyms(overallDict)
        #dumpTernaryHomonyms(overallDict)
        dumpNOrderHomonyms(overallDict, 4)
        dumpNOrderHomonyms(overallDict, 5)
        dumpNOrderHomonyms(overallDict, 6)

def dumpHomonymNumber(overallDict):
    wordNumber = {}
    for k, v in overallDict.items():
        wordNumber[len(v)] = 1 + wordNumber.get(len(v), 0)
    print(wordNumber)

def dumpBinaryHomonyms(overallDict):
    with open('dict_2homonyms.txt', 'w', encoding='utf-8') as of:
        for k, v in overallDict.items():
            if len(v) == 2 and not equalWords(v[0], v[1]):
                for line in v:
                    of.write(line + '\n')

def dumpNOrderHomonyms(overallDict, grade):
    with open('dict_{0}homonyms.txt'.format(grade), 'w', encoding='utf-8') as of:
        for k, v in overallDict.items():
            if len(v) == grade: # and not equalWords(v[0], v[1]):
                for line in v:
                    of.write(line + '\n')



def getAttributeVector(attrSet):
    return [ 1 if a in attrSet else 0 for a in allPartsOfSpeech]

def tryAddWord(tokens, dictionary, wordsProcessed, attributesWithPos):
    posSet = set()
    if len(tokens[0]):
        if tokens[0] not in wordsProcessed:
            wordsProcessed.add(tokens[0])
            posSet = getPartOfSpeech(dictionary, tokens[0])
        else:
            return
    elif len(posSet) == 0 and len(tokens[1]): # and isPartOfSpeech(dictionary, tokens[1], posId):
        if tokens[1] not in wordsProcessed:
            wordsProcessed.add(tokens[1])
            posSet = getPartOfSpeech(dictionary, tokens[1])
        else:
            return
    if len(posSet) != 1:
        m = re.match('(.+?)\s*/\(.+', tokens[2], re.S)
        if m:
            posSet = [1] #getPartOfSpeech(dictionary, m.groups()[0])
    else:
        attributes = getEntryAttributes(tokens[2])
        attributesWithPos.append([posSet.pop()] + getAttributeVector(attributes))

def getAttributesOfKnownWords():
    dictionary = Dictionary(os.path.join(os.path.abspath('..'), 'data', 'sys.zip'))
    with open('../data/dict.txt', 'r', encoding='utf-8') as f:
       wordsProcessed = set()
       attributesWithPos = []
       for line in f.readlines():
            tokens = line.split('|||')
            tryAddWord(tokens, dictionary, wordsProcessed, attributesWithPos)
       print(len(attributesWithPos))
       with open('../data/posToAttributes.txt', 'w') as outFile:
          z = ', '.join(allPartsOfSpeech)
          outFile.write('; ' + z + '\n')
          for line in attributesWithPos:
            z = ','.join(map(lambda x: str(x), line))
            outFile.write(z + '\n')

def getWordPoS(word):
    #dictionary = Dictionary(os.path.join(os.path.abspath('..'), 'data', 'sys.zip'))
    res = ''
    with open('../data/dict.txt', 'r', encoding='utf-8') as f:
       wordsProcessed = set()
       attributesWithPos = []
       printed = False
       for line in f.readlines():
            tokens = line.split('|||')
            attributes = set()
            if tokens[0] == word:
                attributes = getEntryAttributes(tokens[2])
            if tokens[1] == word and len(tokens[0]) == 0:
                attributes = getEntryAttributes(tokens[2])
            if len(attributes) != 0:
                res += str(attributes) + ' ' + str(tokens[2].strip()) + '\n'
    return res

advContent = \
"""
"""

def getParticlePoS():
    parentDir = r'c:\Program Files (x86)\Anki\mecab\dic\ipadic'
    #parentDir = r'c:\project\github\python\ichimoku\testdata'
    particleName = 'adj.csv'
    out = ''
    with open(os.path.join(parentDir, particleName), 'r', encoding='shift_jis') as f: #encoding='shift_jis') as f:
        for line in f.readlines()[1000]:
            tokens = line.split(',')
            res = getWordPoS(tokens[0])
            if len(res):
                out += str(tokens[0]) + '\n'
                out += res
##    start = 0
##    while(True):
##        p = advContent.find('\n', start)
##        if p >= 0:
##            line = advContent[start:p]
##            start = p + 1
##            if len(line) == 0:
##                continue
##            tokens = line.split(',')
##            res = getWordPoS(tokens[0])
##            if len(res):
##                out += str(tokens[0]) + '\n'
##                out += res
##        else:
##            break
    open('../testdata/pos_out_adj.txt', 'w', encoding='utf-8').write(out)

def main():
    #getRecords()
    #getAttributesOfKnownWords()
    #getWordPoS('た')
    getParticlePoS()

main()

