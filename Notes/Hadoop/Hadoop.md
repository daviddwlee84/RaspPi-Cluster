# Hadoop

## Hadoop Fundamentals

### HDFS

### YARN

### MapReduce

### Spark

### Hive

### Pig

### HBase

### Sqoop

### MongoDB

### Hadoop Security

## Hadoop Streaming

Hadoop provides a streaming API which supports any programming language that can read from the standard input *stdin* and write to the standard output *stdout*. The Hadoop streaming API uses standard Linux streams as the interface between Hadoop and the program.  Thus, input data is passed via the *stdin* to a map function, which processes it line by line and writes to the *stdout*.  Input to the reduce function is *stdin* (which is guaranteed to be sorted by key by Hadoop) and the results are output to *stdout*.

* Hadoop provides an API to MapReduce that allows you to write your map and reduce functions in languages other than Java!
* Hadoop Streaming use Unix standard streams as the interface between Hadoop and your program, so you can use any language that can read standard input and write to standard output to write your MapReduce program.

**Little trick** (set in `~/.bashrc` of hadoop user)

```sh
run_mapreduce() {
    hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-*streaming*.jar -mapper $1 -reducer $2 -file $1 -file $2 -input $3 -output $4
}

alias hs=run_mapreduce
```

then you can use it

```sh
hs mapper.py reducer.py hdfs_data_in hdfs_data_out
```

* "hdfs_data_out" is the output data folder, it is important that this folder doesn't already exist

## Book

Hadoop - The Definitive Guide

## Links

### Article

* [**Hadoop**](https://docs.deistercloud.com/Technology.50/Hadoop/index.xml?embedded=true&navbar=0&param-iframe=index-iframe)
    * [Hadoop cluster setup](https://docs.deistercloud.com/Technology.50/Hadoop/index.xml)
* [**Big Data And Hadoop**](http://www.micacomputers.co.in/bigdata_hadoop.php)

### Getting Started

* [**How to Install and Set Up a 3-Node Hadoop Cluster**](https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/)

macOS installation guide

* [How to install Hadoop|Spark on macOS High Sierra](http://hanslen.me/2018/01/19/How-to-install-Hadoop-on-macOS-High-Sierra/)
* [Slide - Install Apache Hadoop on Mac OS Sierra](https://www.slideshare.net/SunilkumarMohanty3/install-apache-hadoop-on-mac-os-sierra-76275019)

### Sandbox

* [Hortonworks Sandbox](https://hortonworks.com/products/sandbox/) - The Sandbox is a straightforward, pre-configured, learning environment that contains the latest developments from Apache Hadoop, specifically the Hortonworks Data Platform (HDP).
    * [Sandbox Deployment and Install Guide](https://hortonworks.com/tutorial/sandbox-deployment-and-install-guide/)
