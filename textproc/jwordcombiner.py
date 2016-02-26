# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from . import combiner
from .intwordinfo import IntermediateWordInfo

class JWordCombiner(combiner.Combiner):
    def __init__(self, dictionary, combineRules):
        self.combineRules = combineRules
        self.dictionary = dictionary

    def isDelimiter(self, a):
        return a.isSymbol or not a.isKnownWord

    def combine(self, a, b):
        for conditionA, conditionB, resultPoS in self.combineRules:
            if conditionA(a.partOfSpeech) and conditionB(b.partOfSpeech):
                mergedWord = a.word + b.word
                reading, definition = self.dictionary(mergedWord)
                if reading:
                    return IntermediateWordInfo(mergedWord, a.startPos, resultPoS, reading, definition)
        return None
