#!/usr/bin/python3
# Combiner

import sys

for line in sys.stdin:
    #for each document create dictionary of words
    word_cnts = dict()
    line = line.strip()
    words = line.split()
    for word in words:
        if word not in word_cnts.keys(): word_cnts[word] = 1
        else: word_cnts[word] += 1
    # emit key-value pairs only for distinct words per document 
    for w in word_cnts.keys():
        print('%s\t%s' % (w, word_cnts[w]))
