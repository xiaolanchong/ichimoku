# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import io
import os
import os.path
import sys

sys.path.append(os.path.abspath('..'))
from mecab.viterbi import Viterbi
#from mecab.node import Node
#from mecab.token import Token
from mecab.runmecab import MecabOutputGetter
from mecab.writer import Writer
from mecab.utils import text_type, isPy2
from textproc.dataloader import getDataLoader

class ResultContainer:
    def __init__(self, fileName):
        self.file = io.open(fileName ,'w', encoding='utf-8', buffering=1)

    def print(self, line):
        self.file.write(text_type(line))
        self.file.write('\n')

class Helper:
    def outputNodes(self, nodes):
        return '\n'.join([str(node) for node in nodes])

    def maketransU(self, s1, s2):
        trans_tab = dict( zip( map(ord, s1), map(ord, s2) ) )
        #trans_tab.update( (ord(c),None) for c in todel )
        return trans_tab

    def fixEncodingError(self, text):
        # try to fix
        # －  -> ー
        # ～  ->  ~
        fromChars = '－～〝〟'
        toChars = 'ー~""'
        if isPy2():
            table = self.maketransU(fromChars, toChars)
            pos = 0
            while pos < len(text):
                ch = table.get(ord(text[pos]), None)
                if ch is not None:
                    text = text[:pos] + unichr(ch) + text[pos+1:]
                pos += 1
            return text
        else:
            table = text_type.maketrans(fromChars, toChars)
            text = text.translate(table)
        return text
        # detect errors
        try:
            bytearray(text, 'euc-jp')
        except UnicodeEncodeError as u:
            raise RuntimeError(text + ': ' + str(e))
        # ignore
        if False:
            b = bytearray(text, 'euc-jp', 'ignore')
            return text_type(b)

class MecabCompareTest(unittest.TestCase):
    def setUp(self):
        self.viterbi = Viterbi(getDataLoader())
        self.maxDiff = None

    @unittest.skip("temp skipping")
    def testEntireFile(self):
        resAccumulator = ResultContainer('maigrat_rep.txt')
        self.compareOnFile(r'../testdata/other/MaigraitInNewYork_ch1.txt', 'utf-8', resAccumulator)
        self.compareOnFile(r'../testdata/other/MaigraitInNewYork.txt', 'utf-8', resAccumulator)

    #@unittest.skip("temp skipping")
    def testDirContents(self):
        resAccumulator = ResultContainer('dir_report.txt')
        baseDir = r'c:\project\temp_for_mecab\1'
        dirList = os.listdir(baseDir)
        txtFiles = list(filter(lambda x: x.endswith('.txt'), dirList))
        for fileName in txtFiles[:3]:
            self.compareOnFile(os.path.join(baseDir, fileName), 'shift-jis', resAccumulator)

    def readFile(self, fileName, encoding, resAccumulator):
        with io.open(fileName, 'rb') as inFile:
            contents = inFile.read()
        contents = contents.split(b'\r\n')
        lineNum = 1
        encodingError = 0
        resAccumulator.print(fileName)
        for line in contents:
            try:
                text = line.strip()
                text = text_type(line, encoding)
                lineNum += 1
                yield text
            except UnicodeDecodeError as u:
                encodingError += 1
                resAccumulator.print('line {0}, pos {1}: encoding error'.format(lineNum, u.start))

    def testFixEncoding(self):
        helper = Helper()
        z = helper.fixEncodingError('11～22')
        self.assertEqual(z, '11~22')

    def compareOnFile(self, fileName, encoding, resAccumulator):
        helper = Helper()
        writer = Writer()
        runner = MecabOutputGetter()
        lineNum = 1
        for line in self.readFile(fileName, encoding, resAccumulator):
                text = line.strip()
                #if isPy2():
                #    text = text_type(text)
                if encoding == 'utf-8':
                    text = helper.fixEncodingError(text)
                nodes = self.viterbi.getBestPath(text)

                pyResult = writer.getMecabOutput(self.viterbi.getTokenizer(), nodes)
                try:
                    #runner = MecabOutputGetter()
                    mecabResult = runner.run(text)
                except IOError as e:
                    resAccumulator.print(text_type(e))
                    continue
                try:

                    self.assertEqual(len(mecabResult), len(pyResult),
                        text + '\npyPort:\n' + helper.outputNodes(pyResult) +
                         '\nmecab:\n' + helper.outputNodes(mecabResult))
                    for i in range(len(mecabResult)):
                        self.assertEqual(mecabResult[i], pyResult[i], "at line " + str(lineNum) + ": '" + line + "'")
                except AssertionError as e:
                    resAccumulator.print(text_type(e))
                lineNum += 1
                if lineNum % 500 == 0:
                    resAccumulator.print(text_type(lineNum) + ' lines have been processed')
        resAccumulator.print(text_type(lineNum) + ' lines have been processed')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MecabCompareTest)
    unittest.TextTestRunner(verbosity=2).run(suite)