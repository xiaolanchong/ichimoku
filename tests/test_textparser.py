# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('..'))
import textproc.textparser as textparser

class ParserTest(unittest.TestCase):
    #@unittest.skip("temp skipping")
    def testNarration(self):
        textToParse = \
        """
        ジーンの船室、だった。
        ノックをしたところでなんになる？
        　メグレは船室にもどった。
        それから酒を飲んだ……
        """
        p = textparser.TextParser(textToParse)
        result = [
            "ジーンの船室、だった",
            "ノックをしたところでなんになる",
            "メグレは船室にもどった",
            "それから酒を飲んだ"
            ]
        self.assertEqual(result, list(p.getSentences()))

   # @unittest.skip("temp skipping")
    def testDirectSpeach(self):
        textToParse = \
        "「怒るって何をだね？" \
        "よくご存じでしょう……" \
        "」"
        p = textparser.TextParser(textToParse)
        result = [
            "怒るって何をだね",
            "よくご存じでしょう"
            ]
        self.assertEqual(result, list(p.getSentences()))

    def testSpacesBeforeSpeachMark(self):
       textToParse = \
       """　ジョン・モーラは背は普通以下の、小柄なそうだった。
             「私に何かご用ですか？
            」
       """
       p = textparser.TextParser(textToParse)
       result = [
            "ジョン・モーラは背は普通以下の、小柄なそうだった",
            "私に何かご用ですか"
            ]
       self.assertEqual(result, list(p.getSentences()))

    def testRemoveFurigana(self):
        p = textparser.TextParser('錨《いかり》の騒々しい物音', True)
        self.assertEqual(['錨の騒々しい物音'], p.getSentences())
        p = textparser.TextParser('錨の騒々《そうぞう》しい物音', True)
        self.assertEqual(['錨の騒々しい物音'], p.getSentences())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

