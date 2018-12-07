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
