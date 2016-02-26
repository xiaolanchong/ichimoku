# -*- coding: utf-8 -*-

class Glossary:
    def __init__(self):
        self.words = set()
        self.foundWords = []
        self.unknownWords = []

    def add(self, word, reading, definition, usageSample):
        if word not in self.words:
            self.words.add(word)
            if reading and definition:
                self.foundWords.append((word, reading, definition, usageSample))
            else:
                self.unknownWords.append((word, usageSample))

    def getFoundWords(self):
        return self.foundWords

    def getUnknownWords(self):
        return self.unknownWords