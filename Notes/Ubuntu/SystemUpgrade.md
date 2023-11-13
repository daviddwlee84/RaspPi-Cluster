# System Upgrade

* [How to upgrade | Ubuntu](https://ubuntu.com/server/docs/upgrade-introduction)

```bash
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 16.04.7 LTS
Release:        16.04
Codename:       xenial

$ cat /etc/os-release
NAME="Ubuntu"
VERSION="16.04.7 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.7 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
```

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt autoremove

sudo apt install update-manager-core
sudo do-release-upgrade
```

```
Reading cache

Checking package manager

Continue running under SSH?

This session appears to be running under ssh. It is not recommended
to perform a upgrade over ssh currently because in case of failure it
is harder to recover.

If you continue, an additional ssh daemon will be started at port
'1022'.
Do you want to continue?

Continue [yN] y

Starting additional sshd

To make recovery in case of failure easier, an additional sshd will
be started on port '1022'. If anything goes wrong with the running
ssh you can still connect to the additional one.
If you run a firewall, you may need to temporarily open this port. As
this is potentially dangerous it's not done automatically. You can
open the port with e.g.:
'iptables -I INPUT -p tcp --dport 1022 -j ACCEPT'

To continue please press [ENTER]
```

## Links

* 
