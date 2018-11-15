# RaspPi-Cluster

The following tutorial we will use a four Raspberry Pi Cluster for an example.

(And I'll use my preferred selection between many similar options.)

## Hardware Preparation

### Raspberry Pi

* Raspberry Pi × 4
* micro SD card × 4

### Internet

* 5-port ethernet switch × 1
* ethernet cable
    * short × 4
    * long  × 1

### Power

* usb power hub × 1
* micro USB cable × 4

### Optional

* (4-layer) cluster frame × 1
* Ducky Mini :P

## Software Dependencies

### Operating System

* macOS
* Raspbian

### Python Packages

* Python 3
* [Fabric 2](https://www.fabfile.org/)

## Steps

1. [Setup Raspberry Pis](SetupRaspPi.md)
2. Assemble hardwares
3. Setup fabric - execute shell commands remotely over SSH to all hosts at once!
