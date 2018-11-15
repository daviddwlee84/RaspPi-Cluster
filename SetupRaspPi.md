# Setup Raspberry Pi

## Image

### Download Images

* [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

### Write Image into SD Card

* [Etcher](https://www.balena.io/etcher/)

1. Select image.zip
2. Select drive
3. Flash!

## Configuration

### Setup SSH

In order to connect to Raspberry Pi without a monitor at first. We need to enable ssh since in current version of Raspbian it is default disable.

1. Create a empty file called `ssh` at the root directory of the SD card.
    * `touch /Volumes/boot/ssh`
2. Ejact (Unmount) SD card
    * Check the device name of the SD Card `diskutil list`
    * Unmount disk `diskutil unmountDisk /dev/diskNum`

### raspi-config

1. Expand file system

TBD

## Connect to Pi

### Scan Pi's IP Address

There are many approach

#### nmap

* `nmap -sn 192.168.x.x/24`

#### iOS

* Fing - Network Scanner

### SSH Client

* Windows
    * putty
* iOS, Android
    * Terminus

### Connection

Default setting

* user: pi
* password: raspberry

e.g. `ssh pi@192.168.x.x`

## Links

* [Official Website](https://www.raspberrypi.org/)
* [Installation Guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
* Documentation
    * Remote Access
        * [SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md)
            * 3 Enable SSH on a headless Raspberry Pi (add file to SD card on another machine)
        * [VNC](https://www.raspberrypi.org/documentation/remote-access/vnc/README.md)
        * [FTP](https://www.raspberrypi.org/documentation/remote-access/ftp.md)
    * Configuration
        * [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)
        * [config.txt](https://www.raspberrypi.org/documentation/configuration/config-txt/README.md) ([the boot folder](https://www.raspberrypi.org/documentation/configuration/boot_folder.md))
            * [HDMI configuration](https://www.raspberrypi.org/documentation/configuration/hdmi-config.md)
        * [Securing Your Raspberry Pi](https://www.raspberrypi.org/documentation/configuration/security.md)