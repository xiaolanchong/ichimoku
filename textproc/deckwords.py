# -*- coding: utf-8 -*-

class DeckWords:
    def __init__(self, textFileName):
        self.words = set()
        with open(textFileName, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                word = line.split('\t')[0]
                self.words.add(word)

    def isInDeck(self, word):
        return word in self.words