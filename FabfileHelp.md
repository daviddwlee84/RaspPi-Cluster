# Manual of my fabfile.py

## Basic fab usage

* `fab --list`: List your tasks
* `fab --help Task`: Show help
    * Docstring
    * Options
        * `@task(help={'command': "help description"})`

## General usage

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

## Quick Setup

### ssh key

It will auto generate ssh key in `temp_files/` and copy it to all remote

```sh
fab ssh-config
```

You can try ssh without passowrd now!

```sh
ssh -i temp_files/id_rsa pi@192.168.1.109
```

## Hadoop

### Download Hadoop to local

```sh
fab download-hadoop
```

### Install Hadoop

```sh
fab install-hadoop
```
