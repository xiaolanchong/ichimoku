# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, platform, re, subprocess
from mecab import utils
from mecab import runmecab
from mecab.viterbi import Viterbi
from mecab.writer import Writer, WordInfo
from .dataloader import getDataLoader

class MecabSentenceParser:
    def __init__(self):
        self.mecab = runmecab.MecabRunner(
             '%m,%ps,%f[6],%h,%f[7] ', '\n', '[%m,%ps] ')

    def tokenize(self, expr):
        exprFromMecab = self.mecab.run(expr)
        out = []
        for line in exprFromMecab:
            for node in line.split(" "):
                if not node:
                  break
                m =  re.match("(.+),(.+),(.+),(.*),(.*)", node);
                if m is None:
                    m = re.match("\[(.+),(.+)\]", node)
                    if m:
                    #raise RuntimeError('unknown node: ' + node)
                        word, startPos= m.groups(0)
                        # word, startPos, dictionaryForm, partOfSpeech, kanaReading
                        unicodeTextPos = int(startPos)/2
                        out.append(WordInfo(word, unicodeTextPos, word, PoS.UNKNOWN, ''))
                    else:
                        raise RuntimeError(node)
                else:
                    word, startPos, dictionaryForm, partOfSpeech, kanaReading = m.groups(0)
                    unicodeTextPos = int(startPos)/2
                    out.append(WordInfo(word, unicodeTextPos, dictionaryForm, int(partOfSpeech), kanaReading))
        return out

class PyPortSentenceParser(object):
    def __init__(self, dataLoader):
        self.mecab = None
        self.viterbi = Viterbi(dataLoader)
        self.writer = Writer()

    def tokenize(self, expr):
        path = self.viterbi.getBestPath(expr)
        return self.writer.getWordInfo(self.viterbi.getTokenizer(), path)
