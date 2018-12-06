# Setup Spark

* Version here: 2.4.0

> Current version of Spark natively contain pre-built Scala binary.

Current installation process is for [Spark Standalone Mode](https://spark.apache.org/docs/latest/spark-standalone.html)

## Download spark

```sh
fab download-spark
```

## Install Spark

```sh
fab install-spark -v
```

Test

```txt
$ fab ssh-connect 0 -h # connect to master

$ spark-shell
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.4.0
      /_/
scala> sc.version
res0: String = 2.4.0
scala> :quit
```

### Install PySpark

[pyspark](https://pypi.org/project/pyspark/)

### Configure for Pi Cluster

spark-env.sh

Memory...

TBD

slaves

like Hadoop workers

## Submit Application

[Spark - Submitting Applications](https://spark.apache.org/docs/latest/submitting-applications.html)

## Job History

* [Spark - Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html)
* [Mastering Apache Spark - Spark History Server](https://jaceklaskowski.gitbooks.io/mastering-apache-spark/spark-history-server.html)
* [IBM - Enabling the Spark History service](https://www.ibm.com/support/knowledgecenter/en/SSGSMK_7.1.1/management_sym/spark_configuring_history_service.html)

## Links

* [Official Website](https://spark.apache.org/)
* [Spark Github](https://github.com/apache/spark)

### Book

* [Mastering Apache Spark](https://legacy.gitbook.com/book/jaceklaskowski/mastering-apache-spark/details)
