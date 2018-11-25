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

### Upload and unpack

1. Upload hadoop-3.1.1.tar.gz to each node
2. Extract it
3. Move to /opt

### Setup hadoop user name and group

1. Add hadoop group
2. Add hadoop user to hadoop group
3. Add hadoop user to sudo group

### Generate ssh key for hadoop user

1. Generate ssh key and corresopnding authorized_keys in local (`./temp_files/hadoopSSH`)
2. Upload keys to remote by using hadoop user
    * it will first remove files to make sure it's the newest version

## TODO

* fix IP (maybe)
* chown
* configuration files
    * node number dynamic config
