# -*- coding: utf-8 -*-

import struct
from mecab.doublearray import DoubleArray
from mecab.utils import binary_type, text_type, extractString, isPy2x6
from mecab.compress import load as zipload

class DartsDictionary:
    def __init__(self, dataReader):
        self.readData(dataReader)

    def readData(self, dictFile):
        magicId = dictFile.read(4)
        if magicId != b'JDC0':
            raise RuntimeError('File is not JDIC file')
        charSetBuffer, = struct.unpack('32s', dictFile.read(32))
        self.charset = extractString(charSetBuffer).lower()
        fmt = 'III'
        (dartsSize, entryOffsetBlobSize, entryBlobSize) = \
             struct.unpack('III', dictFile.read(struct.calcsize(fmt)))
        self.lookupDict = DoubleArray(dictFile.read(dartsSize))
        self.entryOffsetBlob = dictFile.read(entryOffsetBlobSize)
        self.entryBlob = dictFile.read(entryBlobSize)

    def getFirstReadingAndDefinition(self, word):
        entries = self.getAllReadingAndDefinition(word)
        return entries[0] if len(entries) else (None, None)

    def getAllReadingAndDefinition(self, word):
        assert(len(word))
        entries = []
        offsets = self.lookupDict.exactMatchSearch(bytearray(word, 'utf-8'))
        for tokenHandler, tokenLength in offsets:
            entryNum = tokenHandler & 0xff
            entryOffsetStartPos = tokenHandler >> 8
            for i in range(entryNum):
                offset = self.getEntryOffset(entryOffsetStartPos + i)
                entry = self.getEntry(offset)
                (kanji, kana, text) = entry.split(b'\x01')
                kanji = text_type(kanji, 'utf-8')
                kana = text_type(kana, 'utf-8')
                text = text_type(text, 'utf-8')
                entries.append((kana, text))
        return entries

    def getBestReadingAndDefinition(self, word, pos):
        entries = self.getAllReadingAndDefinition(word)

    def getEntryOffset(self, entryOffsetIdx):
        fmt = 'I'
        offsetSize = struct.calcsize(fmt)
        offset, = struct.unpack(fmt, self.entryOffsetBlob[entryOffsetIdx * offsetSize : (entryOffsetIdx + 1) * offsetSize])
        return offset

    def getEntry(self, entryOffset):
        endOfEntry = self.entryBlob.find(b'\x00', entryOffset)
        if endOfEntry >= 0:
            return self.entryBlob[entryOffset:endOfEntry]
        else:
            return None

    def splitEntry(self, entry):
        entry.split(b'\x01')