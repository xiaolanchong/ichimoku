# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os.path
import unittest
import sys
sys.path.append(os.path.abspath('..'))
from mecab.charproperty import CharProperty
from textproc.dataloader import getDataLoader

class CharInfoTest(unittest.TestCase):
    def testCharCategories(self):
        prop = CharProperty(getDataLoader())
        self.assertEqual(['DEFAULT', 'SPACE', 'KANJI', 'SYMBOL',
                          'NUMERIC', 'ALPHA', 'HIRAGANA', 'KATAKANA',
                          'KANJINUMERIC', 'GREEK', 'CYRILLIC'], prop.getCategories())
        self.assertEqual(['SPACE'], prop.getCharCaterogies(' '))
        self.assertEqual(['NUMERIC'], prop.getCharCaterogies('1'))
        self.assertEqual(['ALPHA'], prop.getCharCaterogies('a'))
        self.assertEqual(['KANJI'], prop.getCharCaterogies('吗'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CharInfoTest)
    unittest.TextTestRunner(verbosity=2).run(suite)