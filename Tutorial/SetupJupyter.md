# Setup Jupyter with PySpark and Parallel IPython

Install Jupyter Notebook at once!

```sh
fab install-jupyter
```

Only jupyter

```sh
# This will install in /usr/local/bin (share with all user)
sudo pip3 install jupyter
# This will install in ~/.local/bin
pip3 install --user jupyter
```

## Jupyter Notebook Server

* [Jupyter Notebook Doc - Running a notebook server](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html)

```sh
jupyter notebook --generate-config

# Setup password
jupyter notebook password
```

Start the server

```sh
jupyter notebook --ip <your_LAN_ip> --port 8888
```

* [https://stackoverflow.com/questions/39155953/exposing-python-jupyter-on-lan](https://stackoverflow.com/questions/39155953/exposing-python-jupyter-on-lan)

Either use password or token or ... to login

## PySpark with Jupyter Notebook

* [Get Started with PySpark and Jupyter Notebook in 3 Minutes](https://blog.sicara.com/get-started-pyspark-jupyter-guide-tutorial-ae2fe84f594f)
* [How to set up PySpark for your Jupyter notebook](https://medium.freecodecamp.org/how-to-set-up-pyspark-for-your-jupyter-notebook-7399dd3cb389)

## Interactive Parallel Computing with IPython

> Haven't tried yet

* [ipyparallel Github](https://github.com/ipython/ipyparallel)
* [ipyparallel documents](https://ipyparallel.readthedocs.io/en/latest/)

## Online Jupyter Notebook Server

### Google Colaboratory

```jupyter
# Put at the start of the notebook
!apt-get -y install openjdk-8-jre-headless
!pip install pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
spark = SparkSession.builder.master("local").getOrCreate()
sc = SparkContext.getOrCreate()
```

* [使用 Google Colaboratory 跑 PySpark](https://medium.com/@chiayinchen/%E4%BD%BF%E7%94%A8-google-colaboratory-%E8%B7%91-pyspark-625a07c75000)
* [Apache Spark on Google Colaboratory](https://mikestaszel.com/2018/03/07/apache-spark-on-google-colaboratory/)

### AWS SageMaker

* [Build Amazon SageMaker notebooks backed by Spark in Amazon EMR](https://aws.amazon.com/blogs/machine-learning/build-amazon-sagemaker-notebooks-backed-by-spark-in-amazon-emr/)
