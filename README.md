# Ichimoku
Ichimoku is Tool to extract from a Japanese text unique words accompanied by definitions of JDIC, based on Mecab app (https://en.wikipedia.org/wiki/MeCab) ported to pure python3.

Usage:
`ichimoku.py inputfile [-o output file name] [-d deck name] [-t tag]
inputfile - input text file,
output file name - output tsv file,
deck name - text file consist of lines: word <tab> definition, suited for an exported Anki deck, to skip known words,
tag - the final value for all records, useful for Anki export.`

E.g.
`ichimoku.py -o output.txt -t wagahai input.txt`

input.txt:
   吾輩は猫である。名前はまだ無い。

output.txt:
"吾輩";"わがはい";"(pn,adj-no,arch,male) I (nuance of arrogance)/me/myself/we/us/ourselves";"吾輩は猫である";"wagahai"
"は";"";"(prt) topic marker particle/indicates contrast with another option (stated or unstated)/adds emphasis/(P)";"吾輩は猫である";"wagahai"
"猫";"ねこ";"(n,abbr,uk,col) cat/shamisen/geisha/wheelbarrow/clay bed-warmer/submissive partner of a homosexual relationship/(P)";"吾輩は猫である";"wagahai"
"だ";"";"(aux,aux-v) be/is/indicates past or completed action/indicates light imperative/(P)";"吾輩は猫である";"wagahai"
"ある";"";"(v5r-i,vi,uk) to be (usu. of inanimate objects)/to exist/to live/to have/to be located/to be equipped with/to happen/to come about/(P)";"吾輩は猫である";"wagahai"
"名前";"なまえ";"(n) name/full name/given name/first name/(P)";"名前はまだ無い";"wagahai"
"まだ";"";"(adj-na,adv,uk) as yet/hitherto/still/not yet (with negative verb)/(P)";"名前はまだ無い";"wagahai"
"無い";"ない";"(adj-i,uk,aux-adj) nonexistent/not being (there)/unpossessed/unowned/not had/unique/indicates negation, inexperience, unnecessariness or impossibility/(after the ren'youkei form of an adjective) not .../(P)";"名前はまだ無い";"wagahai"


