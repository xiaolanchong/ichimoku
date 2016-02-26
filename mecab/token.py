# -*- coding: utf-8 -*-

class Token:
    def __init__(self, text, leftAttribute, rightAttribute,
                       partOfSpeechId, wordCost,
                       featureId, compound):
        self.text = text
        self.leftAttribute = leftAttribute
        self.rightAttribute = rightAttribute
        self.partOfSpeechId = partOfSpeechId
        self.wordCost = wordCost
        self.featureId = featureId
        self.compound = compound

    def __eq__(self, other):
        return  self.text == other.text and \
                self.leftAttribute == other.leftAttribute and \
                self.rightAttribute == other.rightAttribute and  \
                self.partOfSpeechId == other.partOfSpeechId and  \
                self.wordCost == other.wordCost and \
                self.featureId == other.featureId and \
                self.compound == other.compound

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{0}, la:{1}, ra:{2}, PoS:{3}, cost:{4}, feature:{5}, compound:{6}'.format(
                    self.text, self.leftAttribute, self.rightAttribute,
                    self.partOfSpeechId, self.wordCost, self.featureId,
                    self.compound)