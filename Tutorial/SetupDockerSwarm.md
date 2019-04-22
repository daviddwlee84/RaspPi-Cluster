# Setup Docker Swarm

## Install Docker

### Using get-docker script

> Using the script will get `docker-ce-cli` and `docker-ce` (you can uninstall this by `apt-get`)

```sh
# download the install script
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
# in one line
curl -sSL https://get.docker.com | sudo sh
```

* [How to install Docker on your Raspberry Pi](https://howchoo.com/g/nmrlzmq1ymn/how-to-install-docker-on-your-raspberry-pi)
* [The easy way to set up Docker on a Raspberry Pi](https://medium.freecodecamp.org/the-easy-way-to-set-up-docker-on-a-raspberry-pi-7d24ced073ef)

> But using this script, it needs to run on [interactive](#Interactive-problem-when-using-get-docker-script) terminal (i.e. can't use fabric...) => Solved by setting environment variable `DEBIAN_FRONTEND=noninteractive`

### Using Hypriot distribution

> Haven't tried yet

* [Hypriot - Run Docker on a Raspberry Pi 3 with onboard WiFi](https://blog.hypriot.com/post/run-docker-rpi3-with-wifi/)
* [GitHub Gist tyrell/docker-install-rpi3.md](https://gist.github.com/tyrell/2963c6b121f79096ee0008f5a47cf347)
* [Get Docker up and running on the RaspberryPi (ARMv6) in four steps (Wheezy)](https://github.com/umiddelb/armhf/wiki/Get-Docker-up-and-running-on-the-RaspberryPi-(ARMv6)-in-four-steps-(Wheezy))

### Using HypriotOS

> Haven't tried yet

* [Getting started with Docker on your Raspberry Pi](https://blog.hypriot.com/getting-started-with-docker-on-your-arm-device/)

## Docker Swarm

* [Docker comes to Raspberry Pi](https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/)

## Trouble Shooting

### Interactive problem when using get-docker script

> It seems that the `get-docker.sh` need some interactive installation?! but in the end it showed "install successfully" but actually have some daemon problem.
>
> Update: message show even after setting environment variable `DEBIAN_FRONTEND=noninteractive` but it can work anyway.

```txt
$ fab install-docker
# Executing docker install script, commit: 2f4ae48

...

debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin:

...

If you would like to use Docker as a non-root user, you should now consider
adding your user to the "docker" group with something like:

  sudo usermod -aG docker your-user

Remember that you will have to log out and back in for this to take effect!

WARNING: Adding a user to the "docker" group will grant the ability to run
         containers which can be used to obtain root privileges on the
         docker host.
         Refer to https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface
         for more information.
Docker is ready!
```

* [Is it possible to answer dialog questions when installing under docker?](https://stackoverflow.com/questions/22466255/is-it-possible-to-answer-dialog-questions-when-installing-under-docker)
* [Error debconf: unable to initialize frontend: Dialog](https://github.com/moby/moby/issues/27988)
* [Getting tons of debconf messages unless TERM is set to linux](https://github.com/phusion/baseimage-docker/issues/58)

## Links

* [docker/docker-install](https://github.com/docker/docker-install)
* [Docker document - Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
