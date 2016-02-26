# -*- coding: utf-8 -*-

import copy
from mecab.dictionary import Dictionary
from mecab.charproperty import CharProperty
from mecab.token import Token
from mecab.node import Node

class Tokenizer:
    def __init__(self, loader):
        self.BOS_FEATURE = -1
        self.EOS_FEATURE = -2
        self.sysDictionary = Dictionary(loader, 'sys')
        self.unkDictionary = Dictionary(loader, 'unk')
        if self.sysDictionary.getCharSet() != 'euc-jp':
            raise RuntimeError('Unknown dictionary encoding: ' + self.sysDictionary.getCharSet())
        self.charProperties = CharProperty(loader, self.sysDictionary.getCharSet())
        self.spaceCharInfo = self.charProperties.getCharInfo(' ')
        self.unkCategoryTokens = self.loadUnknownCategoryTokens()

    def loadUnknownCategoryTokens(self):
        unkCategoryTokens = []
        for cat in self.charProperties.getCategories():
            tokens = self.unkDictionary.exactMatchSearch(cat)
            unkCategoryTokens.append(tokens)
        return unkCategoryTokens

    def getFeature(self, featureId, isKnown):
        if isKnown:
            return self.sysDictionary.getFeature(featureId)
        else:
            return '' #return self.unkDictionary.getFeature(featureId)

    def seekToOtherCharType(self, text, charInfo):
        for i in range(len(text)):
            ch = self.charProperties.getCharInfo(text[i])
            if not charInfo.isKindOf(ch):
                return i, ch
        return len(text), charInfo

    def needSeizeMoreChars(self, text, startCharInfo):
        if startCharInfo.invoke:
            endToLookupPos, endToLookup = self.seekToOtherCharType(text, startCharInfo)
            return endToLookupPos != 0
        else:
            return False

    def findNonSpacePosition(self, text):
        startToLookup, startCharInfo = self.seekToOtherCharType(text, self.spaceCharInfo)
        return startToLookup

    def lookUp(self, text, posInSentence):
        # skip leading spaces
        startToLookup, startCharInfo = self.seekToOtherCharType(text, self.spaceCharInfo)
        text = text[startToLookup:]
        posInSentence += startToLookup
        tokens = self.sysDictionary.commonPrefixSearch(text)
        result = []
        if tokens and len(tokens):
            result = [Node(token, posInSentence) for token in tokens]
        if len(result) and not startCharInfo.needAddUnknownChar():
            return result
        if len(text) == 1:
            if len(result) == 0:
                result += self.getUnknownTokens(startCharInfo, text[0], posInSentence)
            return result
        maxGroup, maxGroupPos = self.getMaxGroup(text, startCharInfo, posInSentence)
        result += maxGroup
        result += self.getExtraGroup(text, startCharInfo, maxGroupPos, posInSentence)
        if len(result) == 0:
            result += self.getUnknownTokens(startCharInfo, text[0], posInSentence)
        return result

    def getMaxGroup(self, text, startCharInfo, posInSentence):
        """
          managed by CharInfo.group
        """
        endToLookup = 0
        result = []
        if startCharInfo.canBeGrouped():
            endToLookupPos, endToLookup = self.seekToOtherCharType(text, startCharInfo)
            if endToLookupPos > 1:
                # extend the context and convert the found tokens to unknown ones
                result += self.getUnknownTokens(startCharInfo, text[0 : endToLookupPos], posInSentence)
        return result, endToLookup

    def getExtraGroup(self, text, startCharInfo, maxGroupPos, posInSentence):
        """
            managed by cahrInfo.length
        """
        result = []
        for i in range(1, startCharInfo.getExtraGroupNumber() + 1):
            #unknown token
            if i == maxGroupPos:
                continue
            if i > len(text):
                break
            charCategory = self.charProperties.getCharInfo(text[i-1])
            if startCharInfo.isKindOf(charCategory):
                result += self.getUnknownTokens(startCharInfo, text[0 : i], posInSentence)
            else:
                break
        return result

    def getUnknownTokens(self, startCharInfo, tokenText, posInSentence):
        assert(startCharInfo.defaultType < len(self.unkCategoryTokens))
        tokens = self.unkCategoryTokens[startCharInfo.defaultType]
        nodes = [Node(copy.copy(token), posInSentence) for token in tokens]
        for node in nodes:
            node.token.text = tokenText
            node.isKnown = False
        return nodes

    def getBOSNode(self, bosPos):
        t = Token('', 0, 0, 0, 0, self.BOS_FEATURE, 0)
        return Node(t, bosPos)

    def getEOSNode(self, eosPos):
        t = Token('', 0, 0, 0, 0, self.EOS_FEATURE, 0)
        return Node(t, eosPos)

    def isEOSNode(self, node):
        return node.token.featureId == self.EOS_FEATURE

    def isBOSNode(self, node):
        return node.token.featureId == self.BOS_FEATURE