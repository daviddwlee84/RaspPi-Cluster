# Setup Hadoop

* Version here: 3.1.1

## Download Hadoop

We first download Hadoop from official website to `File/`

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
