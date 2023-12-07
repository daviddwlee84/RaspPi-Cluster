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
