# Setup Hadoop

* Version here: 3.1.1

## Download Hadoop

We first download Hadoop from official website to `temp_files/`

* [Hadoop releases](https://hadoop.apache.org/releases.html#Download)
* [Apache Hadoop 3.1.1 Mirror](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz)

```sh
fab download-hadoop
```

### Configure

(if download different version, you should modify some settings in fabfile.py)

* `HADOOP_VERSION`

## Install Hadoop

(to see more message use `-v` flag)

```sh
fab install-hadoop
```

### Setup hadoop user name and group

1. Add hadoop group
2. Add hadoop user to hadoop group
3. Add hadoop user to sudo group

### Generate ssh key for hadoop user

1. Generate ssh key and corresopnding authorized_keys in local (`./temp_files/hadoopSSH`)
2. Upload keys to remote by using hadoop user
    * it will first remove files to make sure it's the newest version

### Upload, unpack and change owner

1. Upload hadoop-3.1.1.tar.gz to each node
2. Extract it
3. Move to /opt
4. Change owner to hadoop group and user

```py
# SerialGroupt.put() is still pending
# https://github.com/fabric/fabric/issues/1800
# https://github.com/fabric/fabric/issues/1810
# (but it is in the tutorial... http://docs.fabfile.org/en/2.4/getting-started.html#bringing-it-all-together)
```

### Setup environment variable

1. Append setting in /etc/bash.bashrc
2. Source it to apply setting
3. Also configure in $HADOOP_HOME/etc/hadoop/hadoop-env.sh
    * JAVA_HOME
    * HADOOP_HEAPSIZE_MAX

### Setup slaves (worker)

1. Add master hostname address in $HADOOP_HOME/etc/hadoop/master
2. Add slaves hostname address in $HADOOP_HOME/etc/hadoop/workers

> Ps. in Hadoop 2.x it is $HADOOP_HOME/etc/hadoop/slaves

### Update hadoop configuration

Use [update-hadoop-conf](#Update-hadoop-configuration-files)

## Setup HDFS

1. Make directories and change their owner
2. Format HDFS namenode

## Update hadoop configuration files

Update these files to the remotes: (will overwrite the original content)

* core-site.xml
* mapred-site.xml
* hdfs-site.xml
* yarn-site.xml

```sh
fab update-hadoop-conf
```

## Fix native library error

(use `-c` flag to clean up tar and build file when it's finished)

```sh
fab fix-hadoop-lib
```

> THIS METHOD IS STILL IN TEST PHASE

## TODO

* fix IP (maybe)
* make another .md about how to configure hadooop configure file
    * node number dynamic config (hostname or something else)

## Trouble Shooting

### Fix library (Cannot allocate memory)

**Preface**: I've test my hadoop by official example. But I can't finish the calculate-PI example even it reach 100% map 100% reduce. But I can successful running wordcount. It's wierd. So I tried to solve the library problem see if these can solve it.

```txt
Java HotSpot(TM) Client VM warning: You have loaded library /opt/hadoop-3.1.1/lib/native/libhadoop.so.1.0.0 which might have disabled stack guard. The VM will try to fix the stack guard now.
It's highly recommended that you fix the library with 'execstack -c <libfile>', or link it with '-z noexecstack'.
Java HotSpot(TM) Client VM warning: INFO: os::commit_memory(0x52600000, 104861696, 0) failed; error='Cannot allocate memory' (errno=12)
```

```sh
# I've tried to fix it by execstack but it doesn't work
sudo apt-get install execstack
sudo execstack -c /opt/hadoop-3.1.1/lib/native/libhadoop.so.1.0.0
```

```sh
# Some other said that they can fix it by adding these two environment variable in hadoop-env.sh but still doesn't work
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_HOME/lib/"
export HADOOP_COMMON_LIB_NATIVE_DIR="$HADOOP_HOME/lib/native/"
```

* [Compile Apache Hadoop on Linux (fix warning: Unable to load native-hadoop library)](http://www.ercoppa.org/posts/how-to-compile-apache-hadoop-on-ubuntu-linux.html) - Steps
* [Hadoop “Unable to load native-hadoop library for your platform” warning](https://stackoverflow.com/questions/19943766/hadoop-unable-to-load-native-hadoop-library-for-your-platform-warning) - Reason explain
    * By default the library in binary version hadoop is built for 32-bit.
    * Check if the *.so file is readable `ldd libhadoop.so.1.0.0`
* [Building Native Hadoop Libraries to Fix VM Stack Guard error on 64 bit machine](https://kuntalganguly.blogspot.com/2014/07/building-native-hadoop-libraries-to-fix.html) - Steps but a little outdated

```sh
# Get hadoop build tools
sudo apt-get install maven libssl-dev build-essential pkgconf cmake
# Get protobuf build tools
sudo apt-get install -y autoconf automake libtool curl make g++ unzip
```

> I've tried to install libprotobuf10(latest version) and protobuf-compiler by apt-get but it get the error...
> (libprotobuf8 didn't found)

```txt
[ERROR] Failed to execute goal org.apache.hadoop:hadoop-maven-plugins:3.1.1:protoc (compile-protoc) on project hadoop-common: org.apache.maven.plugin.MojoExecutionException: protoc version is 'libprotoc 3.0.0', expected version is '2.5.0'
```

**Build Protocol Buffers**: It has to be v2.5.0

> Follow [Official C++ Installation of Protocol Buffers](https://github.com/protocolbuffers/protobuf/blob/master/src/README.md). Build protobuf from binary. (This won't work because the version is too new)

Download binary version of Protocol Buffer v2.5.0 - [Github release page](https://github.com/protocolbuffers/protobuf/releases/tag/v2.5.0)

1. Method 1

Haven't success yet

```sh
./configure
make
sudo make install
# Now it should be able to build hadoop without error
mvn package -Pdist,native -DskipTests -Dtar
```

2. Method 2

Haven't success yet

```sh
./configure
make
cd hadoop-src-3.1.1/hadoop-common-project/hadoop-common
export HADOOP_PROTOC_PATH=/path/to/protobuf-2.5.0/src/protoc
export JAVA_HOME=/usr/lib/jvm/jdk-8-oracle-arm32-vfp-hflt # without /jre
mvn compile -Pnative
```

> When it's finished, copy `lib` folder to wherever you like and remember to add environment variable in `hadoop-env.sh`.

**THE FINAL SOLUTION**:

Before this I'm trying to use the minimum settings among blablabla.xml files in order to observe the functionality and only add it when I needed.

I think OS killed the map since it exceed the maxmum usage. So that's why I get the 'Cannot allocate memory' error.

And now I found that. If hadoop said it can't use "stack grard" to protect memory usage, maybe I can limit it by myself.

So I add some memory limitation configure in mapred-site.xml and yarn-site.xml. And it work perfect!!

Thus I'm not going to get rid of the warning now. :P

([Configure Memory Allocation](https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/#configure-memory-allocation))

[![The YARN Memory Allocation Properties](https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/hadoop-2-memory-allocation-new.png)](https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/#the-memory-allocation-properties)

([Determine HDP Memory Configuration Settings](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.3.0/bk_installing_manually_book/content/determine-hdp-memory-config.html))

### Hostname Problem

I finally found that. Maybe the ApplicationMaster or somewhat can't not communicate with other nodes. (That I've read the logs and found that only the map on the one node can be successful others will fail.)

So the conlcusion is. You have to comment the self direction (i.e. `127.0.1.1 hostname`)
And set all the other nodes' hostname including itself to `/etc/hosts`

> I haven't find out why I can't set it to be hostname.local because I really don't like hard-code things...

* [**Hadoop Wiki - Connection Refused**](https://wiki.apache.org/hadoop/ConnectionRefused)
* [**Network setup - The hostname resolution**](https://www.debian.org/doc/manuals/debian-reference/ch05.en.html#_the_hostname_resolution)

#### Multicast DNS (mDNS)

* [Wiki - .local](https://en.wikipedia.org/wiki/.local)

This is a zero-configuration protocol that works on LAN subnets. No server required. Uses the `.local` TL;DR.

## Links

### Configuration Files Documents

* [for `core-site.xml`](https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/core-default.xml)
* [for `yarn-site.xml`](https://hadoop.apache.org/docs/r3.1.1/hadoop-yarn/hadoop-yarn-common/yarn-default.xml)
* [for `hdfs-site.xml`](https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml)
* [for `mapred-site.xml`](https://hadoop.apache.org/docs/r3.1.1/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml)

### Similar Project

* [gregbaker/raspberry-pi-cluster](https://github.com/gregbaker/raspberry-pi-cluster) - use fabric 1.X
* [How to build a 7 node Raspberry Pi Hadoop Cluster](http://www.nigelpond.com/uploads/How-to-build-a-7-node-Raspberry-Pi-Hadoop-Cluster.pdf)
* [A Hadoop data lab project on Raspberry Pi](https://blogs.sap.com/2015/04/25/a-hadoop-data-lab-project-on-raspberry-pi-part-14/)
* [Raspberry PI Hadoop Cluster](http://www.widriksson.com/raspberry-pi-hadoop-cluster/)
* Medium - How to Hadoop at home with Raspberry Pi
    * [Part 1: Setting up Raspberry Pi and network configurations](https://medium.com/@jasonicarter/how-to-hadoop-at-home-with-raspberry-pi-part-1-3b71f1b8ac4e#.6xuk426d2)
    * [Part 2: Hadoop single node setup, testing and prepping the cluster](https://medium.com/@jasonicarter/how-to-hadoop-at-home-with-raspberry-pi-part-2-b8ccfbe6ba9a#.rdymvh5zn)
    * [Part 3: Hadoop cluster setup, testing and final thoughts](https://medium.com/@jasonicarter/how-to-hadoop-at-home-with-raspberry-pi-part-3-7d114d35fdf1#.cn9da731k)
* [Build a Hadoop 3 cluster with Raspberry Pi 3](https://medium.com/@oliver_hu/build-a-hadoop-3-cluster-with-raspberry-pi-3-f451b7f93254)
* [Building a Hadoop cluster with Raspberry Pi](https://developer.ibm.com/recipes/tutorials/building-a-hadoop-cluster-with-raspberry-pi/)
* [RPiCluster](https://bitbucket.org/jkiepert/rpicluster)
    * [Demo](https://youtu.be/i_r3z1jYHAc)
