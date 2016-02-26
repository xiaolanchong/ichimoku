# -*- coding: utf-8 -*-

expr = 'すべてに滲《し》み込み'
with open('test_unk.txt', 'wb') as outFile:
    outFile.write(expr.encode("euc-jp", "ignore"))

with open('mecab_test.txt', 'r', encoding='euc-jp') as mecabFile:
    print(mecabFile.readline())