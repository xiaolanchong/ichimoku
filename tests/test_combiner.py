# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from textproc.combiner import Combiner

class StrCombiner(Combiner):
    def __init__(self):
        Combiner.__init__(self)
        self.rules = {  'aa' : 'b',
                        'bb' : 'c',
                        'da' : 'a'}

    def isDelimiter(self, a):
        return ',.!?'.find(a) != -1

    def combine(self, a, b):
        return self.rules.get(a + b)

class CombinerTest(unittest.TestCase):
    def setUp(self):
        self.combiner = StrCombiner()

    def testDelimiter(self):
        res = self.combiner.process('a,b,c')
        self.assertEqual(['a',',','b',',','c'], res)
        res = self.combiner.process('a,,c')
        self.assertEqual(['a',',',',','c'], res)
        res = self.combiner.process('a,,,')
        self.assertEqual(['a',',',',',','], res)

    def testOneStepCombine(self):
        res = self.combiner.process(['a','a','c'])
        self.assertEqual(['b','c'], res)
        res = self.combiner.process(['a',',','a','a','c'])
        self.assertEqual(['a',',','b','c'], res)
        res = self.combiner.process(['a',',','a','a','d','a'])
        self.assertEqual(['a',',','b','a'], res)

    def testTwoStepCombine(self):
        res = self.combiner.process(['a','a','b'])
        self.assertEqual(['c'], res)
        res = self.combiner.process(['a',',','a','a','b'])
        self.assertEqual(['a',',','c'], res)
        res = self.combiner.process(['a',',','a','a','b','a'])
        self.assertEqual(['a',',','c','a'], res)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CombinerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)