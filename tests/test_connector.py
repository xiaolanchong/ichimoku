# -*- coding: utf-8 -*-

import unittest
import os.path
import sys
sys.path.append(os.path.abspath('..'))
from mecab.connector import Connector
from textproc.dataloader import getDataLoader

class ConnectorTest(unittest.TestCase):
    def testSimple(self):
        con = Connector(getDataLoader())
        self.assertEqual(-5447, con.getCost(1283, 1298))
        with self.assertRaises(RuntimeError):
            con.getCost(-1, 101)
        with self.assertRaises(RuntimeError):
            con.getCost(1, 100000001)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConnectorTest)
    unittest.TextTestRunner(verbosity=2).run(suite)