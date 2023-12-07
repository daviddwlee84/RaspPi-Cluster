# Distributed LightGBM

## Dask + LightGBM

* [Dask - Distributed Learning Guide — LightGBM 4.1.0.99 documentation](https://lightgbm.readthedocs.io/en/latest/Parallel-Learning-Guide.html#dask)

```bash
# start Dask cluster like this
dask-ssh 192.168.0.{235,236,237} --scheduler 192.168.0.236
```

```python
import dask.array as da
import lightgbm as lgb
from sklearn.datasets import make_regression
from distributed import Client, wait

client = Client(address="tcp://192.168.0.236:8786")

# starting with clean workers
# client.restart()

EARLY_STOP_ROUND = 20
NUM_ITERATION = 1000
LEARNING_RATE = 0.01

# adding callbacks
callbacks = []
eval_result = {}
record_evaluation_callback = lgb.record_evaluation(eval_result)
callbacks.append(record_evaluation_callback)
log_evaluation_callback = lgb.log_evaluation()
callbacks.append(log_evaluation_callback)
early_stopping_callback = lgb.early_stopping(EARLY_STOP_ROUND)
callbacks.append(early_stopping_callback)

# creating sample regression data
X_np, y_np = make_regression(n_samples=1000, n_features=10)
row_chunks = (100, 100, 100, 100, 100, 100, 100, 100, 100, 100)
X = da.from_array(X_np, chunks=(row_chunks, (10,)))
y = da.from_array(y_np, chunks=(row_chunks))
X_test_np, y_test_np = make_regression(n_samples=300, n_features=10)
test_row_chunks = (100, 100, 100)
X_test = da.from_array(X_test_np, chunks=(test_row_chunks, (10,)))
y_test = da.from_array(y_test_np, chunks=(test_row_chunks))

# persist() + wait() + rebalance() to get an even spread of the data across workers
X = X.persist()
y = y.persist()
X_test = client.persist(X_test)
y_test = client.persist(y_test)
_ = wait([X, y, X_test, y_test])
client.rebalance()

# training
model = lgb.DaskLGBMRegressor(num_iterations=NUM_ITERATION, learning_rate=LEARNING_RATE).fit(
    X, y, eval_set=[(X_test, y_test)], eval_names=['test'], callbacks=callbacks)
```

## Ray + LightGBM

* [ray-project/lightgbm_ray: LightGBM on Ray](https://github.com/ray-project/lightgbm_ray)
* [Using LightGBM with Tune — Ray 2.8.0](https://docs.ray.io/en/latest/tune/examples/lightgbm_example.html)

## Spark + LightGBM (SynapseML)

* [SynapseML | SynapseML](https://microsoft.github.io/SynapseML/)

1. Install Hadoop and configure cluster then start YARN
2. Install Spark and configure YARN related setting
3. Start PySpark and set master to YARN and install SynapseML package
