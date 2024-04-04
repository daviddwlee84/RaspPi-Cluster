from typing import Optional
import yfinance as yf
import datetime
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.utilities.annotations import quote
from prefect.artifacts import create_markdown_artifact
import pandas as pd


# class DataLoader:
#     # https://discourse.prefect.io/t/can-i-define-my-tasks-as-classes-rather-than-functions/54
#
#     @flow
#     def get_date(self, ticker: str, start: datetime.date, end: datetime.date):
#         return yf.download([ticker], start, end)
#
#
# if __name__ == "__main__":
#     loader = DataLoader()
#     print(df := loader.get_date("NVDA"))
#     import ipdb
#
#     ipdb.set_trace()


@task(
    name="Download YFinance",
    description="Download ticker data from YFinance.",
    tags=["data", "download"],
    cache_key_fn=task_input_hash,
)
def download(
    ticker: str,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
):
    """
    Finished in state Cached(type=COMPLETED)
    """
    return yf.download([ticker], start, end)


@task(
    name="Preprocessing",
    description="Convert data to float16 to save space.",
    tags=["data", "preprocess"],
)
def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    return data.astype("float16")


# Use log_prints will turn print into log
@flow(name="Get Ticker Data", log_prints=True)
def get_date(
    ticker: str,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    do_preprocessing: bool = False,
):
    """
    TODO: Should have a cache & persistent data way
    Found that do_preprocessing is not
    """
    logger = get_run_logger()
    # df = download(ticker, start, end)
    state = download(ticker, start, end, return_state=True)
    if state.is_failed():
        logger.warn(f"{ticker} download failed")
        return None
    df = state.result()

    logger.info(f"{ticker} downloaded")
    if do_preprocessing:
        df = preprocess(quote(df))
        logger.info(f"{ticker} preprocessed")

    # This should be a entire dataset level report.
    create_markdown_artifact(
        # Artifact key must only contain lowercase letters, numbers, and dashes. (type=value_error)
        key=f"{ticker}-data".lower(),
        markdown=df.describe().to_markdown(),
        description="Data Statistics",
    )
    return df


if __name__ == "__main__":
    # Normal flow
    print(df := get_date("NVDA").Close)
    # Do preprocessing (condition in flow)
    print(df2 := get_date("AAPL", do_preprocessing=True).Close)
    # Call task directly (not recommend)
    # RuntimeError: Tasks cannot be run outside of a flow. To call the underlying task function outside of a flow use `task.fn()`.
    print(df3 := download.fn("NVDA").Close)
    # Use cache
    print(df4 := get_date("NVDA", do_preprocessing=True).Close)
    # Failed
    print(get_date("Failed"))
    import ipdb

    ipdb.set_trace()
