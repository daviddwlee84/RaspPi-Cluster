# Manual of my fabfile.py

## Basic fab usage

* `fab --list`: List your tasks
* `fab --help Task`: Show help
    * Docstring
    * Options
        * `@task(help={'command': "help description"})`

## General usage

### Sending command

#### To all node in serial

```txt
$ fab --help CMD
Usage: fab [--core-opts] CMD [--options] [other tasks here ...]

Docstring:
  Run command on all nodes in serial

Options:
  -c STRING, --command=STRING   Command you want to sent to host
  -v, --verbose                 verbose output
```

Example:

```sh
fab CMD "hostname -I"
```

#### To all node in parallel

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

#### To single node

```txt
$ fab --help CMD-single
Usage: fab [--core-opts] CMD-single [--options] [other tasks here ...]

Docstring:
  Execute command on single node

Options:
  -c STRING, --command=STRING    Command you want to sent to node
  -n STRING, --node-num=STRING   Node number of HOSTS list
```

Example:

```sh
fab CMD "ls ~/Downloads"
```

## Hadoop

### Install Hadoop

```
fab install-hadoop
```
