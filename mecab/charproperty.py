# -*- coding: utf-8 -*-
from struct import unpack
import mecab.utils as utils

class CharInfo:
    def __init__(self, type, defaultType, length, group, invoke):
        self.type = type  # bit mask of the categories the char belongs to
        self.defaultType = defaultType
        self.length = length # 1 to n length new words are added (in Shift-JIS)
        self.group = group  # 1/0:   make a new word by grouping the same character category
        self.invoke= invoke # always invoke unknown word processing, evan when the word can be found in the lexicon

    def isKindOf(self, charInfo):
        return self.type & charInfo.type

    def isInCategory(self, categoryId):
        return self.type & (1 << categoryId)

    def canBeGrouped(self):
        return self.group != 0

    def getExtraGroupNumber(self):
        return self.length

    def needAddUnknownChar(self):
        return self.invoke != 0

    def __repr__(self):
        return 'type:{0}, defaultType:{1}, length:{2}, group:{3}, invoke:{4}'.format(
                 self.type, self.defaultType, self.length,
                 self.group, self.invoke)

class CharProperty:
    def __init__(self, loader, encoding='euc-jp'):
        self.__map = []
        self.__categories = []
        with loader.load('char') as dataReader:
            self.loadFromBinary(dataReader, encoding)

    def loadFromBinary(self, inFile, encoding):
     #   with open(fileName, 'rb') as inFile:
            uintSize = 4
            categoryBuffer = 32
            categoryNum, = unpack('<I', inFile.read(uintSize))
            calcFileSize = uintSize + categoryBuffer * categoryNum + uintSize * 0xffff
            for i in range(categoryNum):
                categoryStr, = unpack(str(categoryBuffer) + 's', inFile.read(categoryBuffer))
                self.__categories.append( utils.extractString(categoryStr, encoding))
            for i in range(0xffff):
                packedCharInfo, = unpack('<I', inFile.read(uintSize))
                charInfo = CharInfo( (packedCharInfo      ) & 0x3FFFF,
                                     (packedCharInfo >> 18) & 0xFF,
                                     (packedCharInfo >> 26) & 0xF,
                                     (packedCharInfo >> 30) & 0x1,
                                     (packedCharInfo >> 31) & 0x1)
                self.__map.append(charInfo)

    def getCategories(self):
        return self.__categories


    def getCharInfo(self, char):
        return self. __map[ord(char)]

    def getCharCaterogies(self, char):
        char = self.getCharInfo(char)
        categoryNames = []
        for i in range(len(self.__categories)):
            if char.isInCategory(i):
                categoryNames.append(self.__categories[i])
        return categoryNames;

