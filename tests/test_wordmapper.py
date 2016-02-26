# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from textproc.wordmapper import WordMapper
from mecab import partofspeech as PoS

class WordMapperTest(unittest.TestCase):
    def setUp(self):
        self.mapper = WordMapper()

    def testMatchNoun(self):
        self.assertTrue(self.mapper.match(['n'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['vi'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['vi'], PoS.NOUN))
        self.assertFalse(self.mapper.match(['n'], PoS.NOUN_VSURU))
        self.assertTrue(self.mapper.match(['vs'], PoS.NOUN_VSURU))
        #self.assertTrue(self.)

    def testMatchVerb(self):
        self.assertTrue(self.mapper.match(['vi'], PoS.VERB))
        self.assertFalse(self.mapper.match(['vs'], PoS.VERB))
        #self.assertTrue()

    def testMatchAdjective(self):
        pass

    def testSuffix(self):
        self.assertFalse(self.mapper.match(['suf', 'uk', 'n'], PoS.NOUN_SUFFIX))
        self.assertFalse(self.mapper.match(['suf', 'ctr'], PoS.NOUN_SUFFIX))

    def testTaAuxillary(self):
        taWords = [['pref', 'n'], ['ok', 'adj-no', 'pn'], ['n'],
                   ['adj-no', 'n-adv', 'n'], ['arch', 'ctr', 'n-suf', 'n'],
                   ['aux-v']]
        self.assertEqual(5, self.mapper.selectBestWord(taWords, PoS.VERB_AUX))

    def testParticle(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['prt']], PoS.PRT_CASE))
        self.assertEqual(1, self.mapper.selectBestWord([['suf'], ['conj', 'int']], PoS.PRT_CASE))
        self.assertEqual(2, self.mapper.selectBestWord([['n'], ['suf', 'n'], ['adv', 'prt']], PoS.PRT_CASE))

    def testConjunction(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['adv', 'conj', 'uk']], PoS.CONJ))

    def testVerb(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['vi', 'v5r', 'uk']], PoS.VERB))

    def testNoun(self):
        self.assertEqual(0, self.mapper.selectBestWord([['n'], ['vi', 'v5r', 'uk']], PoS.NOUN))

    def testAdj(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['vs', 'adj-no']], PoS.ADJ))

    def testPrenounAdj(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['adj-pn', 'uk']], PoS.ADJ_PRENOUN))

    def testAdverb(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['adv', 'uk', 'on-mim']], PoS.ADVERB))

    def testInterjection(self):
        self.assertEqual(1, self.mapper.selectBestWord([['n'], ['int', 'uk', 'on-mim']], PoS.INT))

    def testPrefix(self):
        self.assertEqual(1, self.mapper.selectBestWord([['v5s'], ['n', 'vs']], PoS.PREFIX_ADJ))

    def testVerbSuffix(self):
        self.assertEqual(1, self.mapper.selectBestWord([['v5s'], ['suf', 'v5r']], PoS.VERB_SUFFIX))

    def testVerbNonIndependent(self):
        self.assertEqual(1, self.mapper.selectBestWord([['vs'], ['v5r', 'aux']], PoS.VERB_NONIND))

    def testNounSuffix(self):
        self.assertEqual(1, self.mapper.selectBestWord([['v5s'], ['suf', 'n']], PoS.NOUN_SUFFIX))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WordMapperTest)
    unittest.TextTestRunner(verbosity=2).run(suite)