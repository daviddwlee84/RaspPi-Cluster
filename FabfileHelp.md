# Manual of my fabfile.py

## Basic fab usage

* `fab --list`: List your tasks
* `fab [--core-opts] Task [--options] [other tasks here ...]`: Invoke / Call / Run a Function / Method / Task
* `fab --help Task`: Show help
    * Docstring
        * `"""  ...  """`
    * Options
        * `@task(help={...})`

```py
@task(help={'parameter': "help description"})
def Task(ctx, parameter):
    """
    I'm docstring
    """
    ...
```

## Before using my fabfile.py

First open fabfile.py

Change some setting to fit your situation

* NUM_NODES: total nodes number
* HOSTS_IP: hosts ip list to your nodes
    * Initially you will need this, and I highly recommend [setting hostname](#Set-Hostname), then you can use `pi@hostname.local` to login.
    * And after you set up hostnames, you can change connection mode `CONN_MODE = connection_mode.IP` to `CONN_MODE = connection_mode.HOSTNAME`, it will be more convenient if your router somehow allocate new IP for them.

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

### Utility Funcitons

These function will do the action to all the nodes

#### Append or Override a line to a file

> like echo something >> file or echo something > file

```txt
fab --help append-line
Usage: fab [--core-opts] append-line [--options] [other tasks here ...]

Docstring:
  Append (or Override) content in new line in a remote file

Options:
  -l STRING, --line-content=STRING       Contnet to add
  -o, --override                         Override content instead of append
  -r STRING, --remote-file-path=STRING   Path to remote file
  -v, --verbose                          Verbose output
```

Append Exmaple:

```sh
fab append-line "Appending new line" test.txt -v
```

Override Example:

```sh
fab append-line "Overriding line" test.txt -o -v
```

#### Comment or Uncomment a line in a file

```txt
fab --help comment-line
Usage: fab [--core-opts] comment-line [--options] [other tasks here ...]

Docstring:
  Commment or uncomment a line in a remote file

Options:
  -l STRING, --line-content=STRING       Content match to comment (or uncomment)
  -r STRING, --remote-file-path=STRING   Path to remote file
  -u, --uncomment                        Uncomment line instead of comment
  -v, --verbose                          Verbose output
```

Comment Example:

```sh
fab comment-line "Appending new line" test.txt -v
```

Uncomment Example:

```sh
fab comment-line "Appending new line" test.txt -u -v
```

#### Update and then Upgrade

```txt
fab --help update-and-upgrade
Usage: fab [--core-opts] update-and-upgrade [--options] [other tasks here ...]

Docstring:
  apt-update and apt-upgrade (this may take a while)

Options:
  -u, --uncommit   Uncommit deb-src line in Raspbian (testing phase)
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

### Change password

This can change password for all user

Method A. Login with pi and use it as superuser to change other user's password

> This can accept any kind of password.

```txt
$ fab change-passwd pi
What password do you want to set?
```

Method B. Login with that user and then change the password

> This wiil need your current password for that user and your new password can't be too simple.

(with -o flag)

```txt
$ fab change-passwd user -o
What's your current password?
What password do you want to set?
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
