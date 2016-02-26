# -*- coding: utf-8 -*-

from __future__ import unicode_literals

OTHER = 0           #
# see ipadict/Fillers.csv
FILLER = 1          # えと, あー
# see ipadict/Interjection.csv
INT = 2             # ふふふ
# symbols, see ipadict/Symbols.csv
ALPHABET = 3        # δ, ←, ￡, etc.
SYMBOL = 4          # ｀, ＼
BRACKET_OPEN = 5    # 【
BRACKET_CLOSE = 6   # ）
PERIOD = 7          # 。．
SPACE = 8           # ' '
COMMA = 9           # ,
# adjective
ADJ = 10
ADJ_SUFFIX = 11
ADJ_NONIND = 12
# particle
PRT_CASE = 13       #
PRT_REF = 14
PRT_PHRASE = 15
PRT_BIND = 16
PRT_END = 17
PRT_CONJUNCT = 18
PRT_SPECIAL = 19
PRT_ADVERB = 20
PRT_ADVERB2 = 21
PRT_ADV_JOIN_END = 22
PRT_JOIN = 23
PRT_PRENOUN = 24
# verb auxillary
VERB_AUX = 25       # た in 所に着いた
# conjunction
CONJ = 26
# prefix
PREFIX_ADJ = 27
PREFIX_NUM = 28
PREFIX_VERB = 29
PREFIX_NOUN = 30
# verb
VERB = 31
VERB_SUFFIX = 32
VERB_NONIND = 33  # 続く, ください
# adv
ADVERB = 34
ADVERB_CON = 35
# noun
NOUN_VSURU = 36
NOUN_ADJROOT = 37
NOUN = 38
NOUN_REF = 39
NOUN_ADJVERB_ROOT = 40
NOUN_PROPER = 41
NOUN_PERSON = 42
NOUN_SURNAME = 43
NOUN_FIRSTNAME = 44
NOUN_ORGANIZATION = 45
NOUN_PLACE = 46
NOUN_COUNTRY = 47
NOUN_NUMERIC = 48
NOUN_JOIN = 49
# noun suffix
NOUN_SUFFIX_VSURU = 50
NOUN_SUFFIX = 51
NOUN_SUFFIX_ADJVERBROOT = 52
NOUN_SUFFIX_COUNTER = 53
NOUN_SUFFIX_AUXVERB = 54
NOUN_SUFFIX_PERSON = 55
NOUN_SUFFIX_PLACE = 56
NOUN_SUFFIX_SPECIAL = 57
NOUN_SUFFIX_ADV = 58
# other noun type
NOUN_PRONOUN = 59
NOUN_PRONOUN_CONTRACTION = 60
NOUN_VERB = 61
NOUN_SPECIAL_PRTROOT = 62
NOUN_NONIND = 63
NOUN_NONIND_ADJVERBROOT = 64
NOUN_NONIND_AUXVERBROOT = 65
NOUN_NONIND_ADVERB = 66
NOUN_ADVERB = 67
# prenoun adjectival
ADJ_PRENOUN = 68    # 大した

def isParticle(pos):
    return pos >= PRT_CASE and pos <= PRT_PRENOUN

def isPrefix(pos):
    return pos >= PREFIX_ADJ and pos <= PREFIX_NOUN

def isNounSuffix(pos):
    return pos >= NOUN_SUFFIX_VSURU and pos <= NOUN_SUFFIX_ADV

def isNoun(pos):
    return pos >= NOUN_VSURU and pos <= NOUN_ADVERB

def isAfterVerb(pos):
    return pos == VERB_AUX or pos == VERB_NONIND or pos == VERB_SUFFIX

def isNotWord(pos):
    """
        Not to skip OTHER!
    """
    return not (pos >= ADJ or pos == FILLER or pos == INT or pos == OTHER)
