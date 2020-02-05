# Preparation

## Hardware Preparation

### Raspberry Pi

* Raspberry Pi 3 Model B+ × 4
* MicroSD card × 4

> * Raspberry Pi 4 Model B × 4 with Heatsinks

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
  * if later than Catalina, might face 32-bit `nmap` problem
* Raspbian
  * currently Buster, if it changed, it might need to change some code in `fabfile.py`

### Python Packages

* Python 3.6
  * f-string support
* [Fabric 2](https://www.fabfile.org/)
* [PyYAML](https://pyyaml.org/)
