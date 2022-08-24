"""Tradingview view"""
__docformat__ = "numpy"

import logging
import os

from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data, print_rich_table
from openbb_terminal.stocks.technical_analysis import tradingview_model

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def print_recommendation(
    symbol: str,
    screener: str = "america",
    exchange: str = "",
    interval: str = "",
    export: str = "",
):
    """Print tradingview recommendation based on technical indicators

    Parameters
    ----------
    symbol : str
        Ticker symbol to get tradingview recommendation based on technical indicators
    screener : str
        Screener based on tradingview docs https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
    exchange: str
        Exchange based on tradingview docs https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
    interval: str
        Interval time to check technical indicators and correspondent recommendation
    export: str
        Format of export file
    """

    recom = tradingview_model.get_tradingview_recommendation(
        symbol, screener, exchange, interval
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "recom",
        recom,
    )
    print_rich_table(
        recom,
        headers=list(recom.columns),
        title="Ticker Recommendation",
        show_index=True,
    )
