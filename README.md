# RaspPi-Cluster

The following tutorial I will use a four node Raspberry Pi Cluster for an example.

> (And I'll use my preferred selection between many similar options.)

After setting up the environment, I'll implement some popular distributed computing ecosystem on it.
And try to write a quick start script for them. And maybe some example demo.

## Usage

(put some usage of instant-use script here)

## Example

Subject|Ecosystem|Purpose
-------|---------|-------
[MapReduce Practice](Example/MapReduce/)|Hadoop|MapReduce practice with Hadoop Streaming

## Steps

A step by step record of how I build this system.

* [Preparation](Preparation.md)
    * Hardware purchase
    * Software package and dependencies install

1. [Setup Raspberry Pis](SetupRaspPi.md)
2. Assemble hardwares
    ![rpi-cluster](Picture/FourNodesRaspberryPiCluster.jpeg)
3. [Setup fabric](SetupFabric.md) - execute shell commands remotely over SSH to all hosts at once!

## Notes about distributed computing

Algorithm

* [MapReduce](Notes/Distributed_Computing/MapReduce.md)

## Notes about specific ecosystem

[Hadoop](Notes/Hadoop/Hadoop.md)

* HDFS

Spark

Kubernetes

## Links

### Similar Project

* [gregbaker/raspberry-pi-cluster](https://github.com/gregbaker/raspberry-pi-cluster)
* [How to build a 7 node Raspberry Pi Hadoop Cluster](http://www.nigelpond.com/uploads/How-to-build-a-7-node-Raspberry-Pi-Hadoop-Cluster.pdf)
* [A Hadoop data lab project on Raspberry Pi](https://blogs.sap.com/2015/04/25/a-hadoop-data-lab-project-on-raspberry-pi-part-14/)
* [Raspberry PI Hadoop Cluster](http://www.widriksson.com/raspberry-pi-hadoop-cluster/)
