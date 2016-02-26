# -*- coding: utf-8 -*-

import unittest
from jmdictconverter import getMixedRecords

class JMDictConverterTest(unittest.TestCase):
    def testKanjiKanaRecordList(self):
        word = ['御襁褓気触れ', 'お襁褓気触れ',
                'オムツ気触れ', 'おむつかぶれ',
                'オムツかぶれ']
        records = getMixedRecords(word)
        result = [ ('御襁褓気触れ', 'おむつかぶれ'),
                   ('お襁褓気触れ', 'おむつかぶれ'),
                   ('オムツ気触れ', 'おむつかぶれ'),
                   ('オムツかぶれ', 'おむつかぶれ')
                ]
        self.assertEquals(records, result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(JMDictConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)