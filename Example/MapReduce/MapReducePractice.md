# MapReduce Practice

## Overview

Practice|Detail|Reference
--------|------|---------
[Word count](#Word-Count)|Simple word count and generator version example|[link](https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/)
[Daily exchange rate](#Daily-Exchange-Rate)|Output currency FX change day to day as a percentage|[link](https://medium.com/@rrfd/your-first-map-reduce-using-hadoop-with-python-and-osx-ca3b6f3dfe78)
[Word count and Text mining](#Word-Count-and-Text-Mining)|Two example: word count with combine step and simple NLP|[link](https://researchcomputing.princeton.edu/computational-hardware/hadoop/mapred-tut)

## Word Count

### General Version - Simple example

* [mapper.py](GeneralWordCount/mapper.py)
* [reducer.py](GeneralWordCount/reducer.py)

**Steps**:

```sh
# Go to project directory
$ cd GeneralWordCount
# Try mapper
$ echo "foo foo quux labs foo bar quux" | ./mapper.py
foo     1
foo     1
quux    1
labs    1
foo     1
bar     1
quux    1
# Try entire procedure
$ echo "foo foo quux labs foo bar quux" | ./mapper.py | sort -k1,1 | ./reducer.py
bar     1
foo     3
labs    1
quux    2
```

### Generator Version - Ebook example

* [mapper.py](GeneratorWordCount/mapper.py)
* [reducer.py](GeneratorWordCount/reducer.py)

**Without Hadoop Steps**:

```sh
# Go to project directory
$ cd GeneratorWordCount
# Download Data
$ bash download_data.sh
# Analysis
$ cat *.txt | ./mapper.py | ./reducer.py
```

## Daily Exchange Rate

**Without Hadoop Steps**:

## Word Count and Text Mining

### Word Count with Combine Step

**Without Hadoop Steps**:

### Text Mining

**Without Hadoop Steps**:
