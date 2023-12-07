# MinIO

## Getting Stared

### MinIO Server

* [Install and Deploy MinIO — MinIO Object Storage for Linux](https://min.io/docs/minio/linux/operations/installation.html#minio-installation)

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio_20231111081441.0.0_amd64.deb
sudo dpkg -i minio_20231111081441.0.0_amd64.deb
# /usr/local/bin/minio
```

```bash
mkdir -p /mnt/sdb/minio
MINIO_ROOT_USER=MYUSER MINIO_ROOT_PASSWORD=MYPASSWORD minio server /mnt/sdb/minio --address ":19000" --console-address ":19001"
```

#### Distributed MinIO Server

* [Deploy MinIO: Multi-Node Multi-Drive — MinIO Object Storage for Linux](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html#minio-mnmd)
* [minio/docs/distributed at master · minio/minio](https://github.com/minio/minio/tree/master/docs/distributed)

> Not working
>
> ```bash
> # Run this on multiple machine (exclude one)
> MINIO_ROOT_USER=MYUSER MINIO_ROOT_PASSWORD=MYPASSWORD minio server /mnt/sdb/minio --address ":19000"
> # Run this on the excluded one
MINIO_ROOT_USER=MYUSER MINIO_ROOT_PASSWORD=MYPASSWORD minio server http://192.168.222.{1,2,3}:19000/mnt/sdb/minio --address ":19000" --console-address ":19001"
> ```
>
> ```bash
> MINIO_ROOT_USER=MYUSER MINIO_ROOT_PASSWORD=MYPASSWORD minio server http://192.168.222.{1,2,3}:19000/mnt/sdb/minio --address ":19000" --console-address ":19001"
> ```

### MinIO Client

* [MinIO Client — MinIO Object Storage for Linux](https://min.io/docs/minio/linux/reference/minio-mc.html)

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mcli_20231110213717.0.0_amd64.deb
dpkg -i mcli_20231110213717.0.0_amd64.deb
```

```bash
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

mc --help

# or

sudo curl https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc
sudo chmod +x /usr/local/bin/mc

mc --help
```

```bash
mcli alias set myminio/ http://MINIO-SERVER-IP:19000 MYUSER MYPASSWORD
# OR
mc alias set 'myminio' 'http://MINIO-SERVER-IP:19000' 'MYUSER' 'MYPASSWORD'
```

```bash
mc admin info myminio
```

```bash
# Make bucket
mc mb myminio/bucket_name

mc cp my_file myminio/bucket_name/my_file
```

### Python

* [Python Quickstart Guide — MinIO Object Storage for Linux](https://min.io/docs/minio/linux/developers/python/minio-py.html)

## Trouble Shooting

* [Troubleshooting — MinIO Object Storage for Linux](https://min.io/docs/minio/linux/operations/troubleshooting.html)

### Your proposed upload size ‘xxx’ exceeds the maximum allowed object size ‘5368709120’ for single PUT operation.


## Links

* [MinIO | High Performance, Kubernetes Native Object Storage](https://min.io/)
* [minio/minio: High Performance Object Storage for AI](https://github.com/minio/minio)
* [minio/mc: Simple | Fast tool to manage MinIO clusters :cloud:](https://github.com/minio/mc)
* [MinIO | Code and downloads to create high performance object storage](https://min.io/download#/linux)
* [Introduction to MinIO | Baeldung](https://www.baeldung.com/minio)
