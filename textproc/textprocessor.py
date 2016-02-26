# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import logging
import codecs
from mecab.utils import text_type
from .textparser import TextParser
from .sentenceparser import PyPortSentenceParser, MecabSentenceParser
from .glossary import Glossary
from .dartsdict import DartsDictionary
from .jdictprocessor import JDictProcessor
from .intwordinfo import IntermediateWordInfo

class Settings:
    """
    Output settings of the processor
    """
    def __init__(self):
        self.ignoreSymbols = False # do not output 、 ？ etc.
        self.readingForKanjiOnly = False # do not provide reading if the word has no kanji
        self.sentenceOnlyForFirst = False # give the sentence only for the 1st word in it

    @classmethod
    def Minimal(cls):
        s = Settings()
        s.sentenceOnlyForFirst = True
        s.readingForKanjiOnly = True
        s.ignoreSymbols = True
        return s

    @classmethod
    def NoExcessiveReading(cls):
        s = Settings()
        s.ignoreSymbols = True
        s.sentenceOnlyForFirst = False
        s.readingForKanjiOnly = True
        return s

    @classmethod
    def Verbose(cls):
        s = Settings()
        s.ignoreSymbols = False
        s.readingForKanjiOnly = False
        s.sentenceOnlyForFirst = False
        return s

class TextProcessor:
    def __init__(self, dataLoader):
      self.dictionary = DartsDictionary(dataLoader.load('jdict'))
      if True:
        self.parser = PyPortSentenceParser(dataLoader)
      else:
        self.parser = MecabSentenceParser()

    @classmethod
    def hasKanji(cls, word):
        m = re.search("[\u4E00-\u9FFF]", word, re.S|re.UNICODE)
        return m is not None

    def getContext(self, text, wordInfo):
        """
        Gets 10 symbol before and after the given one
        text: text to the substring extract from
        wordInfo: the mean of the range
        """
        contextStart = max(0, wordInfo.startPos - 10)
        contextEnd = min(wordInfo.startPos + len(wordInfo.word) + 10, len(text))
        textToLog = text[contextStart:contextEnd]
        return textToLog

    def parseSentenceWithBestChoice(self, text, settings, mergeWords):
        """
        Parses and selects the best match to JDICT dictionary
        text: string to parse
        settings: Settings object to set the parsing up
        """
        allWords = self.stepOne(text, settings)
        jdictProcessor = JDictProcessor(self.dictionary)
        if mergeWords:
            allWords = jdictProcessor.mergeWords(allWords)
        return self.stepTwo(allWords, settings)


    def stepTwo(self, allWordInfo, settings):
        result = []
        for wordInfo in allWordInfo:
            if wordInfo.isSymbol:
                if not settings.ignoreSymbols:
                    result.append((wordInfo.word, wordInfo.startPos, '', ''))
            elif not wordInfo.isKnownWord:
                result.append((wordInfo.word, wordInfo.startPos, '', ''))
            else:
                if settings.readingForKanjiOnly and not TextProcessor.hasKanji(wordInfo.word):
                    reading = ''
                else:
                    reading = wordInfo.reading
                result.append((wordInfo.word, wordInfo.startPos, reading, wordInfo.definition))
        return result

    def stepOne(self, text, settings):
        allWordInfo = self.parser.tokenize(text)
        jdictProcessor = JDictProcessor(self.dictionary)
        result = []
        for wordInfo in allWordInfo:
            if wordInfo.isNotWord():
                result.append(IntermediateWordInfo.createNonWord(wordInfo.word, wordInfo.startPos, wordInfo.partOfSpeech))
                logging.info("'%s' is an unknown token. Text: '%s'",
                            wordInfo.word, self.getContext(text, wordInfo))
            elif len(wordInfo.dictionaryForm):
                alternatives = self.dictionary.getAllReadingAndDefinition(wordInfo.dictionaryForm)
                alternatives = jdictProcessor.filterOnReading(alternatives, wordInfo.kanaReading)
                reading, definition = jdictProcessor.getBestAlternative(alternatives, wordInfo.partOfSpeech)
                result.append(IntermediateWordInfo(wordInfo.dictionaryForm, wordInfo.startPos, wordInfo.partOfSpeech, reading, definition))
            else:
                result.append(IntermediateWordInfo.createUnknownWord(wordInfo.word, wordInfo.startPos, wordInfo.partOfSpeech))
                logging.info("'%s' not found in dictionary. Text: '%s'",
                                wordInfo.word, self.getContext(text, wordInfo))
        return result

    def do(self, text, settings = Settings.Verbose(), mergeWords = False):
        p = TextParser(text)
        glossary = Glossary()
        for sentence in p.getSentences():
            allWords = self.parseSentenceWithBestChoice(sentence, settings, mergeWords)
            for word, startPos, reading, definition in allWords:
                yield word, startPos, reading, definition, sentence