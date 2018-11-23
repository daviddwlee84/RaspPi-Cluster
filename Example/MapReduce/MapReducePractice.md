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
## Example 1
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

![Example 2](https://cdn-images-1.medium.com/max/800/0*it9fFvZ5h2eFL2e3.jpg)

```sh
## Example 2
# Go to project directory
$ cd GeneralWordCount
# Try mapper
$ echo "X B B\nC B A\nX A C\n" | ./mapper.py
X       1
B       1
B       1
C       1
B       1
A       1
X       1
A       1
C       1
# Try entire procedure
$ echo "X B B\nC B A\nX A C\n" | ./mapper.py | sort -k1,1 | ./reducer.py
A       2
B       3
C       2
X       2
```

### Generator Version - Ebook example

* [mapper.py](GeneratorWordCount/mapper.py)
* [reducer.py](GeneratorWordCount/reducer.py)

**Without Hadoop Steps**:

```sh
# Go to project directory
$ cd GeneratorWordCount
# Download Data (already downloaded in data/)
$ bash download_data.sh
# Analysis
$ cat data/*.txt | ./mapper.py | ./reducer.py
```

## Daily Exchange Rate

* [mapper.py](DailyExchangeRate/mapper.py)
* [reducer.py](DailyExchangeRate/reducer.py)

**Without Hadoop Steps**:

```sh
# Go to project directory
$ cd DailyExchangeRate
# Download Data (already downloaded in data/)
$ bash download_data.sh
# Analysis
$ cat data/daily.csv | python3 mapper.py | python3 reducer.py
```

## Word Count and Text Mining

### Word Count with Combine Step

* [mapper.py](WordCountCombine/mapper.py)
* [combiner.py](WordCountCombine/reducer.py) -> TBD
* [reducer.py](WordCountCombine/reducer.py)

**Without Hadoop Steps**:

```sh
# Go to project directory
$ cd WordCountCombine
# Download Data (already downloaded in data/)
$ bash download_data.sh
# Analysis (without combine)
$ cat data/44604.txt.utf-8 | python3 mapper.py | sort -k1,1 | python3 reducer.py
# Analysis (with combine)
# TBD
```

### Text Mining

**Without Hadoop Steps**:

TBD