from typing import List, Type
from prefect import flow, task, Flow
from prefect.utilities.annotations import quote
from prefect.task_runners import ConcurrentTaskRunner
from data_loader import get_date, download
import pandas as pd


class BaseFeature:
    """
    The reason of using Flow in feature is that different feature might require different input, we would prepare for them
    """

    @task(name="Feature Calculation", tags=["Feature"])
    def calc(df: pd.DataFrame):
        raise NotImplementedError()

    @flow(name="Feature Flow")
    def flow(ticker: str):
        # df = get_date()
        df = download(ticker)
        return BaseFeature.calc(df)


class FeatureA(BaseFeature):

    name: str = "FeatureB"

    @task(name="Feature A Calculation", tags=["Feature", "FeatureA"])
    def calc(df: pd.DataFrame):
        return df.Close.rolling(10).mean()

    @flow(name="FeatureA Flow", persist_result=True)
    def flow(ticker: str):
        # df = get_date(ticker)
        df = download(ticker)
        return FeatureA.calc(quote(df))


class FeatureB(BaseFeature):
    """
    Assume depend on FeatureA
    """

    name: str = "FeatureB"

    @task(name="Feature B Calculation", tags=["Feature", "FeatureB"])
    def calc(df: pd.DataFrame, feature_a_result: pd.DataFrame):
        return df.Close.rolling(10).mean() + feature_a_result

    @flow(name="FeatureB Flow", persist_result=True)
    def flow(ticker: str):
        # df = get_date(ticker)
        df = download(ticker)
        # feature_a_result = FeatureA.calc(df)
        feature_a_result = FeatureA.flow(ticker)
        return FeatureB.calc(quote(df), quote(feature_a_result))


@flow(
    name="Process All Features of Ticker",
    description="Process all given feature of a ticker concurrently.",
    persist_result=False,
    task_runner=ConcurrentTaskRunner(),
)
def feature_processing(ticker: str, features: List[Type[BaseFeature]]):
    results = {}
    for feature in features:
        results[feature.name] = feature.flow(ticker)
    # TypeError: unhashable type: 'dict_keys'
    return pd.concat(results.values(), keys=results.keys(), axis=1)


if __name__ == "__main__":
    # print(FeatureA.flow("NVDA"))
    # print(FeatureB.flow("NVDA"))

    print(result := feature_processing("MSFT", [FeatureA, FeatureB]))
    print(result2 := feature_processing("MSFT", [FeatureB, FeatureA]))

    import ipdb

    ipdb.set_trace()
