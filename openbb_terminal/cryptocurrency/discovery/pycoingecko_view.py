"""CoinGecko view"""
__docformat__ = "numpy"

import logging
import os

from pandas.plotting import register_matplotlib_converters

from openbb_terminal.cryptocurrency.dataframe_helpers import (
    lambda_very_long_number_formatter,
)
from openbb_terminal.cryptocurrency.discovery import pycoingecko_model
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data, print_rich_table
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)

register_matplotlib_converters()

# pylint: disable=R0904, C0302

COINS_COLUMNS = [
    "Symbol",
    "Name",
    "Volume [$]",
    "Market Cap",
    "Market Cap Rank",
    "7D Change [%]",
    "24H Change [%]",
]


@log_start_end(log=logger)
def display_coins(
    category: str, top: int = 250, sortby: str = "Symbol", export: str = ""
) -> None:
    """Display top coins [Source: CoinGecko]

    Parameters
    ----------
    category: str
        If no category is passed it will search for all coins. (E.g., smart-contract-platform)
    top: int
        Number of records to display
    sortby: str
        Key to sort data
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    df = pycoingecko_model.get_coins(top=top, category=category, sortby=sortby)
    if not df.empty:
        df = df[
            [
                "symbol",
                "name",
                "total_volume",
                "market_cap",
                "market_cap_rank",
                "price_change_percentage_7d_in_currency",
                "price_change_percentage_24h_in_currency",
            ]
        ]
        df = df.set_axis(
            COINS_COLUMNS,
            axis=1,
            inplace=False,
        )
        for col in ["Volume [$]", "Market Cap"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: lambda_very_long_number_formatter(x))
        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "cgtop",
            df,
        )
    else:
        console.print("\nUnable to retrieve data from CoinGecko.\n")


@log_start_end(log=logger)
def display_gainers(
    period: str = "1h", top: int = 20, sortby: str = "market_cap_rank", export: str = ""
) -> None:
    """Shows Largest Gainers - coins which gain the most in given period. [Source: CoinGecko]

    Parameters
    ----------
    period: str
        Time period by which data is displayed. One from [1h, 24h, 7d, 14d, 30d, 60d, 1y]
    top: int
        Number of records to display
    sortby: str
        Key to sort data. The table can be sorted by every of its columns. Refer to
        API documentation (see /coins/markets in https://www.coingecko.com/en/api/documentation)
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = pycoingecko_model.get_gainers_or_losers(
        top=top, period=period, typ="gainers", sortby=sortby
    )
    if not df.empty:
        if sortby in COINS_COLUMNS:
            df = df[
                (df["total_volume"].notna()) & (df["market_cap"].notna())
            ].sort_values(by=sortby, ascending=True)
        for col in ["total_volume", "market_cap"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: lambda_very_long_number_formatter(x))
        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "gainers",
            df,
        )
    else:
        console.print("\nUnable to retrieve data from CoinGecko.\n")


@log_start_end(log=logger)
def display_losers(
    period: str = "1h", top: int = 20, export: str = "", sortby: str = "Market Cap Rank"
) -> None:
    """Shows Largest Losers - coins which lost the most in given period of time. [Source: CoinGecko]

    Parameters
    ----------
    period: str
        Time period by which data is displayed. One from [1h, 24h, 7d, 14d, 30d, 60d, 1y]
    top: int
        Number of records to display
    sortby: str
        Key to sort data. The table can be sorted by every of its columns. Refer to
        API documentation (see /coins/markets in https://www.coingecko.com/en/api/documentation)
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = pycoingecko_model.get_gainers_or_losers(
        top=top, period=period, typ="losers", sortby=sortby
    )
    if not df.empty:
        for col in ["Volume [$]", "Market Cap"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: lambda_very_long_number_formatter(x))
        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "cglosers",
            df,
        )
    else:
        console.print("\nUnable to retrieve data from CoinGecko.\n")


@log_start_end(log=logger)
def display_trending(export: str = "") -> None:
    """Display trending coins [Source: CoinGecko]

    Parameters
    ----------
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = pycoingecko_model.get_trending_coins()
    if not df.empty:
        print_rich_table(
            df,
            headers=list(df.columns),
            floatfmt=".4f",
            show_index=False,
            title="Trending coins on CoinGecko",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "cgtrending",
            df,
        )
    else:
        console.print("\nUnable to retrieve data from CoinGecko.\n")
