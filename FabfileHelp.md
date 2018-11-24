# Manual of my fabfile.py

## Basic fab usage

* `fab --list`: List your tasks
* `fab --help Task`: Show help
    * Docstring
    * Options
        * `@task(help={'command': "help description"})`

## Before using my fabfile.py

First open fabfile.py

Change some setting

* HOSTS: hosts ip to your nodes

## General usage

### List current nodes

```sh
fab node-ls
```

### Sending command

#### CMD

```txt
$ fab --help CMD
Usage: fab [--core-opts] CMD [--options] [other tasks here ...]

Docstring:
  Run command on all nodes in serial order

Options:
  -c STRING, --command=STRING   Command you want to sent to host
  -n INT, --node-num=INT        Node number of HOSTS list
  -v, --verbose                 Verbose output
```

**To every node**:

```sh
fab CMD "hostname -I" -v
```

**To single node**:

```sh
fab CMD "ls ~/Downloads" -v -n=2
```

#### CMD-parallel

```txt
$ fab --help CMD-parallel
Usage: fab [--core-opts] CMD-parallel [--options] [other tasks here ...]

Docstring:
  Execute command on all nodes in parallel

Options:
  -c STRING, --command=STRING   Command you want to sent to host in parallel
  -v, --verbose                 Verbose output
```

Example:

```sh
fab CMD "sudo apt-get install -y vim"
```

### File Transmit

#### Upload file

```txt
$ fab --help uploadfile
Usage: fab [--core-opts] uploadfile [--options] [other tasks here ...]

Docstring:
  Copy local file to remote

Options:
  -d STRING, --dest=STRING           Remote destination (directory)
  -n INT, --node-num=INT             Node number of HOSTS list
  -p STRING, --path-to-file=STRING   Path to file in local
  -v, --verbose                      Verbose output
```

### ssh

#### Connect to node

Default using [pre-generate key](#Generate-ssh-key). Or you can specific your own key if you have already set it.

```txt
fab --help ssh-connect
Usage: fab [--core-opts] ssh-connect [--options] [other tasks here ...]

Docstring:
  Connect to specific node using ssh private key

Options:
  -n STRING, --node-num=STRING      Node number of HOSTS list
  -p STRING, --private-key=STRING   Path to private key
```

Example:

use [pre-generate key](#Generate-ssh-key).

```sh
fab ssh-connect 0
```

use your own key

```sh
fab ssh-connect 0 -p=~/.ssh/id_rsa
```

## Quick Setup

### Generate ssh key

It will auto generate ssh key in `temp_files/` and copy it to all remote.

```sh
fab ssh-config
```

You can try ssh without passowrd now!

```sh
ssh -i temp_files/id_rsa pi@192.168.1.109
```

### Set Hostname

It will need to rebot after setting.

Hostname rule will be:

```txt
master --> first IP
slave1 --> second IP
slave2 --> third IP
slave3 --> fourth IP
... (If you have larger NUM_NODES and HOSTS_IP)
```

```sh
fab set-hostname
```

## Hadoop

You should first setup some configure in [fabfile.py](fabfile.py).

* HADOOP_VERSION: default 3.1.1

### Download Hadoop to local

```sh
fab download-hadoop
```

### Install Hadoop

```sh
fab install-hadoop
```
