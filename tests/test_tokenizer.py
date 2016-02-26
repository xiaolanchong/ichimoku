# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from mecab.tokenizer import Tokenizer
import mecab.partofspeech as PoS
from textproc.dataloader import getDataLoader

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer(getDataLoader())

    def testSkipingSpaces(self):
        nodes = self.tokenizer.lookUp(' ' * 3 + '少し', 4)
        self.assertEqual(5, len(nodes))
        self.assertEqual('少', nodes[0].token.text)
        self.assertEqual(4 + 3, nodes[0].startPos)
        self.assertEqual(4 + 3, nodes[1].startPos)

    def testWhiteSpaces(self):
        nodes = self.tokenizer.lookUp('\n少し', 4)
        self.assertEqual(5, len(nodes))
        self.assertEqual('少', nodes[0].token.text)
        self.assertEqual(4 + 1, nodes[0].startPos)
        self.assertEqual(4 + 1, nodes[1].startPos)

    def testFindNonSpace(self):
        pos = self.tokenizer.findNonSpacePosition('少し')
        self.assertEqual(0, pos)
        pos = self.tokenizer.findNonSpacePosition('')
        self.assertEqual(0, pos)
        pos = self.tokenizer.findNonSpacePosition('  少し')
        self.assertEqual(2, pos)
        pos = self.tokenizer.findNonSpacePosition('\n  \t少し')
        self.assertEqual(4, pos)

    def testLatinSymbols(self):
        """
            Latin chars are grabbed as a whole
        """
        nodes = self.tokenizer.lookUp('kana', 4)
        self.assertEqual(6, len(nodes))
        self.assertEqual(4 + 0, nodes[0].startPos)
        for node in nodes:
            self.assertEqual('kana', node.token.text)

    def testBreakSymbol(self):
        """
           滲 can't be joined with 《
        """
        nodes = self.tokenizer.lookUp('滲《し》み込み', 4)
        self.assertEqual(6, len(nodes))
        for i in range(6):
            self.assertEqual('滲', nodes[i].token.text)

    def testUnicodeError(self):
        """
            '－' can't be encoded in euc-jp
        """
        nodes = self.tokenizer.lookUp('ドンキ－・バー', 0)
        self.assertEqual(19, len(nodes))


    def testUnknownKanaWord(self):
        """
            'ざめ' is unknown
        """
        nodes = self.tokenizer.lookUp('ざめて見えた', 0)
        self.assertEqual(14, len(nodes))

    def testGroupUnknown(self):
        """
            Grabs the entire kana symbols + 2 chars
        """
        nodes = self.tokenizer.lookUp('マール・ブランデーの壜', 0)
        self.assertEqual(12, len(nodes))
        for i in range(0, 6):
            self.assertEqual('マール・ブランデー', nodes[i].token.text)
        for i in range(6, 12):
            self.assertEqual('マ', nodes[i].token.text)

    def testComma(self):
        nodes = self.tokenizer.lookUp('、', 0)
        self.assertEqual(2, len(nodes))
        self.assertEqual(PoS.NOUN_NUMERIC, nodes[0].token.partOfSpeechId)
        self.assertEqual(PoS.COMMA, nodes[1].token.partOfSpeechId)

    def testBracket(self):
        nodes = self.tokenizer.lookUp('」', 0)
        self.assertEqual(1, len(nodes))

    def testKnownKanaInGroup(self):
        nodes = self.tokenizer.lookUp('ジーン・モーラの姿', 0)
        self.assertEqual(13, len(nodes))
        self.assertEqual('ジーン', nodes[0].token.text)
        for i in range(1, 7):
            self.assertEqual('ジーン・モーラ', nodes[i].token.text)
        for i in range(7, 13):
            self.assertEqual('ジ', nodes[i].token.text)

    def testUnknownGrouppedChars(self):
        nodes = self.tokenizer.lookUp('づめに', 0)
        self.assertEqual(14, len(nodes))
        for i in range(0, 7):
            self.assertEqual('づめに', nodes[i].token.text)
        for i in range(7, 14):
            self.assertEqual('づ', nodes[i].token.text)

    def testKanjiRow(self):
        nodes = self.tokenizer.lookUp('一列縦隊で', 0)
        self.assertEqual(5, len(nodes))
        for i in range(0, 4):
            self.assertEqual('一', nodes[i].token.text)
        self.assertEqual('一列縦隊', nodes[4].token.text)

    def testUnknownKanji(self):
        nodes = self.tokenizer.lookUp('四時頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))
        nodes = self.tokenizer.lookUp('時頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))
        nodes = self.tokenizer.lookUp('頃に', 0)
        self.assertEqual(1, len(nodes[0].token.text))

    def testDash(self):
        nodes = self.tokenizer.lookUp('ー・', 0)
        self.assertEqual(12, len(nodes))
        for i in range(0, 6):
            self.assertEqual('ー・', nodes[i].token.text)
        for i in range(6, 12):
            self.assertEqual('ー', nodes[i].token.text)

    def testKanjiGroup(self):
        nodes = self.tokenizer.lookUp('疫所', 0)
        self.assertEqual(6, len(nodes))
        for i in range(0, 3):
            self.assertEqual('疫', nodes[i].token.text)
        for i in range(3, 6):
            self.assertEqual('疫所', nodes[i].token.text)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TokenizerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)