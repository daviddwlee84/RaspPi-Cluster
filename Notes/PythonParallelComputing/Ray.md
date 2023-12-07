# Ray

## Setup Cluster

* [Launching an On-Premise Cluster — Ray 2.8.0](https://docs.ray.io/en/latest/cluster/vms/user-guides/launching-clusters/on-premises.html)

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ray[default]
```

> If found error [`TypeError: issubclass() arg 1 must be a class`](https://github.com/langchain-ai/langchain/issues/5113#issuecomment-1558493486):
>
> ```bash
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple typing-inspect==0.8.0 typing_extensions==4.5.0
> ```

### Local Cluster

```python
import ray
ray.init()
# 2023-11-21 16:28:43,072 INFO worker.py:1664 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8266
# RayContext(dashboard_url='127.0.0.1:8266', python_version='3.8.13', ray_version='2.8.0', ray_commit='105355bd253d6538ed34d331f6a4bdf0e38ace3a', protocol_version=None)

# You can do port forwarding like
# ssh username@ssh-ip -N -f -L local_port:remote_IP:remote_port
```

### Cluster

Head Node

```bash
ray start --head --node-ip-address 192.168.222.235 --port 6379 --dashboard-host 0.0.0.0 --dashboard-port 8265
```

Worker Node

* [Collecting and monitoring metrics — Ray 2.8.0](https://docs.ray.io/en/latest/cluster/metrics.html)

## Raylet


## Storage

* [Configuring Persistent Storage — Ray 2.8.0](https://docs.ray.io/en/latest/train/user-guides/persistent-storage.html)
    * Cloud Storage (AWS S3, Google Cloud Storage)
    * Shared filesystem (NFS, HDFS)

## Ray Dataset

* [**Ray Datasets for large-scale machine learning ingest and scoring | Anyscale**](https://www.anyscale.com/blog/ray-datasets-for-machine-learning-training-and-scoring)

## Dask on Ray

* [Using Dask on Ray — Ray 2.8.0](https://docs.ray.io/en/latest/ray-more-libs/dask-on-ray.html)

## Runtime Environment

* [Environment Dependencies — Ray 2.8.0](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html)
    * `ray.init(runtime_env={'working_dir': '...', 'excludes': ['...']}, ...)`
* [ray.runtime_env.RuntimeEnv — Ray 2.8.0](https://docs.ray.io/en/latest/ray-core/api/doc/ray.runtime_env.RuntimeEnv.html)
* [Exclude files/folders in workdir using Runtime Environments - Ray Core - Ray](https://discuss.ray.io/t/exclude-files-folders-in-workdir-using-runtime-environments/3080/2)

## Links

* [maxpumperla/learning_ray: Notebooks for the O'Reilly book "Learning Ray"](https://github.com/maxpumperla/learning_ray/)
    * [Learning Ray - Flexible Distributed Python for Machine Learning](https://maxpumperla.com/learning_ray/)
