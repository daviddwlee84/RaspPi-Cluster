# Setup Hadoop

* Version here: 3.1.1

## Download Hadoop

We first download Hadoop from official website to `temp_files/`

```sh
fab download-hadoop
```

### Configure

(if download different version, you should modify some settings in fabfile.py)

* `HADOOP_VERSION`

## Install Hadoop

```sh
fab install-hadoop
```

### Setup hadoop user name and group

1. Add hadoop group
2. Add hadoop user to hadoop group
3. Add hadoop user to sudo group

### Generate ssh key for hadoop user

1. Generate ssh key and corresopnding authorized_keys in local (`./temp_files/hadoopSSH`)
2. Upload keys to remote by using hadoop user
    * it will first remove files to make sure it's the newest version

### Upload, unpack and change owner

1. Upload hadoop-3.1.1.tar.gz to each node
2. Extract it
3. Move to /opt
4. Change owner to hadoop group and user

```py
# SerialGroupt.put() is still pending
# https://github.com/fabric/fabric/issues/1800
# https://github.com/fabric/fabric/issues/1810
# (but it is in the tutorial... http://docs.fabfile.org/en/2.4/getting-started.html#bringing-it-all-together)
```

### Setup environment variable

1. Append setting in /etc/bash.bashrc
2. Source it to apply setting

## TODO

* fix IP (maybe)
* chown
* configuration files
    * node number dynamic config
