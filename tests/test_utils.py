# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from mecab import utils

class UtilsTest(unittest.TestCase):
    def testExtractString(self):
        res = utils.extractString(b'sample\x00\x00\x00')
        self.assertEqual('sample', res)

    def testPy(self):
        res = utils.isPy2x6()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)