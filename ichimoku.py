# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import sys
import os.path
import logging
import logging.handlers
import argparse
from textproc.textprocessor import TextProcessor, Settings
from textproc.dataloader import getDataLoader
from textproc.deckwords import DeckWords
from mecab.utils import isPy2, text_type

def setupLogger():
    logs_dir = 'logs'
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), logs_dir))
    except OSError:
        pass
    fullPath = os.path.join(os.path.dirname(__file__), logs_dir, 'ichimoku.txt')
    handler = logging.handlers.RotatingFileHandler(fullPath, "a",
                        encoding = "utf-8", maxBytes=1024*512, backupCount=20)
    formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(module)s %(message)s')
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

def openInputFile(fileName):
    if isPy2():
        return open(fileName, 'r')
    else:
        return open(fileName, 'r', encoding='utf-8')

def openOutputFile(fileName):
    if isPy2():
        return open(fileName, 'w')
    else:
        return open(fileName, 'w', encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='Get the list word in the text.')
    parser.add_argument('inputfile', metavar='input file name',
                   help='input file name')
    parser.add_argument('-d', metavar='deck file name', required=False,
                   help='deck file nime')
    parser.add_argument('-t', metavar='tag', required=False,
                   help='optional tag appended to the list')
    parser.add_argument('-o', metavar='output file name', required=False,
                   help='output file name')
    args = parser.parse_args()
    if args.o:
        sys.stdout = open(args.o, 'w', encoding='utf-8')

    setupLogger()
    with openInputFile(args.inputfile) as file:
        contents = file.read()
        if isPy2():
            contents = unicode(contents, 'utf-8')
        textProc = TextProcessor(getDataLoader())
        getUniqueCSVList(textProc, contents, args.d, args.t)

def getUniqueCSVList(textProc, contents, deckFileName, tag):
    if deckFileName:
        deck = DeckWords(deckFileName)
    else:
        deck = None
    if tag is None:
        tag = ''
    allWords = set()
    for word, startPos, reading, definition, sentence in textProc.do(contents, Settings.NoExcessiveReading(), True):
        if word in allWords or not definition  or deck and deck.isInDeck(word):
            continue
        else:
            allWords.add(word)
        line = text_type('"{0:}";"{1:}";"{2:}";"{3}";"{4}"').format(word, reading, definition,sentence, tag)
        if isPy2():
            print(line.encode('utf-8'))
        else:
            print(line)

def dryBurn():
    from pkgutil import iter_modules
    a=iter_modules()
    while True:
        try: x=a.next()
        except: break
        print (x[1], '<br>')

    setupLogger()
    contents = '船が検疫所に着いたのは'
    textProc = TextProcessor(getDataLoader())
    for word, reading, definition, sentence in textProc.do(contents, Settings.NoExcessiveReading(), True):
        line = text_type('{0:<10}  {1:<10}  {2:<10}  {3}\n').format(word, reading, definition,sentence)
        line = line.strip('\n')
        print(line.encode('utf-8'))


if __name__ == '__main__':
   main()
   #dryBurn()
