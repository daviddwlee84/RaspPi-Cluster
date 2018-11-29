# RaspPi-Cluster

The following tutorial I will use a four node Raspberry Pi Cluster for an example.

> (And I'll use my preferred selection between many similar options.)

After setting up the environment, I'll implement some popular distributed computing ecosystem on it.
And try to write a quick start script for them. And maybe some example demo.

## Usage

[**Usage in Detail !!**](FabfileHelp.md) (Manual)

### Quick Start

First check user setting in [fabfile.py](fabfile.py) (Important!) ([Connection Setting Example](ConnectionSetting.md))

```sh
# Install local dependencies
python3 -m pip install -r requirements.txt
```

#### Quick Setup

```sh
fab update-and-upgrade # Make apt-get up to date
fab env-setup # Quick install basic utility function
fab set-hostname # Set hostname for each node (will need to reboot)
fab ssh-config # Generate ssh-key and setup to all nodes
fab change-passwd # Change password for more security (Remember also change in fabfile.py later if you have changed pi's passowrd)
```

Regular used function

```sh
fab ssh-connect NODE_NUM # Connect to any node by it's index without password after you've generated ssh-key (use -h flag to be hadoop user)
```

#### Hadoop

If you changed default hostname in fabfile.py. Make sure you also change in hadoop configuraiton file in ./Files.

```sh
fab install-hadoop # An one button setup for hadoop environment on all nodes!!!

fab update-hadoop-conf # Every time you update configure file in local you can update it to all nodes at once
```

Utility function

```sh
fab start-hadoop
fab restart-hadoop
fab stop-hadoop

fab status-hadoop

fab example-hadoop # If everything is done. You can play around with some hadoop official example
```

## Example

Subject|Ecosystem|Purpose
-------|---------|-------
[MapReduce Practice](Example/MapReduce/)|Hadoop|MapReduce practice with Hadoop Streaming

## Steps

A step by step record of how I build this system.

* [Preparation](Preparation.md)
    * Hardware purchase
    * Software package and dependencies (PC/Laptop)

1. [Setup Raspberry Pis](SetupRaspPi.md)
2. Assemble hardwares

    ![rpi-cluster](Picture/FourNodesRaspberryPiCluster.jpeg)

3. [Setup fabric (brief notes)](SetupFabric.md) - execute shell commands remotely over SSH to all hosts at once!
    * I've built some utility function first and then move on setup Hadoop
    * when any general purpose manipulation needed I'll add it.
4. [Setup Hadoop](SetupHadoop.md)

## Notes about distributed computing

Algorithm

* [MapReduce](Notes/Distributed_Computing/MapReduce.md)

## Notes about specific ecosystem

[Hadoop](Notes/Hadoop/Hadoop.md)

* HDFS

Spark

Kubernetes

## TODO

* Expand to support any other Debian/Unix system
* Better switch between multiple configuration files for multi-server
* More friendly Document
* Hadoop utility function introduction

## Links

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
