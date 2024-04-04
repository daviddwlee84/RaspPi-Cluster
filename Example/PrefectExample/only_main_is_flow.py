from data_loader import download, preprocess
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


@flow(
    name="Process Feature Set A",
    task_runner=ConcurrentTaskRunner(),
    log_prints=True,
    flow_run_name="Process Feature Set A for {params.ticker}",
)
# def feature_set_a(ticker: str):
def feature_set_a(params: SymbolConfig):
    ticker = params.ticker
    print("Get Raw Data...")
    raw_data = download(ticker)
    print("Preprocess Raw Data...")
    df = preprocess(quote(raw_data))
    print("Processing Features...")
    processed_features = {}
    feature_names = []
    for i in [5, 10]:
        # f_a = feature_a.with_options(cache_key_fn=lambda )(df, i)
        # Actually no need to cache since we calculate it once and use it right away
        f_a = feature_a(df, i)
        processed_features[f"FeatureA({i})"] = f_a
        f_b = feature_b(df, f_a)
        processed_features[f"FeatureB({i})"] = f_b
    f_c = feature_c(df, 20)
    processed_features[f"FeatureC({i})"] = f_c
    result = pd.concat(
        processed_features.values(), keys=processed_features.keys(), axis=1
    )

    create_markdown_artifact(
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)
        key=f"{ticker}-feature-set".lower(),
        markdown=df.describe().to_markdown(),
        description="Data Statistics",
    )

    return result


@flow(
    name="Process All Feature",
    task_runner=ConcurrentTaskRunner(),
    log_prints=True,
    flow_run_name="Process All Feature for {params.ticker}",
)
def all_feature(params: SymbolConfig):
    ticker = params.ticker
    print("Get Raw Data...")
    raw_data = download(ticker)
    print("Preprocess Raw Data...")
    df = preprocess(quote(raw_data))
    print("Processing Features...")
    features = feature_set_a(params)

    result = df.join(features)
    result.dropna(inplace=True)

    create_markdown_artifact(
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)
        key=f"{ticker}-feature-set".lower(),
        markdown=df.describe().to_markdown(),
        description="Data Statistics",
    )

    return result


if __name__ == "__main__":
    # feature_set_a("NVDA")
    # feature_set_a("MSFT")
    # feature_set_a(SymbolConfig(ticker="NVDA"))
    # feature_set_a(SymbolConfig(ticker="MSFT"))
    all_feature(SymbolConfig(ticker="NVDA"))
    all_feature(SymbolConfig(ticker="MSFT"))
