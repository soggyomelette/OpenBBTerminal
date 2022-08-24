""" Finnhub Model """
__docformat__ = "numpy"

import logging

import pandas as pd
import requests

from openbb_terminal import config_terminal as cfg
from openbb_terminal.decorators import log_start_end
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_rating_over_time(symbol: str) -> pd.DataFrame:
    """Get rating over time data. [Source: Finnhub]

    Parameters
    ----------
    symbol : str
        Ticker symbol to get ratings from

    Returns
    -------
    pd.DataFrame
        Get dataframe with ratings
    """
    response = requests.get(
        f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={cfg.API_FINNHUB_KEY}"
    )
    df = pd.DataFrame()

    if response.status_code == 200:
        if response.json():
            df = pd.DataFrame(response.json())
        else:
            console.print("No ratings over time found", "\n")
    elif response.status_code == 401:
        console.print("[red]Invalid API Key[/red]\n")
    elif response.status_code == 403:
        console.print("[red]API Key not authorized for Premium Feature[/red]\n")
    else:
        console.print(f"Error in request: {response.json()['error']}", "\n")

    return df
