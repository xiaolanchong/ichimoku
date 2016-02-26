# -*- coding: utf-8 -*-

from mecab.token import Token

class Node:
    def __init__(self, token, startPos):
        self.leftNode = None    # reference to the node before
        self.rightNode = None   # reference to the node after
        self.totalCost = 0      # cost of the entire path till the node
        self.startPos = startPos    # starting position of the token in the sentence
        self.token = token      # token from the dictionary
        self.connectionCost = 0 # cost after the connection
        self.isKnown = True     # known token?

    def createUnknownNode(text):
        t = Token(text, 0, 0, 0, 0, 0, 0)
        return Node(t)

    def connect(left, right, connectionCost, totalCost):
        assert(left)
        assert(right)
        left.rightNode = right
        right.leftNode = left
        right.totalCost = totalCost
        right.connectionCost = connectionCost

    def __repr__(self):
        return 'token: [{0}], startPos: {1}, totalCost: {2}'.format(
                    self.token, self.startPos, self.totalCost)