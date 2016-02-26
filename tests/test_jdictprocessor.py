# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
from textproc.jdictprocessor import JDictProcessor
from textproc.dartsdict import DartsDictionary
from textproc.dataloader import getDataLoader
import mecab.partofspeech as PoS
from mecab.writer import WordInfo
from textproc.intwordinfo import IntermediateWordInfo

class JDictProcessorTest(unittest.TestCase):
    def setUp(self):
        dictionary = DartsDictionary(getDataLoader().load('jdict'))
        self.processor = JDictProcessor(dictionary)

    def testDifferentReadingsSameWord(self):
        """
        新所帯|||あらじょたい|||(n) new household/new home
        新所帯|||しんじょたい|||(n) new household/new home
        新所帯|||しんしょたい|||(n) new household/new home
        """
        pass

    def testJoinReadings(self):
        """
        大君|||たいくん|||(n) liege lord/shogunate
        大君|||おおきみ|||(n) emperor/king/prince
        大君|||おおぎみ|||(n) emperor/king/prince
        """

    def testRemovePartitialDuplicates(self):
        """
        黒桧|||くろべ|||(n,uk) Japanese arborvitae (Thuja standishii)
        黒桧|||くろび|||(n,uk) Japanese arborvitae (Thuja standishii)
        黒桧|||くろべ|||黒桧 [クロベ] /(n,uk) Japanese arborvitae (Thuja standishii)/
        """

    def testBestChoice(self):
        definitions = \
        [( 'に', '(n) load/baggage/cargo/freight/goods/burden/responsibility/(P)'),
         ( 'に', '(suf) takes after (his mother)'),
         ( 'に', '(n) red earth (i.e. containing cinnabar or minium)/vermilion)'),
         ( 'に', '(num) two/(P)'),
         ( 'に', '(prt) indicates such things as location of person or thing, location of short-term action, etc./(P)')]
        res = self.processor.getBestAlternative(definitions, PoS.PRT_CASE)
        self.assertEqual(definitions[-1], res)

    def testEqualMatch(self):
        definitions = \
        [ ('着く', '(v5k) to arrive at/to reach/to sit on/to sit at (e.g. the table)/(P)'),
          ('着く', '(v5k,vt) to put on (or wear) lower-body clothing ')
        ]
        res = self.processor.getBestAlternative(definitions, PoS.VERB)
        self.assertEqual(definitions[0], res)

    def testMergeNoun(self):
        a = IntermediateWordInfo( '検疫', 0, PoS.NOUN_VSURU, 'xx','')
        b = IntermediateWordInfo( '所', 2, PoS.NOUN_SUFFIX, 'xx','')
        newWord = self.processor.mergeWords([a, b])
        expected = IntermediateWordInfo('検疫所', 0, PoS.NOUN, 'けんえきじょ', '(n) quarantine station')
        self.assertEqual(newWord, [expected])

    def testMergeNoun3Kanji(self):
        a = IntermediateWordInfo( '数', 0, PoS.NOUN_VSURU, 'xx', '')
        b = IntermediateWordInfo( '時間', 1, PoS.NOUN_SUFFIX, 'xx', '')
        newWord = self.processor.mergeWords([a, b])
        expected = IntermediateWordInfo('数時間', 0, PoS.NOUN, 'すうじかん', '(n) a few hours/(P)')
        self.assertEqual(newWord, [expected])

    def testMergeNoun4Kanji(self):
        a = IntermediateWordInfo( '予算', 0,  PoS.NOUN, 'xx', '')
        b = IntermediateWordInfo( '補正', 2, PoS.NOUN, 'xx', '')
        newWord = self.processor.mergeWords([a, b])
        self.assertIsNotNone(newWord)

    def testSelectNounOnReading(self):
        a = WordInfo('所' , 0, '所', PoS.NOUN_SUFFIX, 'ショ')
        allWords = self.processor.dictionary.getAllReadingAndDefinition('所')
        newWord = self.processor.filterOnReading(allWords, a.kanaReading)[0]
        self.assertEqual(newWord, ('しょ', '(suf,ctr) counter for places'))

    def testMergeVerbs(self):
        a = IntermediateWordInfo('ちがい' , 0, PoS.VERB, '', '')
        b = IntermediateWordInfo('ない' , 0, PoS.VERB_AUX, '', '')
        newWord = self.processor.mergeWords([a, b])
        self.assertIsNotNone(newWord)

    def testMergeVerbs2(self):
        a = IntermediateWordInfo('滲み' , 0, PoS.VERB, 'シミ', '')
        b = IntermediateWordInfo('込み' , 0, PoS.VERB_NONIND, 'コミ', '')
        newWord = self.processor.mergeWords([a, b])
        self.assertIsNotNone(newWord)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JDictProcessorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)