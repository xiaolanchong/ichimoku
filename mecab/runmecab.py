# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys, os, platform, re, subprocess
from mecab.utils import text_type, isPy2
import time

isWin = sys.platform == "win32"

def getStartupInfo():
    if isWin:
        si = subprocess.STARTUPINFO()
        try:
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        except:
            si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
    else:
        si = None

def mungeForPlatform(popen):
    if isWin:
        popen = [os.path.normpath(x) for x in popen]
        popen[0] += ".exe"
    elif not isMac:
        popen[0] += ".lin"
    return popen

class MecabRunner(object):
    def __init__(self, nodeFormat='%m,%f[6]', eosNodeFormat='\n', unknownNodeFormat='[%m]'):
        self.mecab = None
        self.lineDelimiter = '|'
        self.mecabArgs = ['--node-format=' + nodeFormat + self.lineDelimiter,
                          '--eos-format=' + eosNodeFormat + self.lineDelimiter,
                          '--unk-format=' + unknownNodeFormat + self.lineDelimiter,
                          ]

    def setup(self):
        currentDir = os.path.dirname(__file__)
        base = os.path.abspath(os.path.join(currentDir, '..', 'support'))
        mecabExe = os.path.join(base, 'mecab')
        mecabRc = os.path.join(base, 'mecabrc')
        self.mecabCmd = mungeForPlatform(
            [mecabExe] + self.mecabArgs + ['-d', base, '-r', mecabRc])
        os.environ['DYLD_LIBRARY_PATH'] = base
        os.environ['LD_LIBRARY_PATH'] = base
        if not isWin:
            os.chmod(self.mecabCmd[0], 0o755)

    def ensureOpen(self):
        if not self.mecab:
            self.setup()
            try:
                self.mecab = subprocess.Popen(
                    self.mecabCmd, bufsize=-1, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    startupinfo=getStartupInfo())
            except OSError:
                raise Exception("Please install mecab")

    def run(self, expr):
        self.ensureOpen()
        expr += '\n'
        self.mecab.stdin.write(expr.encode("euc-jp", "ignore"))
        self.mecab.stdin.flush()
        exprFromMecab = text_type(self.mecab.stdout.readline(), "euc-jp")
        exprFromMecab = exprFromMecab.rstrip('\r\n')
        return exprFromMecab.split(self.lineDelimiter)[:-1]

class MecabOutputGetter(MecabRunner):
    def __init__(self):
        fmt = '%m,%f[6],[pos],%h,[cost],%pw,%pC,%pc,%phl,%phr,'\
              '[l2]%pb,%P,%pP,%pA,%pB'
        MecabRunner.__init__(self, fmt, '\n', '=' + fmt)

    def run(self, expr):
        lines = MecabRunner.run(self, expr)
        res = []
        for line in lines:
            node = self.getParam(line)
            if node:
                res.append(node)
        return res


    def getParam(self, expr):
        if len(expr) == 0:
            return
        m = re.match('\=?(.+?),(.*?),\[pos\],(\d+),\[cost\],(-?\d+),(-?\d+),(-?\d+),(-?\d+),(-?\d+),\[l2\].*', expr, re.S)
        if m:
            morphema, dictForm, pos, wordCost, linkCost, totalCost, leftAttr, rightAttr = m.groups()
            return [morphema, dictForm, pos, wordCost, linkCost, totalCost, leftAttr, rightAttr]
        else:
            raise RuntimeError('Incorrect mecab output: ' + expr)

def getPartOfSpeech():
    runner = MecabRunner('%m,%f[7]')
    res = runner.run('雨が降っていたん')
    #res = runner.run('海泡石')
    for line in res:
        if not isPy2():
            print(''.join(line))

def dumpNodeInfo():
    runner = MecabOutputGetter()
    #z = bytearray('－・', 'euc-jp', "ignore")
    res = runner.run('雨が降っていたん')
   # res = runner.run('すべてに滲《し》み込み')
    for line in res:
        if not isPy2():
            print(' '.join(line))

if __name__ == '__main__':
    getPartOfSpeech()
    #dumpNodeInfo()
