# Setup Raspberry Pi

## Image

### Download Images

* [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) (currently `buster`)

> If using new version Raspbian, make sure all the version related name in `fabfile.py` is matched

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

## Connect to Pi

### Scan Pi's IP Address

There are many approaches

#### nmap

> Use `ifconfig` and see current PC WLAN address and replace `x` with related value

* `nmap -sn 192.168.x.x/24`

> * [bad CPU type in executable: nmap (x86 -> x64) · Issue #1722 · nmap/nmap](https://github.com/nmap/nmap/issues/1722)
> * [Release Nmap as a 64-bit build on macOS · Issue #1371 · nmap/nmap](https://github.com/nmap/nmap/issues/1371)

#### Fing

* [Fing - IoT device intelligence for the connected world | Fing](https://www.fing.com/)

#### Angry IP Scanner

* [Angry IP Scanner - the original IP scanner for Windows, Mac and Linux](https://angryip.org/)
* [angryip/ipscan: Angry IP Scanner - fast and friendly network scanner](https://github.com/angryip/ipscan)

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

## Additional Settings

### raspi-config

> Login to each Raspparry Pi and type `sudo raspi-config` (only for Raspbian)

1. Setup locale
   * [How to configure locale settings of Raspbian Stretch with raspi-config - Techcoil Blog](https://www.techcoil.com/blog/how-to-configure-locale-settings-of-raspbian-stretch-with-raspi-config/)
   * Or just `sudo locale-gen en_US.UTF-8` (recommend)

## Format and copy image from another SD card

```txt
# Find the SD card device name (assume it's disk2)
$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *251.0 GB   disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:                 Apple_APFS Container disk1         250.8 GB   disk0s2

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                      +250.8 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume Macintosh HD            234.4 GB   disk1s1
   2:                APFS Volume Preboot                 45.1 MB    disk1s2
   3:                APFS Volume Recovery                517.1 MB   disk1s3
   4:                APFS Volume VM                      11.7 GB    disk1s4

/dev/disk2 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *15.7 GB    disk2
   1:             Windows_FAT_32 boot                    45.9 MB    disk2s1
   2:                      Linux                         15.6 GB    disk2s2

/dev/disk3 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *15.7 GB    disk3
   1:             Windows_FAT_32 boot                    45.9 MB    disk3s1
   2:                      Linux                         15.6 GB    disk3s2

# Unmount SD card
$ diskutil unmountDisk /dev/disk2
Unmount of all volumes on disk2 was successful

# Format SD card (FAT32)
$ sudo newfs_msdos -F 32 /dev/disk2
newfs_msdos: warning: /dev/disk2 is not a character device
512 bytes per physical sector
/dev/disk2: 30567232 sectors in 1910452 FAT32 clusters (8192 bytes/cluster)
bps=512 spc=16 res=32 nft=2 mid=0xf0 spt=32 hds=255 hid=0 drv=0x00 bsec=30597120 bspf=14926 rdcl=2 infs=1 bkbs=6

# Copy from another SD card
$ sudo dd if=/dev/disk3 of=/dev/disk2
```

## Raspberry Pi 4 Heat Testing

* [How to find out Raspberry Pi GPU and ARM CPU temperature on Linux - nixCraft](https://www.cyberciti.biz/faq/linux-find-out-raspberry-pi-gpu-and-arm-cpu-temperature-command/)
* [Raspberry Pi 4 Heat Testing - YouTube](https://www.youtube.com/watch?v=tWsM69_5g4E)

```sh
#!/bin/bash
# Script: my-pi-temp.sh
# Purpose: Display the ARM CPU and GPU  temperature of Raspberry Pi 2/3 
# Author: Vivek Gite <www.cyberciti.biz> under GPL v2.x+
# -------------------------------------------------------
cpu=$(</sys/class/thermal/thermal_zone0/temp)
echo "$(date) @ $(hostname)"
echo "-------------------------------------------"
echo "GPU => $(/opt/vc/bin/vcgencmd measure_temp)"
echo "CPU => $((cpu/1000))'C"
```

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

Trouble Shooting

* [ubuntu - How do I resolve `The following packages have unmet dependencies` - Stack Overflow](https://stackoverflow.com/questions/26571326/how-do-i-resolve-the-following-packages-have-unmet-dependencies)
  * `fab CMD-parallel 'sudo apt-get install -fy vlc-bin vlc-plugin-skins2'`
* Perl locale problem
  * [How to fix a locale setting warning from Perl? - Stack Overflow](https://stackoverflow.com/questions/2499794/how-to-fix-a-locale-setting-warning-from-perl)
  * [Perl warning Setting locale failed in Debian - Thomas-Krenn-Wiki](https://www.thomas-krenn.com/en/wiki/Perl_warning_Setting_locale_failed_in_Debian)
