"""Momentum View"""
__docformat__ = "numpy"

import logging
import os
from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from openbb_terminal.config_terminal import theme
from openbb_terminal.common.technical_analysis import momentum_model
from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    export_data,
    plot_autoscale,
    reindex_dates,
    is_valid_axes_count,
    print_rich_table,
)

logger = logging.getLogger(__name__)

register_matplotlib_converters()


@log_start_end(log=logger)
def display_cci(
    data: pd.DataFrame,
    window: int = 14,
    scalar: float = 0.0015,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display CCI Indicator

    Parameters
    ----------

    data : pd.DataFrame
        Dataframe of OHLC
    window : int
        Length of window
    scalar : float
        Scalar variable
    symbol : str
        Stock ticker
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None
    """
    df_ta = momentum_model.cci(
        data["High"], data["Low"], data["Adj Close"], window, scalar
    )
    plot_data = pd.merge(data, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    # This plot has 2 axes
    if external_axes is None:
        _, axes = plt.subplots(
            2, 1, figsize=plot_autoscale(), sharex=True, dpi=PLOT_DPI
        )
        (ax1, ax2) = axes
    elif is_valid_axes_count(external_axes, 2):
        (ax1, ax2) = external_axes
    else:
        return

    ax1.set_title(f"{symbol} CCI")
    ax1.plot(
        plot_data.index,
        plot_data["Adj Close"].values,
    )
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Share Price ($)")

    theme.style_primary_axis(
        ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(plot_data.index, plot_data[df_ta.columns[0]].values)
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax2.axhspan(100, ax2.get_ylim()[1], facecolor=theme.down_color, alpha=0.2)
    ax2.axhspan(ax2.get_ylim()[0], -100, facecolor=theme.up_color, alpha=0.2)

    theme.style_primary_axis(
        ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax3 = ax2.twinx()
    ax3.set_ylim(ax2.get_ylim())
    ax3.axhline(100, color=theme.down_color, ls="--")
    ax3.axhline(-100, color=theme.up_color, ls="--")

    theme.style_twin_axis(ax3)

    ax2.set_yticks([-100, 100])
    ax2.set_yticklabels(["OVERSOLD", "OVERBOUGHT"])

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "cci",
        df_ta,
    )


@log_start_end(log=logger)
def display_macd(
    series: pd.Series,
    n_fast: int = 12,
    n_slow: int = 26,
    n_signal: int = 9,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Plot MACD signal

    Parameters
    ----------
    series : pd.Series
        Values to input
    n_fast : int
        Fast period
    n_slow : int
        Slow period
    n_signal : int
        Signal period
    symbol : str
        Stock ticker
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None
    """
    df_ta = momentum_model.macd(series, n_fast, n_slow, n_signal)
    plot_data = pd.merge(series, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    # This plot has 2 axes
    if external_axes is None:
        _, axes = plt.subplots(
            2, 1, figsize=plot_autoscale(), sharex=True, dpi=PLOT_DPI
        )
        (ax1, ax2) = axes
    elif is_valid_axes_count(external_axes, 2):
        (ax1, ax2) = external_axes
    else:
        return

    ax1.set_title(f"{symbol} MACD")
    ax1.plot(plot_data.index, plot_data.iloc[:, 1].values)
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Share Price ($)")
    theme.style_primary_axis(
        ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(plot_data.index, plot_data.iloc[:, 2].values)
    ax2.plot(plot_data.index, plot_data.iloc[:, 4].values, color=theme.down_color)
    ax2.bar(
        plot_data.index,
        plot_data.iloc[:, 3].values,
        width=theme.volume_bar_width,
        color=theme.up_color,
    )
    ax2.legend(
        [
            f"MACD Line {plot_data.columns[2]}",
            f"Signal Line {plot_data.columns[4]}",
            f"Histogram {plot_data.columns[3]}",
        ]
    )
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    theme.style_primary_axis(
        ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "macd",
        df_ta,
    )


@log_start_end(log=logger)
def display_rsi(
    series: pd.Series,
    window: int = 14,
    scalar: float = 100.0,
    drift: int = 1,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display RSI Indicator

    Parameters
    ----------
    series : pd.Series
        Values to input
    window : int
        Length of window
    scalar : float
        Scalar variable
    drift : int
        Drift variable
    symbol : str
        Stock ticker
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None
    """
    df_ta = momentum_model.rsi(series, window, scalar, drift)

    # This plot has 2 axes
    if external_axes is None:
        _, axes = plt.subplots(
            2, 1, figsize=plot_autoscale(), sharex=True, dpi=PLOT_DPI
        )
        (ax1, ax2) = axes
    elif is_valid_axes_count(external_axes, 2):
        (ax1, ax2) = external_axes
    else:
        return

    plot_data = pd.merge(series, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    ax1.plot(plot_data.index, plot_data.iloc[:, 1].values)
    ax1.set_title(f"{symbol} RSI{window}")
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Share Price ($)")
    theme.style_primary_axis(
        ax=ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(plot_data.index, plot_data[df_ta.columns[0]].values)
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax2.axhspan(0, 30, facecolor=theme.up_color, alpha=0.2)
    ax2.axhspan(70, 100, facecolor=theme.down_color, alpha=0.2)
    ax2.set_ylim([0, 100])

    theme.style_primary_axis(
        ax=ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax3 = ax2.twinx()
    ax3.set_ylim(ax2.get_ylim())
    ax3.axhline(30, color=theme.up_color, ls="--")
    ax3.axhline(70, color=theme.down_color, ls="--")
    ax2.set_yticks([30, 70])
    ax2.set_yticklabels(["OVERSOLD", "OVERBOUGHT"])

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "rsi",
        df_ta,
    )


@log_start_end(log=logger)
def display_stoch(
    data: pd.DataFrame,
    fastkperiod: int = 14,
    slowdperiod: int = 3,
    slowkperiod: int = 3,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
) -> None:
    """Plot stochastic oscillator signal

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe of OHLC prices
    fastkperiod : int
        Fast k period
    slowdperiod : int
        Slow d period
    slowkperiod : int
        Slow k period
    symbol : str
        Stock ticker symbol
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (3 axes are expected in the list), by default None
    """
    df_ta = momentum_model.stoch(
        data["High"],
        data["Low"],
        data["Adj Close"],
        fastkperiod,
        slowdperiod,
        slowkperiod,
    )
    # This plot has 3 axes
    if not external_axes:
        _, axes = plt.subplots(
            2, 1, sharex=True, figsize=plot_autoscale(), dpi=PLOT_DPI
        )
        ax1, ax2 = axes
        ax3 = ax2.twinx()
    elif is_valid_axes_count(external_axes, 3):
        (ax1, ax2, ax3) = external_axes
    else:
        return

    plot_data = pd.merge(data, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    ax1.plot(plot_data.index, plot_data["Adj Close"].values)

    ax1.set_title(f"Stochastic Relative Strength Index (STOCH RSI) on {symbol}")
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Share Price ($)")
    theme.style_primary_axis(
        ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(plot_data.index, plot_data[df_ta.columns[0]].values)
    ax2.plot(plot_data.index, plot_data[df_ta.columns[1]].values, ls="--")
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    theme.style_primary_axis(
        ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax3.set_ylim(ax2.get_ylim())
    ax3.axhspan(80, 100, facecolor=theme.down_color, alpha=0.2)
    ax3.axhspan(0, 20, facecolor=theme.up_color, alpha=0.2)
    ax3.axhline(80, color=theme.down_color, ls="--")
    ax3.axhline(20, color=theme.up_color, ls="--")
    theme.style_twin_axis(ax3)

    ax2.set_yticks([20, 80])
    ax2.set_yticklabels(["OVERSOLD", "OVERBOUGHT"])
    ax2.legend([f"%K {df_ta.columns[0]}", f"%D {df_ta.columns[1]}"])

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "stoch",
        df_ta,
    )


@log_start_end(log=logger)
def display_fisher(
    data: pd.DataFrame,
    window: int = 14,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display Fisher Indicator

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe of OHLC prices
    window : int
        Length of window
    symbol : str
        Ticker string
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (3 axes are expected in the list), by default None
    """
    df_ta = momentum_model.fisher(data["High"], data["Low"], window)
    plot_data = pd.merge(data, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    # This plot has 3 axes
    if not external_axes:
        _, axes = plt.subplots(
            2, 1, sharex=True, figsize=plot_autoscale(), dpi=PLOT_DPI
        )
        ax1, ax2 = axes
        ax3 = ax2.twinx()
    elif is_valid_axes_count(external_axes, 3):
        (ax1, ax2, ax3) = external_axes
    else:
        return

    ax1.set_title(f"{symbol} Fisher Transform")
    ax1.plot(plot_data.index, plot_data["Adj Close"].values)
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Price")
    theme.style_primary_axis(
        ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(
        plot_data.index,
        plot_data[df_ta.columns[0]].values,
        label="Fisher",
    )
    ax2.plot(
        plot_data.index,
        plot_data[df_ta.columns[1]].values,
        label="Signal",
    )
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    theme.style_primary_axis(
        ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax3.set_ylim(ax2.get_ylim())
    ax3.axhspan(2, ax2.get_ylim()[1], facecolor=theme.down_color, alpha=0.2)
    ax3.axhspan(ax2.get_ylim()[0], -2, facecolor=theme.up_color, alpha=0.2)
    ax3.axhline(2, color=theme.down_color, ls="--")
    ax3.axhline(-2, color=theme.up_color, ls="--")
    theme.style_twin_axis(ax3)

    ax2.set_yticks([-2, 0, 2])
    ax2.set_yticklabels(["-2 STDEV", "0", "+2 STDEV"])
    ax2.legend()

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "fisher",
        df_ta,
    )


@log_start_end(log=logger)
def display_cg(
    series: pd.Series,
    window: int = 14,
    symbol: str = "",
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display center of gravity Indicator

    Parameters
    ----------
    series : pd.Series
        Series of values
    window : int
        Length of window
    symbol : str
        Stock ticker
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None
    """
    df_ta = momentum_model.cg(series, window)
    plot_data = pd.merge(series, df_ta, how="outer", left_index=True, right_index=True)
    plot_data = reindex_dates(plot_data)

    # This plot has 2 axes
    if external_axes is None:
        _, axes = plt.subplots(
            2, 1, figsize=plot_autoscale(), sharex=True, dpi=PLOT_DPI
        )
        (ax1, ax2) = axes
    elif is_valid_axes_count(external_axes, 2):
        (ax1, ax2) = external_axes
    else:
        return

    ax1.set_title(f"{symbol} Centre of Gravity")
    ax1.plot(plot_data.index, plot_data[series.name].values)
    ax1.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax1.set_ylabel("Share Price ($)")
    theme.style_primary_axis(
        ax1,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    ax2.plot(plot_data.index, plot_data[df_ta.columns[0]].values, label="CG")
    # shift cg 1 bar forward for signal
    signal = np.roll(plot_data[df_ta.columns[0]].values, 1)
    ax2.plot(plot_data.index, signal, label="Signal")
    ax2.set_xlim(plot_data.index[0], plot_data.index[-1])
    ax2.legend()
    theme.style_primary_axis(
        ax2,
        data_index=plot_data.index.to_list(),
        tick_labels=plot_data["date"].to_list(),
    )

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "cg",
        df_ta,
    )


@log_start_end(log=logger)
def display_clenow_momentum(
    series: pd.Series,
    window: int = 90,
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display clenow momentum

    Parameters
    ----------
    series : pd.Series
        Series of values
    window : int
        Length of window
    export : str
        Format to export data
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None

    Returns
    -------

    """
    r2, coef, fit_data = momentum_model.clenow_momentum(series, window)

    df = pd.DataFrame.from_dict(
        {
            "R^2": f"{r2:.5f}",
            "Fit Coef": f"{coef:.5f}",
            "Factor": f"{coef * r2:.5f}",
        },
        orient="index",
    )
    print_rich_table(
        df,
        show_index=True,
        headers=[""],
        title="Clenow Exponential Regression Factor",
        show_header=False,
    )

    # This plot has 2 axes
    if external_axes is None:
        _, ax1 = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

    elif is_valid_axes_count(external_axes, 1):
        ax1 = external_axes
    else:
        return

    ax1.plot(series.index, np.log(series.values))
    ax1.plot(series.index[-window:], fit_data, linewidth=2)

    ax1.set_title("Clenow Momentum Exponential Regression")
    ax1.set_xlim(series.index[0], series.index[-1])
    ax1.set_ylabel("Log Price")
    theme.style_primary_axis(
        ax1,
    )
    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "clenow",
    )
