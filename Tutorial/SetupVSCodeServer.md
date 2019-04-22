# Setup VSCode code-server

## Quick Start with Docker

> TODO (quick install docker on Raspberry Pi)

```sh
docker run -it -p 127.0.0.1:8443:8443 -v "${PWD}:/home/coder/project" codercom/code-server --allow-http --no-auth
```

## Download from Release

* [code-server release](https://github.com/codercom/code-server/releases)

```sh
version="1.903-vsc1.33.1"
wget https://github.com/codercom/code-server/releases/download/$version/code-server$version-linux-x64.tar.gz
tar -xzf code-server$version-linux-x64.tar.gz
rm code-server$version-linux-x64.tar.gz
```

## Trouble Shooting

### Using Docker Image on Raspberry Pi

```sh
$ docker run -it -p 127.0.0.1:8443:8443 -v "${PWD}:/home/coder/project" codercom/code-server --allow-http --no-auth
standard_init_linux.go:207: exec user process caused "exec format error"
```

* [exec user process caused "exec format error" when run container with CMD on RHEL](https://github.com/containers/buildah/issues/475)

## Links

* [coder](https://coder.com/)
  * [code-server github](https://github.com/codercom/code-server)
* [codercom/sshcode](https://github.com/codercom/sshcode)

### Tutorial

* [Use Coder to Run VS Code on Google Cloud](https://fireship.io/lessons/vscode-cloud-coder-tensorflow/)
  * [Youtube - Run VS Code in the browser with massive computing resources](https://www.youtube.com/watch?v=N5WojMutddQ)

### Single Machine Version

#### Code-OSS

* [PiMyLifeUp - Raspberry Pi Visual Studio Code: Installing VS Code on Raspbian](https://pimylifeup.com/raspberry-pi-visual-studio-code/)

```sh
curl -L https://code.headmelted.com/installers/apt.sh | sudo bash
```
