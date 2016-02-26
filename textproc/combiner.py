# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class Combiner:
    def __init__(self):
        pass

    def isDelimiter(self, a):
        pass

    def combine(self, a, b):
        pass

    def process(self, tokens):
        result = list(tokens)
        aPos = 0
        bPos = 1
        while True:
            if aPos + 1 >= len(result):
                break
            if bPos >= len(result):
                break
            if self.isDelimiter(result[aPos]):
                aPos += 1
                bPos = aPos + 1
                continue
            if self.isDelimiter(result[bPos]):
                aPos = bPos + 1
                bPos = aPos + 1
                continue
            combinedToken = self.combine(result[aPos], result[bPos])
            if combinedToken is not None:
                result[aPos] = combinedToken
                result.pop(bPos)
                continue
            else:
                aPos += 1
                bPos += 1
                continue
        return result
