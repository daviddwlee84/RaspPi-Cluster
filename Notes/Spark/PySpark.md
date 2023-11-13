# PySpark

## Docker

* [jupyter/pyspark-notebook - Docker Image | Docker Hub](https://hub.docker.com/r/jupyter/pyspark-notebook)
    * [jupyter/docker-stacks: Ready-to-run Docker images containing Jupyter applications](https://github.com/jupyter/docker-stacks)
* [apache/spark-py - Docker Image | Docker Hub](https://hub.docker.com/r/apache/spark-py)

### Docker + YARN

```bash
# not working
docker run -it apache/spark-py /opt/spark/bin/pyspark --master yarn
```

### Docker + Kubernetes
