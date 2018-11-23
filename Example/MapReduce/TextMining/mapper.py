#!/usr/bin/env python3

# Mapper

import sys
import re
import string

sys.path.insert(0, 'nltk.zip')
import nltk
from nltk.corpus import stopwords
stops = set(stopwords.words('english'))

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    #split each line on whitspace
    data = line.split()
    stemmer = nltk.stem.SnowballStemmer("english")
    for word in data:
        #remove punctuation
        word = word.strip(string.punctuation)
        #remove numbers
        if re.search(r"\d+",word): continue 
        #remove stopwords
        if word.lower() in stops: continue
        #stem<
        word = stemmer.stem(word) 
        if len(word) < 2: continue
        print('%s\t%s' % (word, 1))
