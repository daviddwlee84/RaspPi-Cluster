# RaspPi-Cluster

The following tutorial we will use a four node Raspberry Pi Cluster for an example.

(And I'll use my preferred selection between many similar options.)

## Hardware Preparation

### Raspberry Pi

* Raspberry Pi 3 Model B+ × 4
* MicroSD card × 4

### Internet

* 5-port Ethernet Switch × 1
* Ethernet cable
    * short × 4
    * long  × 1

### Power

* 4-port USB Power Hub × 1
* MicroUSB cable × 4

### Optional

* (4-layer) Cluster Frame × 1
* [~~Ducky Mini~~](http://www.duckychannel.com.tw/en/ducky-mini/) with Cherry MX Brown switch :P

## Software Dependencies

### Operating System

* macOS
* Raspbian

### Python Packages

* Python 3
* [Fabric 2](https://www.fabfile.org/)

## Steps [Main Part]

1. [Setup Raspberry Pis](SetupRaspPi.md)
2. Assemble hardwares
3. [Setup fabric](SetupFabric.md) - execute shell commands remotely over SSH to all hosts at once!

## Links

### Similar Project

* [gregbaker/raspberry-pi-cluster](https://github.com/gregbaker/raspberry-pi-cluster)
* [How to build a 7 node Raspberry Pi Hadoop Cluster](http://www.nigelpond.com/uploads/How-to-build-a-7-node-Raspberry-Pi-Hadoop-Cluster.pdf)
* [A Hadoop data lab project on Raspberry Pi](https://blogs.sap.com/2015/04/25/a-hadoop-data-lab-project-on-raspberry-pi-part-14/)
* [Raspberry PI Hadoop Cluster](http://www.widriksson.com/raspberry-pi-hadoop-cluster/)
