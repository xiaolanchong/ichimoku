# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from mecab.node import Node
from mecab.token import Token
from mecab.partofspeech import isNotWord

class WordInfo:
    def __init__(self, word, startPos, dictionaryForm, partOfSpeech, kanaReading):
        self.word = word
        self.startPos = startPos
        self.dictionaryForm = dictionaryForm
        self.partOfSpeech = partOfSpeech
        self.kanaReading = kanaReading

    def isNotWord(self):
        return isNotWord(self.partOfSpeech)

    def __repr__(self):
        return '({0}, {1}, {2}, {3}, {4})'.format(self.word, self.startPos,
                    self.dictionaryForm, self.partOfSpeech, self.kanaReading)

    def __eq__(self, other):
        return  self.word == other.word and \
                self.startPos == other.startPos and \
                self.dictionaryForm == other.dictionaryForm and \
                self.partOfSpeech == other.partOfSpeech and \
                self.kanaReading == other.kanaReading

    def __neq__(self, other):
        return not self.__eq__(other)

class Writer:
    def __init__(self):
        pass

    def getNodeText(self, tokenizer, path):
        nodeText = []
        for node in path:
            if tokenizer.isBOSNode(node):
                text = '<BOS>'
            elif tokenizer.isEOSNode(node):
                text = '<EOS>'
            else:
                text = node.token.text
            nodeText.append(text)
        return nodeText

    def getMecabOutput(self, tokenizer, path):
        res = []
        prevNodeCost = 0
        for node in path:
            nodeInfo = []
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            else:
                text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
            nodeInfo.append(text)
            nodeInfo.append(featureStr[6] if len(featureStr) >= 7 else '')
            nodeInfo.append(str(node.token.partOfSpeechId))
            nodeInfo.append(str(node.token.wordCost))
            nodeInfo.append(str(node.connectionCost))
            nodeInfo.append(str(node.totalCost))
            nodeInfo.append(str(node.token.leftAttribute))
            nodeInfo.append(str(node.token.rightAttribute))
            res.append(nodeInfo)
            prevNodeCost = node.totalCost
        return res

    def getMorphAndFeature(self, tokenizer, path):
        out =[]
        for node in path:
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
            padding = ['' for i in range(0 if len(featureStr) >= 7 else 7 - len(featureStr))]
            out.append([text] + featureStr + padding)
        return out

    def getWordInfo(self, tokenizer, path):
        out =[]
        for node in path:
            if tokenizer.isBOSNode(node) or \
               tokenizer.isEOSNode(node):
                continue
            text = node.token.text
            featureStr = tokenizer.getFeature(node.token.featureId, node.isKnown)
            featureStr = featureStr.split(',')
            out.append(WordInfo(text, node.startPos,  self.getItemOrEmptyStr(featureStr, 6),
                                node.token.partOfSpeechId, self.getItemOrEmptyStr(featureStr, 7)))
        return out



    def getItemOrEmptyStr(self, arr, index):
        return arr[index] if len(arr) > index else ''
