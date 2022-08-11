""" Short Interest View """
__docformat__ = "numpy"

import logging
import os

from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data, print_rich_table
from openbb_terminal.stocks.discovery import shortinterest_model
from openbb_terminal.stocks.discovery import yahoofinance_model as yf_model
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def low_float(num: int, export: str):
    """Prints top N low float stocks from https://www.lowfloat.com

    Parameters
    ----------
    num: int
        Number of stocks to display
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df_low_float = shortinterest_model.get_low_float()
    df_low_float = df_low_float.iloc[1:].head(n=num)

    print_rich_table(
        df_low_float,
        headers=list(df_low_float.columns),
        show_index=False,
        title="Top Float Stocks",
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "lowfloat",
        df_low_float,
    )


@log_start_end(log=logger)
def hot_penny_stocks(num: int = 10, export: str = "", source: str = "yf"):
    """Prints top N hot penny stocks from https://www.pennystockflow.com

    Parameters
    ----------
    num: int
        Number of stocks to display
    export : str
        Export dataframe data to csv,json,xlsx file
    source : where to get the data from. Choose from:
    yf (yfinance), or psf (pennystockflow)
    """
    if source == "yf":
        df_penny_stocks = yf_model.get_hotpenny()
    elif source == "psf":
        console.print("[red]Data from this source is often not penny stocks[/red]\n")
        df_penny_stocks = shortinterest_model.get_today_hot_penny_stocks()
    else:
        console.print("[red]Invalid source provided[/red]\n")
        return

    print_rich_table(
        df_penny_stocks.head(num),
        headers=list(df_penny_stocks.columns) if source != "psf" else None,
        show_index=False,
        title="Top Penny Stocks",
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "hotpenny",
        df_penny_stocks,
    )
