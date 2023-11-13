# Kubernetes

## Concept

* Nodes
* Pods

## Variation

### Kubeadm

> Kubeadm is a tool built to provide kubeadm init and kubeadm join as best-practice "fast paths" for creating Kubernetes clusters.

* [Kubeadm | Kubernetes](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)

### MicroK8s

> Based on `snap`

```bash
sudo snap info microk8s
```

* [MicroK8s - Zero-ops Kubernetes for developers, edge and IoT](https://microk8s.io/)
* [Install microk8s on Linux | Snap Store](https://snapcraft.io/microk8s) 
* [canonical/microk8s: MicroK8s is a small, fast, single-package Kubernetes for datacenters and the edge.](https://github.com/canonical/microk8s)

```bash
sudo snap install microk8s --classic

sudo usermod -a -G microk8s $USER
newgrp microk8s

# Check installation
microk8s kubectl get nodes
microk8s status
```

Dashboard

```bash
microk8s enable dashboard
```

* [url - How to access micro8ks's dashboard web UI? - Ask Ubuntu](https://askubuntu.com/questions/1123996/how-to-access-micro8kss-dashboard-web-ui)
* [dashboard/docs/user/access-control/creating-sample-user.md at master · kubernetes/dashboard](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md)
* [dashboard/docs/user/access-control/README.md at master · kubernetes/dashboard](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/README.md)

`chrome://flags/#allow-insecure-localhost`
`chrome://flags/#block-insecure-private-network-requests`

```
token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s kubectl -n kube-system describe secret $token
microk8s kubectl port-forward -n kube-system --address 0.0.0.0 service/kubernetes-dashboard 10443:443

microk8s dashboard-proxy
```

#### MicroK8s in GFW

> [microk8s is not running. microk8s.inspect showing no error · Issue #886 · canonical/microk8s (github.com)](https://github.com/canonical/microk8s/issues/886#issuecomment-1256861859)

Some default Kubernetes Add-ons might not successfully pulled.

Pulled from mirror and re-tag them.

* [microk8s 搭建 - 肖祥 - 博客园](https://www.cnblogs.com/xiao987334176/p/10931290.html)
* [国内microk8s安装指南 | 猿明园](https://www.omingo.cn/2019/06/21/%E5%9B%BD%E5%86%85microk8s%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97/)

This old version has `microk8s.docker`, while new version use system docker. Which the "mirror clone" trick might not work.

```bash
# No microk8s.add-node command
# sudo snap install microk8s --classic --channel=1.12/stable
# No microk8s.docker command => use microk8s.ctr image import instead
sudo snap install microk8s --classic --channel=1.18/stable
```

* [K8S(kubernetes)镜像源 - HackerVirus - 博客园](https://www.cnblogs.com/Leo_wl/p/15775077.html)
* [It can't be used now · Issue #58 · Azure/container-service-for-azure-china](https://github.com/Azure/container-service-for-azure-china/issues/58)

```bash
docker pull mirrorgooglecontainers/pause:3.1
docker pull mirrorgooglecontainers/heapster-influxdb-amd64:v1.3.3
docker pull mirrorgooglecontainers/heapster-grafana-amd64:v4.4.3
docker pull mirrorgooglecontainers/kubernetes-dashboard-amd64:v1.8.3
docker pull mirrorgooglecontainers/heapster-amd64:v1.5.2
docker pull mirrorgooglecontainers/k8s-dns-dnsmasq-nanny-amd64:1.14.7
docker pull mirrorgooglecontainers/k8s-dns-kube-dns-amd64:1.14.7
docker pull mirrorgooglecontainers/k8s-dns-sidecar-amd64:1.14.7

docker tag mirrorgooglecontainers/pause:3.1 k8s.gcr.io/pause:3.1
docker tag mirrorgooglecontainers/heapster-influxdb-amd64:v1.3.3 k8s.gcr.io/heapster-influxdb-amd64:v1.3.3
docker tag mirrorgooglecontainers/heapster-grafana-amd64:v4.4.3 k8s.gcr.io/heapster-grafana-amd64:v4.4.3
docker tag mirrorgooglecontainers/kubernetes-dashboard-amd64:v1.8.3 k8s.gcr.io/kubernetes-dashboard-amd64:v1.8.3
docker tag mirrorgooglecontainers/heapster-amd64:v1.5.2 k8s.gcr.io/heapster-amd64:v1.5.2
docker tag mirrorgooglecontainers/k8s-dns-dnsmasq-nanny-amd64:1.14.7 gcr.io/google_containers/k8s-dns-dnsmasq-nanny-amd64:1.14.7
docker tag mirrorgooglecontainers/k8s-dns-kube-dns-amd64:1.14.7 gcr.io/google_containers/k8s-dns-kube-dns-amd64:1.14.7
docker tag mirrorgooglecontainers/k8s-dns-sidecar-amd64:1.14.7 gcr.io/google_containers/k8s-dns-sidecar-amd64:1.14.7

docker save k8s.gcr.io/pause > pause.tar
docker save k8s.gcr.io/heapster-influxdb-amd64 > heapster-influxdb-amd64.tar
docker save k8s.gcr.io/heapster-grafana-amd64 > heapster-grafana-amd64.tar
docker save k8s.gcr.io/kubernetes-dashboard-amd64 > kubernetes-dashboard-amd64.tar
docker save k8s.gcr.io/heapster-amd64 > heapster-amd64.tar
docker save gcr.io/google_containers/k8s-dns-dnsmasq-nanny-amd64 > k8s-dns-dnsmasq-nanny-amd64.tar
docker save gcr.io/google_containers/k8s-dns-kube-dns-amd64 > k8s-dns-kube-dns-amd64.tar
docker save gcr.io/google_containers/k8s-dns-sidecar-amd64 > k8s-dns-sidecar-amd64.tar

for file in $(ls *.tar); do
    microk8s ctr --namespace k8s.io image import $file
done
```

* [Pull images from others than k8s.gcr.io · Issue #472 · canonical/microk8s](https://github.com/canonical/microk8s/issues/472)

```bash
$SPARK_HOME/bin/docker-image-tool.sh \
  -t v3.2.1 \
  -p $SPARK_HOME/resource-managers/kubernetes/docker/src/main/dockerfiles/spark/bindings/python/Dockerfile \
  build
```

#### MicroK8s Addon

* [MicroK8s - Addon: dashboard](https://microk8s.io/docs/addon-dashboard)

### Minikube

```bash
# -m is for minikube
$SPARK_HOME/bin/docker-image-tool.sh \
  -m \
  -t v3.2.1 \
  -p $SPARK_HOME/resource-managers/kubernetes/docker/src/main/dockerfiles/spark/bindings/python/Dockerfile \
  build
```

### K3s

## Helm

## Kubernetes + Spark

* [Running Spark on Kubernetes - Spark 3.5.0 Documentation](https://spark.apache.org/docs/latest/running-on-kubernetes.html)



## Links

* [Official Website](https://kubernetes.io/)
    * [Getting started | Kubernetes](https://kubernetes.io/docs/setup/)
    * [Tutorial](https://kubernetes.io/docs/tutorials/)
    * [Concepts](https://kubernetes.io/docs/concepts/)
        * [Understanding Kubernetes Objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
    * [Kubectl Reference Docs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
* Minikube
    * [Running Kubernetes Locally via Minikube](https://kubernetes.io/docs/setup/minikube/)
* Installation
    * [Install and Set Up kubectl on Linux | Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
    * [How to Install Kubernetes - 4 Different Ways [Step-by-Step]](https://spacelift.io/blog/install-kubernetes)
        * Minikube
        * MicroK8s
        * K3s
        * Kubeadm
    * [使用 MicroK8s 架設 Kubernetes 叢集的完整過程解析 | The Will Will Web](https://blog.miniasp.com/post/2021/12/05/Running-Kubernetes-with-MicroK8s) (Using MicroK8s + Multipass + Helm)
        * [Multipass orchestrates virtual Ubuntu instances](https://multipass.run/)
* Tutorial
    * [**Learn Kubernetes with Lessons & Tutorials | Kube by Example**](https://kubebyexample.com/)
* [Helm -The package manager for Kubernetes](https://helm.sh/)
* [kubernetes/dashboard: General-purpose web UI for Kubernetes clusters](https://github.com/kubernetes/dashboard)
    * [dashboard/docs/user/access-control/creating-sample-user.md at master · kubernetes/dashboard](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md)
    * [dashboard/docs/common/dashboard-arguments.md at 1148f7ba9f9eadd719e53fa3bc8bde5b7cfdb395 · kubernetes/dashboard](https://github.com/kubernetes/dashboard/blob/1148f7ba9f9eadd719e53fa3bc8bde5b7cfdb395/docs/common/dashboard-arguments.md#arguments)
    * [kubernetes-dashboard 7.0.0-alpha1 · helm/k8s-dashboard](https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard)
 
--- 

Raspberry Pi

* [Kubernetes at the edge: easy as Pi](https://www.brighttalk.com/webcast/6793/488796)
    * [Kubernetes at the edge: Easy as Pi - YouTube](https://www.youtube.com/watch?v=cB8fNytQXTY)
* [Install microk8s on Raspberry Pi using the Snap Store | Snapcraft](https://snapcraft.io/install/microk8s/raspbian)
