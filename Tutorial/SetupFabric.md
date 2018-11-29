# Fabric

A simple getting started guide of composing fabfile.

[fabfile.py](fabfile.py)

## Installation

`pip install fabric`

## Basic usage

Create a file called `fabfile.py` in your working directory.

### Make a invokable "Task"

You can use `fab` command to call your "Task" in CLI

`fab --list`: List your tasks

`fab task_name [args...]`: Invoke your funciton in CLI

There must be a default argument in your function (different from fabric 1.x). Here we called it `ctx`.

```python
from fabric import task

@task
def task_name(ctx, arg):
    print(arg)
```

* [CLI Guild](http://docs.pyinvoke.org/en/latest/getting-started.html)

### Send a command to all the cluster

#### Old-fashioned way (list with loop)

```python
from fabric import Connection

hosts = [
    'pi@192.168.1.100',
    'pi@192.168.1.114',
    'pi@192.168.1.115',
    'pi@192.168.1.116',
]

piPassword = 'raspberry'

@task
def CMD(ctx, command):
    print("Sending commend")
    for host in hosts:
        result = Connection(host, connect_kwargs={'password': piPassword}).run(command, hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        print(msg.format(result))
```

Example: `fab CMD 'echo 'haha''`

#### Groups

SerialGroup and ThreadingGroup

* [api - group](http://docs.fabfile.org/en/2.4/api/group.html)
* [getting started - multiple servers](http://docs.fabfile.org/en/2.4/getting-started.html#multiple-servers)

## Links

Fabric

* [Official Website](https://www.fabfile.org/)
    * [Getting Started](https://docs.fabfile.org/en/latest/getting-started.html#)
* [Github](https://github.com/fabric/fabric/)

Trouble Shooting

* [What does the “at” (@) symbol do in Python?](https://stackoverflow.com/questions/6392739/what-does-the-at-symbol-do-in-python)
* [TypeError: Tasks must have an initial Context argument!](https://github.com/pyinvoke/invoke/issues/362)
* [Converting list to *args when calling function](https://stackoverflow.com/questions/3941517/converting-list-to-args-when-calling-function) - *HOSTS

* [Adding a line into the hosts file, getting permission denied when using sudo - Mac](https://superuser.com/questions/538760/adding-a-line-into-the-hosts-file-getting-permission-denied-when-using-sudo-m)
