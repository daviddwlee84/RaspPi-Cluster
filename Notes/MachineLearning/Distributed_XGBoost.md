# Distributed XGBoost

## Dask + XGBoost

## Spark + XGBoost

## Ray + XGBoost

* [Difference between xgboost_ray and XGBoostTrainer? - Ray Libraries (Data, Train, Tune, Serve) - Ray](https://discuss.ray.io/t/difference-between-xgboost-ray-and-xgboosttrainer/8459)

> XGBoostTrainer uses xgboost_ray underneath and provides a Ray AIR-compatible API. If you are a new user, using XGBoostTrainer over xgboost_ray is recommended. That being said, xgboost_ray supports some extra data formats and elastic training, while those features are not yet present in XGBoostTrainer API.

* [Introducing Distributed XGBoost Training with Ray | Anyscale](https://www.anyscale.com/blog/distributed-xgboost-training-with-ray)
  * [Distributed XGBoost on Ray - YouTube](https://www.youtube.com/watch?v=N49_mRCm4_4)
* [Get Started with XGBoost and LightGBM — Ray 2.8.1](https://docs.ray.io/en/latest/train/distributed-xgboost-lightgbm.html#how-to-optimize-xgboost-memory-usage)

> XGBoost uses a compute-optimized datastructure, the DMatrix, to hold training data. When converting a dataset to a DMatrix, XGBoost creates intermediate copies and ends up holding a complete copy of the full data. XGBoost converts the data into the local data format. On a 64-bit system the format is 64-bit floats. Depending on the system and original dataset dtype, this matrix can thus occupy more memory than the original dataset.
>
> The peak memory usage for CPU-based training is at least 3x the dataset size, assuming dtype float32 on a 64-bit system, plus about 400,000 KiB for other resources, like operating system requirements and storing of intermediate results.

### Ray XGBoost Trainer

- [Get Started with XGBoost and LightGBM — Ray 2.8.0](https://docs.ray.io/en/latest/train/distributed-xgboost-lightgbm.html)

### XGBoost_Ray

* [ray-project/xgboost_ray: Distributed XGBoost on Ray](https://github.com/ray-project/xgboost_ray)
* [Distributed XGBoost with Ray — xgboost 2.0.2 documentation](https://xgboost.readthedocs.io/en/stable/tutorials/ray.html)
* [Tuning XGBoost hyperparameters with Ray Tune — Ray 2.8.1](https://docs.ray.io/en/latest/tune/examples/tune-xgboost.html#early-stopping)

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xgboost_ray
```

* [Tuning xgboost with early stopping - Ray Libraries (Data, Train, Tune, Serve) / Ray Tune - Ray](https://discuss.ray.io/t/tuning-xgboost-with-early-stopping/75/5)
* [tune-sklearn/examples/xgbclassifier.py at master · ray-project/tune-sklearn](https://github.com/ray-project/tune-sklearn/blob/master/examples/xgbclassifier.py)

### Logging

* [Logging and Outputs in Tune — Ray 2.8.0](https://docs.ray.io/en/latest/tune/tutorials/tune-output.html#how-to-log-your-tune-runs-to-tensorboard)

---

## External Memory

* [Using XGBoost External Memory Version — xgboost 2.1.0-dev documentation](https://xgboost.readthedocs.io/en/latest/tutorials/external_memory.html)
* [Experimental support for external memory — xgboost 2.1.0-dev documentation](https://xgboost.readthedocs.io/en/latest/python/examples/external_memory.html)

## Parameters

* [XGBoost Parameters — xgboost 2.0.3 documentation](https://xgboost.readthedocs.io/en/stable/parameter.html)
