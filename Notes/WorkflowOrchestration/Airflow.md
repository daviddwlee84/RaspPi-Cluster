# Apache Airflow

* [Apache Airflow](https://airflow.apache.org/)
* [apache/airflow: Apache Airflow - A platform to programmatically author, schedule, and monitor workflows](https://github.com/apache/airflow)

## Getting Started

* [Quick Start — Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

```bash
export AIRFLOW_HOME=~/airflow

AIRFLOW_VERSION=2.8.4

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.8.4 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.8.4/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

---

* [anyscale/airflow-provider-ray: Ray provider for Apache Airflow](https://github.com/anyscale/airflow-provider-ray)
* [Deploying Ray for ML platforms — Ray 2.10.0](https://docs.ray.io/en/latest/ray-air/deployment.html)
