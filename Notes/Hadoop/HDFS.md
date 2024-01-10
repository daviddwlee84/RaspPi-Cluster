# Hadoop Distributed File System (HDFS)

## Getting Started

You just need to have proper configure XMLs and then start cluster on NameNode.
This will bring up workers automatically.

* `hadoop/sbin/start_dfs.sh`
* `hadoop/sbin/stop_dfs.sh`

## Hadoop Architecture

[![hdfs architecture](https://hadoop.apache.org/docs/r1.2.1/images/hdfsarchitecture.gif)](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html#NameNode+and+DataNodes)

### NameNode

### DataNodes

## Concept

* [Apache Hadoop 3.3.6 – HDFS Short-Circuit Local Reads](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ShortCircuitLocalReads.html)

> should not manually create dn_socket

```xml
<configuration>

  ...

  <property>
    <name>dfs.client.read.shortcircuit</name>
    <value>true</value>
  </property>
  <property>
    <name>dfs.domain.socket.path</name>
    <value>/var/lib/hadoop-hdfs/dn_socket</value>
  </property>
</configuration>
```

```bash
# https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/NativeLibraries.html
$ hadoop checknative -a
2024-01-09 10:18:09,933 INFO bzip2.Bzip2Factory: Successfully loaded & initialized native-bzip2 library system-native
2024-01-09 10:18:09,939 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
2024-01-09 10:18:09,972 WARN erasurecode.ErasureCodeNative: Loading ISA-L failed: Failed to load libisal.so.2 (libisal.so.2: cannot open shared object file: No such file or directory)
2024-01-09 10:18:09,973 WARN erasurecode.ErasureCodeNative: ISA-L support is not available in your platform... using builtin-java codec where applicable
2024-01-09 10:18:10,124 INFO nativeio.NativeIO: The native code was built without PMDK support.
Native library checking:
hadoop:  true /home/hadoop/hadoop/lib/native/libhadoop.so.1.0.0
zlib:    true /lib/x86_64-linux-gnu/libz.so.1
zstd  :  true /usr/lib/x86_64-linux-gnu/libzstd.so.1
bzip2:   true /lib/x86_64-linux-gnu/libbz2.so.1
openssl: true /usr/lib/x86_64-linux-gnu/libcrypto.so
ISA-L:   false Loading ISA-L failed: Failed to load libisal.so.2 (libisal.so.2: cannot open shared object file: No such file or directory)
PMDK:    false The native code was built without PMDK support.
2024-01-09 10:18:10,137 INFO util.ExitUtil: Exiting with status 1: ExitException
```

## Trouble Shooting

### HDFS Save Mode => Make HDFS read-only

1. Clean disk
2. Run `hdfs dfsadmin -safemode leave`

```
Security is off.

Safe mode is ON. Resources are low on NN. Please add or free up more resourcesthen turn off safe mode manually. NOTE: If you turn off safe mode before adding resources, the NN will immediately return to safe mode. Use "hdfs dfsadmin -safemode leave" to turn safe mode off.

1,432 files and directories, 2,041 blocks (2,041 replicated blocks, 0 erasure coded block groups) = 3,473 total filesystem object(s).

Heap Memory used 1.74 GB of 2.4 GB Heap Memory. Max Heap Memory is 29.97 GB.

Non Heap Memory used 100.85 MB of 105.5 MB Committed Non Heap Memory. Max Non Heap Memory is <unbounded>
```

* [Turn off Safemode for the NameNode on your EMR cluster | AWS re:Post](https://repost.aws/knowledge-center/emr-namenode-turn-off-safemode)
* [hadoop - Name node is in safe mode. Not able to leave - Stack Overflow](https://stackoverflow.com/questions/15803266/name-node-is-in-safe-mode-not-able-to-leave)

## Links

### Shell Command

* [HDFS FileSystemShell Command](https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-common/FileSystemShell.html)
