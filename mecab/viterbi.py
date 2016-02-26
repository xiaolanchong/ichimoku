# -*- coding: utf-8 -*-

import sys
from mecab.tokenizer import Tokenizer
from mecab.connector import Connector
from mecab.node import Node

class Viterbi:
    def __init__(self, loader):
        self.tokenizer = Tokenizer(loader)
        self.connector = Connector(loader)

    def getTokenizer(self):
        return self.tokenizer

    def getBestPath(self, text):
        endNodes = [[] for i in range(len(text) + 1)]
        bosNode = self.tokenizer.getBOSNode(0)
        endNodes[0] = [bosNode]
        posInText = 0
        while posInText < len(text):
            nextPosInText = posInText + 1
            if len(endNodes[posInText]) > 0:
                skipCharNumber = self.tokenizer.findNonSpacePosition(text[posInText:])
                lookFrom = skipCharNumber + posInText
                nextPosInText = lookFrom + 1
                if lookFrom >= len(text):
                    break
                nodes = self.tokenizer.lookUp(text[lookFrom:], lookFrom)
                for node in nodes:
                    self.connect(endNodes[posInText], node)
                    endNodes[lookFrom + len(node.token.text)].append(node)
            posInText = nextPosInText
        eosNode = self.tokenizer.getEOSNode(len(text))
        for i in range(1, len(endNodes)):
            if len(endNodes[-i]):
                self.connect(endNodes[-i], eosNode)
                break
        return self.createBackwardPath(eosNode)

    def connect(self, beginNodes, endNode):
        bestNode = None
        bestCost = sys.maxsize
        bestNodeConnection = 0
        for beginNode in beginNodes:
            if True: # beginNode.isKnown and endNode.isKnown:
                connectionCost = self.connector.getCost(beginNode.token.rightAttribute,
                                                    endNode.token.leftAttribute)
                totalCost = beginNode.totalCost + endNode.token.wordCost + connectionCost
            else:
                totalCost = beginNode.totalCost
            if totalCost < bestCost:
                bestCost = totalCost
                bestNode = beginNode
                bestNodeConnection = connectionCost
        if bestNode:
            Node.connect(bestNode, endNode, bestNodeConnection, bestCost)

    def createBackwardPath(self, endNode):
        beginNode = endNode
        path = []
        while(endNode):
            path.append(endNode)
            endNode = endNode.leftNode
        path.reverse()
        return path


