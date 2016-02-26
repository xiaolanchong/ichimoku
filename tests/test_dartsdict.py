# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
import operator
sys.path.append(os.path.abspath('..'))
from textproc import dartsdict
from textproc.dataloader import getDataLoader

class DartsDictionaryTest(unittest.TestCase):
    def setUp(self):
        self.dictionary = dartsdict.DartsDictionary(getDataLoader().load('jdict'))

    def testRecord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('開扉')
        self.assertEqual('かいひ', reading)
        self.assertEqual('(n,vs) opening a door', entry)

    def testMultipleDefinition(self):
        res = self.dictionary.getAllReadingAndDefinition('降る')
        self.assertEqual(['くだる', 'ふる'], list(map(operator.itemgetter(0), res)))
        res = list(self.dictionary.getAllReadingAndDefinition('電燈'))
        res = res

    def testDuplicatedRecord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('々')
        self.assertEqual('くりかえし', reading)
        self.assertEqual('(n) repetition of kanji (sometimes voiced)', entry)

    def testNoSuchWord(self):
        reading, entry = self.dictionary.getFirstReadingAndDefinition('メグレ')
        self.assertEqual(None, reading)
        self.assertEqual(None, entry)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DartsDictionaryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)