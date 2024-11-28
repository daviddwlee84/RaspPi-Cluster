# Slurm Workload Manager

> Simple Linux Utility for Resource Management (SLURM)

* [Slurm Workload Manager - Overview](https://slurm.schedmd.com/overview.html)
    * [Slurm Workload Manager - REST API Reference](https://slurm.schedmd.com/rest.html)
* [Slurm Workload Manager - Wikipedia](https://en.wikipedia.org/wiki/Slurm_Workload_Manager)
* [SchedMD/slurm: Slurm: A Highly Scalable Workload Manager](https://github.com/SchedMD/slurm)
* [Slurm 作业调度系统 - 上海交大超算平台用户手册](https://docs.hpc.sjtu.edu.cn/job/slurm.html)

![arch](https://slurm.schedmd.com/arch.gif)

---

* [facebookincubator/submitit: Python 3.8+ toolbox for submitting jobs to Slurm](https://github.com/facebookincubator/submitit)
* [dask/dask-jobqueue: Deploy Dask on job schedulers like PBS, SLURM, and SGE](https://github.com/dask/dask-jobqueue)
    * [dask_jobqueue.SLURMCluster — Dask-jobqueue 0.9.0+3.gb07308e documentation](https://jobqueue.dask.org/en/latest/generated/dask_jobqueue.SLURMCluster.html)
    * [Example Deployments — Dask-jobqueue 0.9.0+3.gb07308e documentation](https://jobqueue.dask.org/en/latest/clusters-example-deployments.html)
* [Deploying on Slurm — Ray 2.39.0](https://docs.ray.io/en/latest/cluster/vms/user-guides/community/slurm.html?utm_source=chatgpt.com#python-interface-slurm-scripts)
    * [slurm-launch.py — Ray 2.39.0](https://docs.ray.io/en/latest/cluster/vms/user-guides/community/slurm-launch.html#slurm-launch)
    * [slurm-template.sh — Ray 2.39.0](https://docs.ray.io/en/latest/cluster/vms/user-guides/community/slurm-template.html#slurm-template)

---

Quick run in Docker

* [SciDAS/slurm-in-docker: Slurm in Docker - Exploring Slurm using CentOS 7 based Docker images](https://github.com/SciDAS/slurm-in-docker)
* [nathan-hess/docker-slurm: Docker images with Slurm Workload Manager installed](https://github.com/nathan-hess/docker-slurm)
* [**giovtorres/slurm-docker-cluster: A Slurm cluster using docker-compose**](https://github.com/giovtorres/slurm-docker-cluster)

```sh
git clone https://github.com/giovtorres/slurm-docker-cluster.git
cd slurm-docker-cluster

# This will use version in .env
docker compose build
```
