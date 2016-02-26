# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from mecab.dictionary import Dictionary
from mecab.token import Token
from textproc.dataloader import getDataLoader

class DictionaryTest(unittest.TestCase):
    def setUp(self):
        self.dict = Dictionary(getDataLoader(), 'sys')

    def testInternalCommonPrefix(self):
        res = self.dict.internalCommonPrefixSearch('船')
        self.assertEqual([(67884804, 2)], res)
        res = self.dict.internalCommonPrefixSearch('が')
        self.assertEqual([(5274372, 2)], res)
        res = self.dict.internalCommonPrefixSearch('検疫')
        self.assertEqual([(42079745, 2), (42086145, 4)], res)
        res = self.dict.internalCommonPrefixSearch('かかわらず、')
        self.assertEqual([(4058371, 2), (4187651, 4), (4212737, 6), (4213249, 8)], res)
        res = self.dict.internalCommonPrefixSearch('デッキ')
        self.assertEqual([(23825665, 2), (23878657, 6)], res)

    def testCommonPrefix(self):
        res = self.dict.commonPrefixSearch('か')
        kaTokens = [ Token('か', 359, 359, 22, 5360, 14505916, 0),
                     Token('か', 776, 776, 31, 10872, 17590041, 0),
                     Token('か', 1001, 1001, 33, 12742, 18988624, 0) ]
        self.assertEqual(kaTokens, res)

    def testExactMatch(self):
        res = self.dict.exactMatchSearch('～')
        self.assertEqual(0, len(res))
        res = self.dict.commonPrefixSearch('～')
        self.assertEqual(0, len(res))
        res = self.dict.commonPrefixSearch('検～')
        self.assertEqual(1, len(res))

    def testUnicodeError(self):
        res = self.dict.exactMatchSearch('かかわら')
        kaTokens = [ Token('かかわら', 780, 780, 31, 5413, 16382529, 0) ]
        self.assertEqual(kaTokens, res)

    def testFeature(self):
        res = self.dict.getFeature(14505916)
        self.assertEqual('助詞,副助詞／並立助詞／終助詞,*,*,*,*,か,カ,カ', res)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DictionaryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)