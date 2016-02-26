# -*- coding: utf-8 -*-

from struct import unpack

class Connector:
    def __init__(self, loader):
        self.lsize = 0
        self.rsize = 0
        self.matrix = None
        with loader.load('matrix') as dataReader:
            header = dataReader.read(4)
            self.lsize, self.rsize = unpack('HH', header)
            self.matrix = dataReader.read( self.lsize * self.rsize * 2)

    def checkDimension(self, argName, value, size):
        if value < 0 or value >= size:
            raise RuntimeError('{0} is out of {1} range [{2}, {3}]'.format(
                                value, argName, 0, size - 1
                                ))

    def getCost(self, leftAttribute, rightAttribute):
        self.checkDimension('leftAttribute', leftAttribute, self.lsize)
        self.checkDimension('rightAttribute', rightAttribute, self.rsize)
        start = leftAttribute + self.lsize * rightAttribute
        num, = unpack('h', self.matrix[2*start : 2*start+2])
        return num

