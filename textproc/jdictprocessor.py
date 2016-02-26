# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from .wordmapper import WordMapper
import mecab.partofspeech as PoS
from mecab.utils import isPy2
from . import jcconv_3x as jcconv
from .jwordcombiner import JWordCombiner
from .intwordinfo import IntermediateWordInfo

class JDictProcessor:
    def __init__(self, lookupDictionary):
        self.attrRegex = re.compile('^.*?\(\s*(.+?)\s*\)', re.S)
        self.dictionary = lookupDictionary

    def getWordAttributes(self, entry):
        posSet = set()
        m = self.attrRegex.match(entry)
        if len(entry) and m:
            posTags = m.groups()[0].split(',')
            for pos in posTags:
                posSet.add(pos)
        else:
            raise RuntimeError('Invalid format: ' + entry)
        return posSet

    def getBestAlternative(self, wordsAndDefinitions, pos):
        if len(wordsAndDefinitions) == 0:
            return (None, None)
        elif len(wordsAndDefinitions) == 1:
            return wordsAndDefinitions[0]
        allAttributes = [self.getWordAttributes(definition) for word, definition in wordsAndDefinitions]
        mapper = WordMapper()
        res = mapper.selectBestWord(allAttributes, pos)
        if res is not None:
            return wordsAndDefinitions[res]
        else:
            return None

    def filterOnReading(self, readingsAndDefinitions, mecabReading):
        if len(readingsAndDefinitions) == 0:
            return [(None, None)]
        elif len(readingsAndDefinitions) == 1:
            return readingsAndDefinitions
        hiraganaReading = jcconv.kata2hira(mecabReading)
        filtered = []
        for reading, definition in readingsAndDefinitions:
            if hiraganaReading == reading:
                filtered.append(( reading, definition))
        return filtered if len(filtered) else readingsAndDefinitions

    def lookup(self, word):
        return self.dictionary.getFirstReadingAndDefinition(word)

    def mergeWords(self, words):
        fixedRules = [
                ( PoS.isNoun, PoS.isNoun, PoS.NOUN ),        # noun + noun -> noun
                ( lambda a: a == PoS.VERB, PoS.isAfterVerb, PoS.VERB ), # verb + aux -> verb
                ( lambda a: a == PoS.PREFIX_NOUN, PoS.isNoun, PoS.NOUN ), # prefix + noun -> num
                ( lambda a: a == PoS.NOUN_NUMERIC, lambda a: a == PoS.NOUN_NUMERIC, PoS.NOUN_NUMERIC ),  # num + num -> num
                ( lambda a: a == PoS.NOUN_ADJROOT, lambda a: a == PoS.VERB_AUX, PoS.ADJ ) # ちがいない
                ]
        combiner = JWordCombiner(self.lookup, fixedRules)
        return combiner.process(words)

##    def mergeVerbDeconjugate(self, a, b, dictionary):
##        if a.partOfSpeech == PoS.VERB and PoS.isAfterVerb(b.partOfSpeech):
##            tokens = dictionary.exactMatch(b)
##            words = [for tokens in ]
##            reading, definition = self.lookup(c)
##            if reading:
##                return WordInfo(c, a.startPos, c, PoS.VERB, reading)
##        return None
