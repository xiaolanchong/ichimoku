# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import unicodedata
from mecab.utils import isPy2x6

class TextParser:
    def __init__(self, text, noFurigana = True):
        self.__sentences = self.__markSentences(text)
        if noFurigana:
            self.__sentences = list(map(self.removeFurigana, self.__sentences))

    def __markSentences(self, text):
        inDirectSpeach = False
        sentences = []
        for group in re.findall("\s*(「|≪)|(?:(\S+?)(?:。|？|……|！|」|≫|\Z)|(」|≫))",
                                text, re.MULTILINE):
            if group[0]:
                inDirectSpeach = True
            elif group[2] or group[1] == '」' or group[1] == '≫':
                inDirectSpeach = False
            else:
                sentences.append(group[1].strip())
        return sentences

    def removeFurigana(self, sentence):
        if not isPy2x6():
            res = re.sub('(?<=[\u3005\u4E00-\u9FFF])《[\u3040-\u309F\u30A0-\u30FF]+》', '', sentence, 0, re.M|re.UNICODE)
        else:
            res = re.sub('(?<=[\u3005\u4E00-\u9FFF])《[\u3040-\u309F\u30A0-\u30FF]+》', '', sentence, re.M|re.UNICODE)
        return res


    def getSentences(self):
        return self.__sentences

if __name__ == '__main__':
    sentence = '錨《いかり》の騒'
    res = re.sub('(?<=[\u3005\u4E00-\u9FFF])《[\u3040-\u309F\u30A0-\u30FF]+》', '', sentence, 0, re.M|re.UNICODE)
    #res = re.sub('[\u4E00-\u9FFF]《', '', sentence, 0, re.M)
    print(res)

