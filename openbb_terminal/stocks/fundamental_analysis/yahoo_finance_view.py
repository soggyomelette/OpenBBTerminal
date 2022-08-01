""" Yahoo Finance View """
__docformat__ = "numpy"

import logging
import os
import webbrowser
from datetime import datetime, timedelta
from typing import List, Optional
from fractions import Fraction

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from openbb_terminal.config_terminal import theme
from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    export_data,
    plot_autoscale,
    print_rich_table,
    is_valid_axes_count,
    lambda_long_number_format,
)
from openbb_terminal.rich_config import console
from openbb_terminal.stocks.fundamental_analysis import yahoo_finance_model

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def open_headquarters_map(ticker: str):
    """Headquarters location of the company
    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    webbrowser.open(yahoo_finance_model.get_hq(ticker))
    console.print("")


@log_start_end(log=logger)
def open_web(ticker: str):
    """Website of the company
    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    webbrowser.open(yahoo_finance_model.get_website(ticker))
    console.print("")


@log_start_end(log=logger)
def display_info(ticker: str, export: str = ""):
    """Yahoo Finance ticker info
    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    export: str
        Format to export data
    """
    summary = ""
    df_info = yahoo_finance_model.get_info(ticker)
    if "Long business summary" in df_info.index:
        summary = df_info.loc["Long business summary"].values[0]
        df_info = df_info.drop(index=["Long business summary"])

    if not df_info.empty:
        print_rich_table(
            df_info,
            headers=list(df_info.columns),
            show_index=True,
            title=f"{ticker.upper()} Info",
        )
    else:
        logger.error("Invalid data")
        console.print("[red]Invalid data[/red]\n")
        return

    if summary:
        console.print("Business Summary:")
        console.print(summary)

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "info", df_info)


@log_start_end(log=logger)
def display_shareholders(ticker: str, export: str = ""):
    """Yahoo Finance ticker shareholders
    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    export: str
        Format to export data
    """
    (
        df_major_holders,
        df_institutional_shareholders,
        df_mutualfund_shareholders,
    ) = yahoo_finance_model.get_shareholders(ticker)
    df_major_holders.columns = ["", ""]
    dfs = [df_major_holders, df_institutional_shareholders, df_mutualfund_shareholders]
    titles = ["Major Holders", "Institutional Holders", "Mutual Fund Holders"]
    console.print()

    for df, title in zip(dfs, titles):
        if "Date Reported" in df.columns:
            df["Date Reported"] = df["Date Reported"].apply(
                lambda x: x.strftime("%Y-%m-%d")
            )
        print_rich_table(
            df,
            headers=list(df.columns),
            show_index=False,
            title=f"{ticker.upper()} {title}",
        )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "major_holders",
        df_major_holders,
    )
    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "institutional_holders",
        df_institutional_shareholders,
    )
    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "mutualfunds_holders",
        df_major_holders,
    )


@log_start_end(log=logger)
def display_sustainability(ticker: str, export: str = ""):
    """Yahoo Finance ticker sustainability

    Parameters
    ----------
    other_args : List[str]
        argparse other args
    ticker : str
        Fundamental analysis ticker symbol
    export: str
        Format to export data
    """

    df_sustainability = yahoo_finance_model.get_sustainability(ticker)

    if df_sustainability.empty:
        console.print("No sustainability data found.", "\n")
        return

    if not df_sustainability.empty:
        print_rich_table(
            df_sustainability,
            headers=list(df_sustainability),
            title=f"{ticker.upper()} Sustainability",
            show_index=True,
        )

    else:
        logger.error("Invalid data")
        console.print("[red]Invalid data[/red]\n")

    export_data(
        export, os.path.dirname(os.path.abspath(__file__)), "sust", df_sustainability
    )


@log_start_end(log=logger)
def display_calendar_earnings(ticker: str, export: str = ""):
    """Yahoo Finance ticker calendar earnings

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    export: str
        Format to export data
    """
    df_calendar = yahoo_finance_model.get_calendar_earnings(ticker).T
    if df_calendar.empty:
        console.print("No calendar events found.\n")
        return
    print_rich_table(
        df_calendar,
        show_index=False,
        headers=list(df_calendar.columns),
        title=f"{ticker.upper()} Calendar Earnings",
    )

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "cal", df_calendar)


@log_start_end(log=logger)
def display_dividends(
    ticker: str,
    limit: int = 12,
    plot: bool = False,
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display historical dividends
    Parameters
    ----------
    ticker: str
        Stock ticker
    limit: int
        Number to show
    plot: bool
        Plots historical data
    export: str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """
    div_history = yahoo_finance_model.get_dividends(ticker)
    if div_history.empty:
        console.print("No dividends found.\n")
        return
    div_history["Dif"] = div_history.diff()
    div_history = div_history[::-1]
    if plot:

        # This plot has 1 axis
        if not external_axes:
            _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
        elif is_valid_axes_count(external_axes, 1):
            (ax,) = external_axes
        else:
            return

        ax.plot(
            div_history.index,
            div_history["Dividends"],
            ls="-",
            linewidth=0.75,
            marker=".",
            markersize=4,
            mfc=theme.down_color,
            mec=theme.down_color,
            alpha=1,
            label="Dividends Payout",
        )
        ax.set_ylabel("Amount ($)")
        ax.set_title(f"Dividend History for {ticker}")
        ax.set_xlim(div_history.index[-1], div_history.index[0])
        ax.legend()
        theme.style_primary_axis(ax)

        if not external_axes:
            theme.visualize_output()

    else:
        div_history.index = pd.to_datetime(div_history.index, format="%Y%m%d").strftime(
            "%Y-%m-%d"
        )
        print_rich_table(
            div_history.head(limit),
            headers=["Amount Paid ($)", "Change"],
            title=f"{ticker.upper()} Historical Dividends",
            show_index=True,
        )

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "divs", div_history)


@log_start_end(log=logger)
def display_splits(
    ticker: str,
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display splits and reverse splits events. [Source: Yahoo Finance]

    Parameters
    ----------
    ticker: str
        Stock ticker
    export: str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """
    df_splits = yahoo_finance_model.get_splits(ticker)
    if df_splits.empty:
        console.print("No splits or reverse splits events found.\n")
        return

    # This plot has 1 axis
    if not external_axes:
        _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    elif is_valid_axes_count(external_axes, 1):
        (ax,) = external_axes
    else:
        return

    # Get all stock data since IPO
    df_data = yf.download(ticker, progress=False, threads=False)
    if df_data.empty:
        console.print("No stock price data available.\n")
        return

    ax.plot(df_data.index, df_data["Adj Close"], color="#FCED00")
    ax.set_ylabel("Price")
    ax.set_title(f"{ticker} splits and reverse splits events")

    ax.plot(df_data.index, df_data["Adj Close"].values)
    for index, row in df_splits.iterrows():
        val = row.values[0]
        frac = Fraction(val).limit_denominator(1000000)
        if val > 1:
            ax.axvline(index, color=theme.up_color)
            ax.annotate(
                f"{frac.numerator}:{frac.denominator}",
                (mdates.date2num(index), df_data["Adj Close"].max()),
                xytext=(10, 0),
                textcoords="offset points",
                color=theme.up_color,
            )
        else:
            ax.axvline(index, color=theme.down_color)
            ax.annotate(
                f"{frac.numerator}:{frac.denominator}",
                (mdates.date2num(index), df_data["Adj Close"].max()),
                xytext=(10, 0),
                textcoords="offset points",
                color=theme.down_color,
            )

    theme.style_primary_axis(ax)

    if not external_axes:
        theme.visualize_output()

    print_rich_table(
        df_splits,
        title=f"{ticker.upper()} splits and reverse splits",
        show_index=True,
    )

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "splits", df_splits)


@log_start_end(log=logger)
def display_mktcap(
    ticker: str,
    start: datetime = (datetime.now() - timedelta(days=3 * 366)),
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display market cap over time. [Source: Yahoo Finance]

    Parameters
    ----------
    ticker: str
        Stock ticker
    start: datetime
        Start date to display market cap
    export: str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """
    df_mktcap, currency = yahoo_finance_model.get_mktcap(ticker, start)
    if df_mktcap.empty:
        console.print("No Market Cap data available.\n")
        return

    # This plot has 1 axis
    if not external_axes:
        _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    elif is_valid_axes_count(external_axes, 1):
        (ax,) = external_axes
    else:
        return

    ax.stackplot(df_mktcap.index, df_mktcap.values / 1e9, colors=[theme.up_color])
    ax.set_ylabel(f"Market Cap in Billion ({currency})")
    ax.set_title(f"{ticker} Market Cap")
    ax.set_xlim(df_mktcap.index[0], df_mktcap.index[-1])
    theme.style_primary_axis(ax)

    if not external_axes:
        theme.visualize_output()

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "mktcap", df_mktcap)


@log_start_end(log=logger)
def display_fundamentals(
    ticker: str,
    financial: str,
    limit: int = 120,
    ratios: bool = False,
    plot: list = None,
    export: str = "",
):
    """Display tickers balance sheet, income statement or cash-flow

    Parameters
    ----------
    ticker: str
        Stock ticker
    financial:str
        Either balance or financials for income or cash-flow
    limit : int
    ratios: bool
        Shows percentage change
    plot: list
        List of row labels to plot
    export: str
        Format to export data
    """
    if financial == "balance-sheet":
        fundamentals = yahoo_finance_model.get_financials(ticker, financial, ratios)
        title_str = "Balance Sheet"
    elif financial == "financials":
        fundamentals = yahoo_finance_model.get_financials(ticker, financial, ratios)
        title_str = "Income Statement"
    elif financial == "cash-flow":
        fundamentals = yahoo_finance_model.get_financials(ticker, financial, ratios)
        title_str = "Cash Flow Statement"

    if fundamentals.empty:
        # The empty data frame error handling done in model
        return
    if plot:
        rows_plot = len(plot)
        fundamentals_plot_data = fundamentals.transpose().fillna(-1)
        fundamentals_plot_data.columns = fundamentals_plot_data.columns.str.lower()
        fundamentals_plot_data = fundamentals_plot_data.replace(",", "", regex=True)
        fundamentals_plot_data = fundamentals_plot_data.replace("-", "-1")
        fundamentals_plot_data = fundamentals_plot_data.astype(float)

        if not ratios:
            maximum_value = fundamentals_plot_data.max().max()
            if maximum_value > 1_000_000_000_000:
                df_rounded = fundamentals_plot_data / 1_000_000_000_000
                denomination = " in Trillions"
            elif maximum_value > 1_000_000_000:
                df_rounded = fundamentals_plot_data / 1_000_000_000
                denomination = " in Billions"
            elif maximum_value > 1_000_000:
                df_rounded = fundamentals_plot_data / 1_000_000
                denomination = " in Millions"
            elif maximum_value > 1_000:
                df_rounded = fundamentals_plot_data / 1_000
                denomination = " in Thousands"
            else:
                df_rounded = fundamentals_plot_data
                denomination = ""
        else:
            df_rounded = fundamentals_plot_data
            denomination = ""

        if rows_plot == 1:
            fig, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
            df_rounded[plot[0].replace("_", " ")].plot()
            title = (
                f"{plot[0].replace('_', ' ').lower()} QoQ Growth of {ticker.upper()}"
                if ratios
                else f"{plot[0].replace('_', ' ')} of {ticker.upper()} {denomination}"
            )
            plt.title(title)
            theme.style_primary_axis(ax)
            theme.visualize_output()
        else:
            fig, axes = plt.subplots(rows_plot)
            for i in range(rows_plot):
                axes[i].plot(df_rounded[plot[i].replace("_", " ")])
                axes[i].set_title(f"{plot[i].replace('_', ' ')} {denomination}")
            theme.style_primary_axis(axes[0])
            fig.autofmt_xdate()
    else:
        # Snake case to english
        fundamentals.index = fundamentals.index.to_series().apply(
            lambda x: x.replace("_", " ").title()
        )

        # Readable numbers
        fundamentals = fundamentals.applymap(lambda_long_number_format).fillna("-")
        print_rich_table(
            fundamentals.iloc[:, :limit].applymap(lambda x: "-" if x == "nan" else x),
            show_index=True,
            title=f"{ticker} {title_str}",
        )
    export_data(
        export, os.path.dirname(os.path.abspath(__file__)), financial, fundamentals
    )
