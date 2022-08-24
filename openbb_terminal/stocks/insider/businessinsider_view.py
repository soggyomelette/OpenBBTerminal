""" Business Insider View """
__docformat__ = "numpy"

from datetime import datetime, timedelta
import logging
import os
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from openbb_terminal.config_terminal import theme
from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    export_data,
    get_next_stock_market_days,
    print_rich_table,
    plot_autoscale,
    is_valid_axes_count,
)
from openbb_terminal.rich_config import console
from openbb_terminal.stocks.insider import businessinsider_model

logger = logging.getLogger(__name__)

register_matplotlib_converters()


@log_start_end(log=logger)
def insider_activity(
    data: pd.DataFrame,
    symbol: str,
    start_date: str = (datetime.now() - timedelta(days=1100)).strftime("%Y-%m-%d"),
    interval: str = "1440min",
    limit: int = 10,
    raw: bool = False,
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display insider activity. [Source: Business Insider]

    Parameters
    ----------
    data: pd.DataFrame
        Stock dataframe
    symbol: str
        Due diligence ticker symbol
    start_date: str
        Start date of the stock data
    interval: str
        Stock data interval
    limit: int
        Number of latest days of inside activity
    raw: bool
        Print to console
    export: str
        Export dataframe data to csv,json,xlsx file
    external_axes: Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """
    df_ins = businessinsider_model.get_insider_activity(symbol)

    if df_ins.empty:
        logger.warning("The insider activity on the ticker does not exist")
        console.print("[red]The insider activity on the ticker does not exist.\n[/red]")
    else:

        if start_date:
            df_insider = df_ins[start_date:].copy()  # type: ignore
        else:
            df_insider = df_ins.copy()

        if raw:
            df_insider.index = pd.to_datetime(df_insider.index).date

            print_rich_table(
                df_insider.sort_index(ascending=False)
                .head(n=limit)
                .applymap(lambda x: x.replace(".00", "").replace(",", "")),
                headers=list(df_insider.columns),
                show_index=True,
                title="Insider Activity",
            )
        else:
            # This plot has 1 axis
            if not external_axes:
                _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
            elif is_valid_axes_count(external_axes, 1):
                (ax,) = external_axes
            else:
                return

            if interval == "1440min":
                ax.plot(data.index, data["Adj Close"].values, lw=3)
            else:  # Intraday
                ax.plot(data.index, data["Close"].values, lw=3)

            ax.set_title(f"{symbol.upper()}'s Insider Trading Activity & Share Price")
            ax.set_ylabel("Share Price")

            df_insider["Trade"] = df_insider.apply(
                lambda row: (1, -1)[row.Type == "Sell"]
                * float(row["Shares Traded"].replace(",", "")),
                axis=1,
            )
            ax.set_xlim(right=data.index[-1])
            min_price, max_price = ax.get_ylim()

            price_range = max_price - min_price
            shares_range = (
                df_insider[df_insider["Type"] == "Buy"]
                .groupby(by=["Date"])
                .sum()["Trade"]
                .max()
                - df_insider[df_insider["Type"] == "Sell"]
                .groupby(by=["Date"])
                .sum()["Trade"]
                .min()
            )
            n_proportion = price_range / shares_range

            for ind in (
                df_insider[df_insider["Type"] == "Sell"]
                .groupby(by=["Date"])
                .sum()
                .index
            ):
                if ind in data.index:
                    ind_dt = ind
                else:
                    ind_dt = get_next_stock_market_days(ind, 1)[0]

                n_stock_price = 0
                if interval == "1440min":
                    n_stock_price = data["Adj Close"][ind_dt]
                else:
                    n_stock_price = data["Close"][ind_dt]

                bar_1 = ax.vlines(
                    x=ind_dt,
                    ymin=n_stock_price
                    + n_proportion
                    * float(
                        df_insider[df_insider["Type"] == "Sell"]
                        .groupby(by=["Date"])
                        .sum()["Trade"][ind]
                    ),
                    ymax=n_stock_price,
                    colors=theme.down_color,
                    ls="-",
                    lw=5,
                )

            for ind in (
                df_insider[df_insider["Type"] == "Buy"].groupby(by=["Date"]).sum().index
            ):
                if ind in data.index:
                    ind_dt = ind
                else:
                    ind_dt = get_next_stock_market_days(ind, 1)[0]

                n_stock_price = 0
                if interval == "1440min":
                    n_stock_price = data["Adj Close"][ind_dt]
                else:
                    n_stock_price = data["Close"][ind_dt]

                bar_2 = ax.vlines(
                    x=ind_dt,
                    ymin=n_stock_price,
                    ymax=n_stock_price
                    + n_proportion
                    * float(
                        df_insider[df_insider["Type"] == "Buy"]
                        .groupby(by=["Date"])
                        .sum()["Trade"][ind]
                    ),
                    colors=theme.up_color,
                    ls="-",
                    lw=5,
                )

            ax.legend(
                handles=[bar_1, bar_2],
                labels=["Insider Selling", "Insider Buying"],
                loc="best",
            )
            theme.style_primary_axis(ax)

            if not external_axes:
                theme.visualize_output()

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "act",
            df_insider,
        )
