# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
import operator
sys.path.append(os.path.abspath('..'))
from textproc.textprocessor import TextProcessor, Settings
from textproc.dataloader import getDataLoader
from mecab.writer import WordInfo

class TextProcessorTest(unittest.TestCase):
    def setUp(self):
        self.textProc = TextProcessor(getDataLoader())
        self.maxDiff = None

    def testDumpAll(self):
        res = self.textProc.do('船が検疫所に着いたのは', Settings.Verbose())
        res = list(res)
        expected = \
        [
        ('船', 0, 'ふね', '(n,n-suf,ctr) ship/boat/watercraft/vessel/steamship/tank/tub/vat/trough/counter for boat-shaped containers (e.g. of sashimi)/(P)', '船が検疫所に着いたのは'),
        ('が', 1, 'が', '(prt,conj) indicates sentence subject (occasionally object)/indicates possessive (esp. in literary expressions)/but/however/still/and/(P)', '船が検疫所に着いたのは'),
        ('検疫', 2, 'けんえき', '(n,vs) quarantine/medical inspection', '船が検疫所に着いたのは'),
        ('所', 4, 'しょ', "(suf,ctr) counter for places", '船が検疫所に着いたのは'),
        ('に', 5, 'に', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)', '船が検疫所に着いたのは'),
        ('着く', 6, 'つく', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)', '船が検疫所に着いたのは'),
        ('た', 8, 'た', '(aux-v) indicate past completed or action/indicates light imperative', '船が検疫所に着いたのは'),
        ('の', 9, 'の', '(prt,fem) indicates possessive/nominalizes verbs and adjectives/substitutes for "ga" in subordinate phrases/(at sentence-end, falling tone) indicates a confident conclusion/(P)', '船が検疫所に着いたのは'),
        ('は', 10, 'は', '(prt) topic marker particle/indicates contrast with another option (stated or unstated)/adds emphasis/(P)', '船が検疫所に着いたのは')
        ]
        #        self.assertEqual(len(expected), len(res))
        self.assertEqual(expected, res)

    def testNoKanji(self):
        self.assertFalse(TextProcessor.hasKanji('が'))
        self.assertTrue(TextProcessor.hasKanji('所'))
        self.assertFalse(TextProcessor.hasKanji('。'))

    def testNoExcessiveReading(self):
        res = self.textProc.do('船が、検疫所に着いたのは', Settings.NoExcessiveReading())
        res = list(res)
        expected = \
        [
        ('船', 0,'ふね', '(n,n-suf,ctr) ship/boat/watercraft/vessel/steamship/tank/tub/vat/trough/counter for boat-shaped containers (e.g. of sashimi)/(P)', '船が、検疫所に着いたのは'),
        ('が', 1, '', '(prt,conj) indicates sentence subject (occasionally object)/indicates possessive (esp. in literary expressions)/but/however/still/and/(P)', '船が、検疫所に着いたのは'),
        ('検疫', 3, 'けんえき', '(n,vs) quarantine/medical inspection', '船が、検疫所に着いたのは'),
        ('所', 5,'しょ', "(suf,ctr) counter for places", '船が、検疫所に着いたのは'),
        ('に', 6, '', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)', '船が、検疫所に着いたのは'),
        ('着く', 7, 'つく', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)', '船が、検疫所に着いたのは'),
        ('た', 9, '', '(aux-v) indicate past completed or action/indicates light imperative', '船が、検疫所に着いたのは'),
        ('の', 10, '', '(prt,fem) indicates possessive/nominalizes verbs and adjectives/substitutes for "ga" in subordinate phrases/(at sentence-end, falling tone) indicates a confident conclusion/(P)', '船が、検疫所に着いたのは'),
        ('は', 11, '', '(prt) topic marker particle/indicates contrast with another option (stated or unstated)/adds emphasis/(P)', '船が、検疫所に着いたのは')
        ]
        #        self.assertEqual(len(expected), len(res))
        self.assertEqual(expected, res)

    def testUnknownWord(self):
        res = self.textProc.do('デッキに昇って行った')
        res = list(res)
        self.assertEqual(6, len(res))
        self.assertEqual('デッキ', res[0][0])
      #  for word, reading, definition, sentence in res:
      #      print(word, reading ,definition)

    def testGetContext(self):
        snt = 'デッキに昇って行った'
        res = self.textProc.getContext(snt, WordInfo('デ', 0, '', 0, '') )
        self.assertEqual(snt, res)

    def testExtentionOfUnknownToken(self):
        res = self.textProc.do('ジーン・モーラの姿は見えなかった。')
        res = list(res)
        self.assertEqual(7, len(list(res)))
        self.assertEqual('ジーン・モーラ', res[0][0])

    def testONReading(self):
        res = self.textProc.do('数時間が')
        res = list(res)
        self.assertEqual(3, len(list(res)))
        self.assertEqual('すう', res[0][2])

    def testMergeTwoNouns(self):
        res = self.textProc.do('検疫所に', Settings.NoExcessiveReading(), True)
        res = list(res)
        self.assertEqual(2, len(list(res)))
        self.assertEqual(('検疫所', 0, 'けんえきじょ'), res[0][0:3])
        self.assertEqual('(n) quarantine station', res[0][3])
        self.assertEqual('に', res[1][0])

    def testMergeTwoVerbs(self):
        res = self.textProc.do('頃にちがいない。', Settings.NoExcessiveReading(), True)
        res = list(res)
        self.assertEqual(3, len(list(res)))
        self.assertEqual(('ちがいない', 2, ''), res[2][0:3])
        self.assertEqual('(exp,adj-i) (phrase) sure/no mistaking it/for certain/(P)', res[2][3])

    def testMergeTwoNumerics(self):
        res = self.textProc.do('が一匹と', Settings.NoExcessiveReading(), True)
        res = list(res)
        self.assertEqual(3, len(list(res)))
        self.assertEqual(('一匹', 1, 'いっぴき'), res[1][0:3])
        self.assertEqual('(n,arch) one animal (small)/two-tan bolt of cloth', res[1][3])

    def testPrefixMerger(self):
        res = self.textProc.do('準強姦の罪に', Settings.NoExcessiveReading(), True)
        res = list(res)
        self.assertEqual(('準強姦', 0, 'じゅんごうかん'), res[0][0:3])

    def testThreeTokenJoin(self):
        result = self.textProc.do('海泡石', Settings.NoExcessiveReading(), True)
        result = list(map(operator.itemgetter(0), result))
        self.assertEquals(['海泡石'], result)

class TextProcessorTest2(unittest.TestCase):
    def setUp(self):
        self.textProc = TextProcessor(getDataLoader())
        self.maxDiff = None

    def testONReadingFailure(self):
        # no word 車 with sha reading
        res = self.textProc.stepOne('逃走車', Settings.NoExcessiveReading())

    def test2(self):
        res = self.textProc.do('電燈', Settings.NoExcessiveReading(), True)
        res = list(res)
        res = res

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TextProcessorTest2)
    unittest.TextTestRunner(verbosity=2).run(suite)