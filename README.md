# RaspPi-Cluster

The following tutorial I will use a four node Raspberry Pi Cluster for an example.

> (And I'll use my preferred selection between many similar options.)
>
> i.e. the memory allocation settings is fit for Raspberry Pi 3 with 1G RAM

After setting up the environment, I'll implement some popular distributed computing ecosystem on it.
And try to write a quick start script for them. And maybe some example demo.

## Usage

[**Usage in Detail !!**](Documentation/FabfileHelp.md) (Manual)

### Quick Start

Important!!. First check user settings in [`configure.yaml`](configure.yaml), (for deeper settings check out [`fabfile.py`](fabfile.py) User Settings part)

```sh
# Install local dependencies
python3 -m pip install -r requirements.txt
```

#### Quick Setup

```sh
fab update-and-upgrade # Make apt-get up to date (this can be done using the first login GUI of Raspbian Buster)
fab env-setup # Quick install basic utility function
fab set-hostname # Set hostname for each node (will need to reboot)
fab hosts-config # Set each others' hostname-to-IP on each Raspberry Pi (or they can't find each other using hostname)
fab ssh-config # Generate ssh-key and setup to all nodes
fab change-passwd # Change password for more security (Remember also change in fabfile.py later if you have changed pi's passowrd)
fab expand-swap # Expand swap (default 1024MB use --size=MEMSIZE to match your need) (System default is 100MB)
```

**Regular used function** (make sure you've generated ssh-key or move your ssh-key to `./connection/id_rsa`)

```sh
fab ssh-connect NODE_NUM # Connect to any node by it's index without password (use -h flag to be hadoop user)
fab uploadfile file_or_dir -s -p # Upload file or folder to remote (specific node use -n=NODE_NUM flag)
```

#### Hadoop

If you changed default hostname in `fabfile.py` or `configure.yaml`.
Make sure you also changed the Hadoop configuraiton file in ./Files.

(if you're using cloud server, make sure you've opened the ports that Hadoop need.)

```sh
fab install-hadoop # An one button setup for hadoop environment on all nodes!!!

fab update-hadoop-conf # Every time you update configure file in local you can update it to all nodes at once
```

(the key of Hadoop user is store in `./connection/hadoopSSH`)

Utility function

```sh
fab start-hadoop
fab restart-hadoop
fab stop-hadoop

fab status-hadoop # Monitor Hadoop behavior

fab example-hadoop # If everything is done. You can play around with some hadoop official example
```

#### Spark

If you changed default hostname in `fabfile.py` or `configure.yaml`.
Make sure you also changed the Spark configuraiton file in ./Files.

```sh
fab install-spark
```

There are lots of utility function like I did for Hadoop. Check it out by `fab --list`

#### Jupyter Notebook with PySpark

This will be installed with Hadoop user

```sh
fab install-jupyter
```

#### Docker Swarm

```sh
fab install-docker
```

#### VSCode code-server

```sh
fab install-codeserver
```

## Example

| Subject                                  | Ecosystem | Purpose                                              |
| ---------------------------------------- | --------- | ---------------------------------------------------- |
| [MapReduce Practice](Example/MapReduce/) | Hadoop    | MapReduce practice with Hadoop Streaming             |
| [Spark Practice](Example/SparkExample/)  | Spark     |                                                      |
| [Inverted Index](Example/InvertedIndex/) |           | Focus on multiple inverted index strategy for search |

## Steps

A step by step record of how I build this system.

* [Preparation](Tutorial/Preparation.md)
  * Hardware purchase
  * Software package and dependencies (PC/Laptop)
    * Python > 3.6
    * Fabric 2.X

1. [Setup Raspberry Pis](Tutorial/SetupRaspPi.md)
2. Assemble hardwares

    ![rpi-cluster](Picture/FourNodesRaspberryPiCluster.jpeg)

3. Follow steps in [Quick Setup](#quick-setup)
   * Make sure
     1. (setup locale)
     2. update and upgrade
     3. setup environment
        1. git
        2. Java (JDK)
     4. setup hostname (for each and between each others)
     5. ssh keys
     6. expand swap (if use Raspberry Pi 3 or small RAM Raspberry Pi 4)
4. [Setup fabric (brief notes)](Tutorial/SetupFabric.md) - execute shell commands remotely over SSH to all hosts at once!
    * I've built some utility function first and then move on setup Hadoop
    * when any general purpose manipulation needed I'll add it.
5. [Setup Hadoop](Tutorial/SetupHadoop.md)
6. [Setup Spark](Tutorial/SetupSpark.md)
7. [Setup Jupyter with PySpark and Parallel IPython](Tutorial/SetupJupyter.md)
8. [Setup Docker Swarm](Tutorial/SetupDockerSwarm.md) - TODO
9. [Setup Kubernetes](Tutorial/SetupKubernetes.md) - TODO
10. [Setup Distributed Tensorflow](Tutorial/SetupDestributedTensorflow.md) - TODO
    * on Hadoop
    * on Kubernetes

### Not Big Data / Cluster Related

1. [Setup VSCode code-server](Tutorial/SetupVSCodeServer.md) - TODO

## Notes about distributed computing

Algorithm

* [MapReduce](Notes/Distributed_Computing/MapReduce.md)

Links

* [Chameleon Cloud Training](https://cloudandbigdatalab.github.io/)

## Notes about specific ecosystem

[Hadoop](Notes/Hadoop/Hadoop.md)

* [HDFS](Notes/Hadoop/HDFS.md)
* [YARN](Notes/Hadoop/YARN.md)

[Spark](Notes/Spark/Spark.md)

[Distributed MongoDB](Notes/NoSQL/MongoDB.md)

[Kubernetes](Notes/Kubernetes/Kubernetes.md)

Distributed Tensorflow

[Elasticsearch](Notes/Elasticsearch/Elasticsearch.md)

[RediSearch](Notes/RediSearch/RediSearch.md)

High Performance Computing (HPC)

- [MPI](Notes/HighPerformanceComputing/MPI.md)
- [PBS](Notes/HighPerformanceComputing/PBS.md)

Resource Manager

### [Parallel Computing](Notes/ParallelComputing/ParallelComputing.md)

> Intel has updated their DevCloud system and currently called oneAPI
>
> * [Intel AI DevCloud oneAPI](Notes/ParallelComputing/NewIntelAIDevCloud.md)
> ([Intel AI DevCloud (Old)](Notes/ParallelComputing/IntelAIDevCloud.md))

#### Resource Allocation System (RAS)

[Sun Grid Engine (SGE)](Notes/ParallelComputing/SGE.md)

[Torque/PBS](Notes/ParallelComputing/Torque_PBS.md)

## TODO

* Deal with PySpark and Jupyter Notebook problem
* More friendly Document
* Hadoop utility function introduction
* Dynamic Configure based on different hardware and maybe GUI and save multiple settings
  * Set up hardware detail e.g. RAM size
  * Read and write *.xml
* list some alterative note
  * pdsh == fab CMD
  * ssh-copy-id == ssh-config
* Hive, HBase, Pig, ...
* Git server maybe
  * [Setting up Your Raspberry Pi as a Git Server](https://www.sitepoint.com/setting-up-your-raspberry-pi-as-a-git-server/)
* [14+ Raspberry Pi Server Projects](https://pimylifeup.com/category/projects/server/)
* Change `apt-get` to `apt`?!
  * [Difference Between apt and apt-get Explained - It's FOSS](https://itsfoss.com/apt-vs-apt-get-difference/)
* MPI
* [Dask](https://www.dask.org/)
  * [Deploy Dask Clusters — Dask documentation](https://docs.dask.org/en/latest/deploying.html)
    * [Dask-MPI](https://mpi.dask.org/en/latest/)
    * Cluster manager: PBS, SLURM, LSF, SGE
  * [Configuring a Distributed Dask Cluster](https://blog.dask.org/2020/07/30/beginners-config)
* Fabric alternative
  * [AsyncSSH: Asynchronous SSH for Python — AsyncSSH 2.13.2 documentation](https://asyncssh.readthedocs.io/en/latest/) 
