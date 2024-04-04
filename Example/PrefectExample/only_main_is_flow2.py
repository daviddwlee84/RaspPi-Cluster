from data_loader import get_date
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from prefect.utilities.annotations import quote
from pydantic import BaseModel
import pandas as pd
from prefect.artifacts import create_markdown_artifact


class SymbolConfig(BaseModel):
    ticker: str


@task(name="Feature A", task_run_name="FeatureA({window})")
def feature_a(df: pd.DataFrame, window: int, tags=["Feature"]):
    return df.Close.rolling(window).mean()


@task(name="Feature B", description="Depends on Feature A", tags=["Feature"])
def feature_b(df: pd.DataFrame, feature_a: pd.Series):
    return df.Close + feature_a


@task(
    name="Feature C", description="Depends on Feature A and Feature B", tags=["Feature"]
)
def feature_c(df: pd.DataFrame, c: int):
    return df.Close * c


# @flow(
#     name="Process Feature Set A",
#     task_runner=ConcurrentTaskRunner(),
#     log_prints=True,
# )
# def feature_set_a(df: pd.DataFrame):
#     print("Processing Feature Set A...")
#     processed_features = {}
#     feature_names = []
#     for i in [5, 10]:
#         f_a = feature_a(df, i)
#         processed_features[f"FeatureA({i})"] = f_a
#         f_b = feature_b(df, f_a)
#         processed_features[f"FeatureB({i})"] = f_b
#     f_c = feature_c(df, 20)
#     processed_features[f"FeatureC({i})"] = f_c
#     result = pd.concat(
#         processed_features.values(), keys=processed_features.keys(), axis=1
#     )
#
#     return result


@flow(
    name="Process Feature Set A",
    task_runner=ConcurrentTaskRunner(),
    log_prints=True,
)
def feature_set_a(df: pd.DataFrame):
    print("Processing Feature Set A...")
    processed_features = {}
    feature_names = []
    # Quote every dataframe
    # If use quote then we won't be able to see the dependency on Prefect Server UI
    for i in [5, 10]:
        f_a = feature_a(quote(df), i)
        processed_features[f"FeatureA({i})"] = f_a
        f_b = feature_b(quote(df), quote(f_a))
        processed_features[f"FeatureB({i})"] = f_b
    f_c = feature_c(quote(df), 20)
    processed_features[f"FeatureC({i})"] = f_c
    result = pd.concat(
        processed_features.values(), keys=processed_features.keys(), axis=1
    )

    return result


@flow(
    name="Process All Feature",
    task_runner=ConcurrentTaskRunner(),
    log_prints=True,
    flow_run_name="Process All Feature for {params.ticker}",
)
def all_feature(params: SymbolConfig):
    # https://docs.prefect.io/latest/api-ref/prefect/flows/#prefect.flows.Flow.with_options
    df = get_date.with_options(flow_run_name=f"Get Data of {params.ticker}")(
        params.ticker
    )
    print("Processing Features...")
    features = feature_set_a.with_options(
        flow_run_name=f"Create Feature set A of {params.ticker}"
    )(df)

    result = df.join(features)
    result.dropna(inplace=True)

    create_markdown_artifact(
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)
        key=f"{params.ticker}-all-data".lower(),
        markdown=df.describe().to_markdown(),
        description="Data Statistics",
    )

    return result


if __name__ == "__main__":
    print(all_feature(SymbolConfig(ticker="NVDA")))
    print(all_feature(SymbolConfig(ticker="MSFT")))

    # This way we would be hard to select feature by column since it is generate it on the fly
    # And hard to pre-config what feature we want to create, since by default we will create them all
