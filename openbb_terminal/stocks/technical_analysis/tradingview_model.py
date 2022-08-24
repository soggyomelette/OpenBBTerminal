"""Tradingview model"""
__docformat__ = "numpy"

import logging

import pandas as pd
import requests
from tradingview_ta import TA_Handler

from openbb_terminal import config_terminal as cfg
from openbb_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)

INTERVALS = {
    "1m": "1 min",
    "5m": "5 min",
    "15m": "15 min",
    "1h": "1 hour",
    "4h": "4 hours",
    "1d": "1 day",
    "1W": "1 week",
    "1M": "1 month",
}

SCREENERS = ["crypto", "forex", "cfd"]


@log_start_end(log=logger)
def get_tradingview_recommendation(
    symbol: str, screener: str = "america", exchange: str = "", interval: str = ""
) -> pd.DataFrame:
    """Get tradingview recommendation based on technical indicators

    Parameters
    ----------
    symbol : str
        Ticker symbol to get the recommendation from tradingview based on technical indicators
    screener : str
        Screener based on tradingview docs https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
    exchange: str
        Exchange based on tradingview docs https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
    interval: str
        Interval time to check technical indicators and correspondent recommendation

    Returns
    -------
    df_recommendation: pd.DataFrame
        Dataframe of tradingview recommendations based on technical indicators
    """

    if not exchange:
        s_req = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={cfg.API_KEY_ALPHAVANTAGE}"
        result = requests.get(s_req, stream=True)
        exchange = result.json()["Exchange"]

    if interval:
        intervals = [interval]
    else:
        intervals = ["1M", "1W", "1d", "4h", "1h", "15m", "5m", "1m"]

    df_recommendation = pd.DataFrame()
    index_recommendation = []
    for an_interval in intervals:
        # If the returned data was successful
        if result.status_code == 200:
            stock_recommendation = TA_Handler(
                symbol=symbol,
                screener=screener,
                exchange=exchange,
                interval=an_interval,
            )
            d_recommendation = stock_recommendation.get_analysis().summary
            df_recommendation = pd.concat(
                [
                    pd.DataFrame.from_dict(d_recommendation, orient="index").T,
                    df_recommendation,
                ],
                axis=0,
            )
            index_recommendation.append(INTERVALS[an_interval])
        df_recommendation.index = index_recommendation
        df_recommendation[["BUY", "NEUTRAL", "SELL"]] = df_recommendation[
            ["BUY", "NEUTRAL", "SELL"]
        ].astype(int)

    df_recommendation.index.name = "Interval"

    return df_recommendation
