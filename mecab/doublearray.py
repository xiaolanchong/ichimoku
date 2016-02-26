# -*- coding: utf-8 -*-

from struct import unpack

class DoubleArray:
    def __init__(self, data):
        assert(isinstance(data, bytes))
        self.data = data

    def exactMatchSearch(self, sequence):
        assert(len(sequence))
        node_pos = 0
        base, dummy = self.getItem(node_pos)
        res = []
        for item in sequence:
            p = base + item + 1
            bz, cz = self.getItem(p)
            if base == cz:
                base = bz
            else:
                return res
            bb, cc = self.getItem(base)
        if base == cc and bb < 0:
            res.append((-bb-1, len(sequence)))
        return res

    def getItem(self, index):
        return unpack('<iI', self.data[8*index : 8*index+8])

    def commonPrefixSearch(self, sequence):
        node_pos = 0
        base, dummy = self.getItem(node_pos)
        res = []
        idx = 0
        for item in sequence:
            bb, cc = self.getItem(base)
            if base == cc and bb < 0:
                res.append((-bb-1, idx))
            p = base + item + 1
            bz, cz = self.getItem(p)
            if base == cz:
                base = bz
            else:
                return res
            idx += 1
        bb, cc = self.getItem(base)
        if base == cc and bb < 0:
            res.append((-bb-1, idx))
        return res
