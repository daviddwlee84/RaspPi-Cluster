# Distributed XGBoost

## Dask + XGBoost

## Spark + XGBoost

## Ray + XGBoost

- [Difference between xgboost_ray and XGBoostTrainer? - Ray Libraries (Data, Train, Tune, Serve) - Ray](https://discuss.ray.io/t/difference-between-xgboost-ray-and-xgboosttrainer/8459)

> XGBoostTrainer uses xgboost_ray underneath and provides a Ray AIR-compatible API. If you are a new user, using XGBoostTrainer over xgboost_ray is recommended. That being said, xgboost_ray supports some extra data formats and elastic training, while those features are not yet present in XGBoostTrainer API.

- [Introducing Distributed XGBoost Training with Ray | Anyscale](https://www.anyscale.com/blog/distributed-xgboost-training-with-ray)
  - [Distributed XGBoost on Ray - YouTube](https://www.youtube.com/watch?v=N49_mRCm4_4)

### Ray XGBoost Trainer

- [Get Started with XGBoost and LightGBM — Ray 2.8.0](https://docs.ray.io/en/latest/train/distributed-xgboost-lightgbm.html)

### XGBoost_Ray

- [ray-project/xgboost_ray: Distributed XGBoost on Ray](https://github.com/ray-project/xgboost_ray)
- [Distributed XGBoost with Ray — xgboost 2.0.2 documentation](https://xgboost.readthedocs.io/en/stable/tutorials/ray.html)

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xgboost_ray
```

- [Tuning xgboost with early stopping - Ray Libraries (Data, Train, Tune, Serve) / Ray Tune - Ray](https://discuss.ray.io/t/tuning-xgboost-with-early-stopping/75/5)
- [tune-sklearn/examples/xgbclassifier.py at master · ray-project/tune-sklearn](https://github.com/ray-project/tune-sklearn/blob/master/examples/xgbclassifier.py)

### Logging

- [Logging and Outputs in Tune — Ray 2.8.0](https://docs.ray.io/en/latest/tune/tutorials/tune-output.html#how-to-log-your-tune-runs-to-tensorboard)
