# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import operator
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from mecab.writer import WordInfo
from mecab import partofspeech as PoS
from  textproc.dataloader import getDataLoader
from textproc.sentenceparser import MecabSentenceParser, PyPortSentenceParser

class SentenceParserTest(unittest.TestCase):
    def setUp(self):
        self.pyparser = PyPortSentenceParser(getDataLoader())
        self.exeparser = MecabSentenceParser()

    def testExeSimple(self):
        res = self.exeparser.tokenize('ですからあの人')
        expected = [WordInfo('ですから', 0, 'ですから', PoS.CONJ, 'デスカラ'),
                    WordInfo('あの', 4, 'あの', PoS.FILLER, 'アノ'),
                    WordInfo('人', 6, '人' ,PoS.NOUN, 'ヒト')]
        self.assertEquals(expected, res)

    def testPySimple(self):
        res = self.pyparser.tokenize('ですからあの人')
        expected = [WordInfo('ですから', 0, 'ですから', PoS.CONJ, 'デスカラ'),
                    WordInfo('あの', 4, 'あの', PoS.FILLER, 'アノ'),
                    WordInfo('人', 6, '人' ,PoS.NOUN, 'ヒト')]
        self.assertEquals(expected, res)


    def testMecabFailure(self):
        """
            A test where Mecab fails to recognize the verb 滲み込む
        """
        result = self.exeparser.tokenize('すべてに滲み込み')
        result = list(map(operator.attrgetter('dictionaryForm'), result))
        self.assertEquals(['すべて', 'に', '滲みる', '込み'], result)

    def testPyPort(self):
        result = self.pyparser.tokenize('所に着いたのは')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['所', 'に', '着い', 'た', 'の', 'は'], result)

    def testWhiteSpace(self):
        result = self.pyparser.tokenize('\n所に着いたのは')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['所', 'に', '着い', 'た', 'の', 'は'], result)

    def testNumericKanji(self):
        result = self.pyparser.tokenize('一列縦隊')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['一', '列', '縦隊'], result)

    def testUnicodeErrorInString(self):
        result = self.pyparser.tokenize('ドンキ－・バー')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['ドンキ', '－', '・', 'バー'], result)



    def testTokenizeNum(self):
        """
        ～
        """
        result = self.pyparser.tokenize('九～九')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['九', '～', '九'], result)

    def testWhiteSpaceInside(self):
        result = self.pyparser.tokenize('\n船が検 疫所に\n')
        words = list(map(operator.attrgetter('word'), result))
        self.assertEquals(['船', 'が', '検', '疫所', 'に'], words)
        positions = list(map(operator.attrgetter('startPos'), result))
        self.assertEquals([1, 2, 3, 5, 7], positions)

    def testTokenize2(self):
        res = self.pyparser.tokenize('所に着いたのは')
        expected = [ WordInfo('所', 0, '所', PoS.NOUN, 'トコロ'),
                     WordInfo('に', 1, 'に', PoS.PRT_CASE, 'ニ'),
                     WordInfo('着い', 2, '着く', PoS.VERB, 'ツイ'),
                     WordInfo('た', 4, 'た', PoS.VERB_AUX, 'タ'),
                     WordInfo('の', 5, 'の', PoS.NOUN_NONIND, 'ノ'),
                     WordInfo('は', 6, 'は', PoS.PRT_BIND, 'ハ')
                   ]
        self.assertEquals(expected, res)

    def testUnknownWord(self):
        res = self.pyparser.tokenize('デッキに昇って行った')
        expected = [ WordInfo('デッキ', 0, 'デッキ', PoS.NOUN, 'デッキ'),
                     WordInfo('に', 3, 'に', PoS.PRT_CASE, 'ニ')
                   ]
        self.assertEquals(expected, res[0:2])

    def testComma(self):
        result = self.pyparser.tokenize('や、船客')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEqual(['や', '、', '船客'], result)

    def testUnkUnk(self):
        result = self.pyparser.tokenize('はっぴー・ばれん')
        result = list(map(operator.attrgetter('word'), result))
        self.assertEqual(['はっぴ', 'ー', '・', 'ばれ','ん'], result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SentenceParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)