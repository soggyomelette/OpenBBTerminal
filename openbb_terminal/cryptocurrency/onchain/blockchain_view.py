"""Blockchain View"""
__docformat__ = "numpy"

import logging
import os
from datetime import datetime
from typing import List, Optional

import matplotlib.pyplot as plt
from matplotlib import ticker

from openbb_terminal.config_terminal import theme
from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.cryptocurrency.onchain import blockchain_model
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    export_data,
    lambda_long_number_format,
    plot_autoscale,
    is_valid_axes_count,
)

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def display_btc_circulating_supply(
    since: int = int(datetime(2010, 1, 1).timestamp()),
    until: int = int(datetime.now().timestamp()),
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
) -> None:
    """Returns BTC circulating supply [Source: https://api.blockchain.info/]

    Parameters
    ----------
    since : int
        Initial date timestamp (e.g., 1_609_459_200)
    until : int
        End date timestamp (e.g., 1_641_588_030)
    export : str
        Export dataframe data to csv,json,xlsx file
    external_axes : Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """

    df = blockchain_model.get_btc_circulating_supply()
    df = df[
        (df["x"] > datetime.fromtimestamp(since))
        & (df["x"] < datetime.fromtimestamp(until))
    ]

    # This plot has 1 axis
    if not external_axes:
        _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    elif is_valid_axes_count(external_axes, 1):
        (ax,) = external_axes
    else:
        return

    ax.plot(df["x"], df["y"])
    ax.set_ylabel("BTC")
    ax.set_title("BTC Circulating Supply")
    ax.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, _: lambda_long_number_format(x))
    )

    if not external_axes:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "btccp",
        df,
    )


@log_start_end(log=logger)
def display_btc_confirmed_transactions(
    since: int = int(datetime(2010, 1, 1).timestamp()),
    until: int = int(datetime.now().timestamp()),
    export: str = "",
    external_axes: Optional[List[plt.Axes]] = None,
) -> None:
    """Returns BTC confirmed transactions [Source: https://api.blockchain.info/]

    Parameters
    ----------
    since : int
        Initial date timestamp (e.g., 1_609_459_200)
    until : int
        End date timestamp (e.g., 1_641_588_030)
    export : str
        Export dataframe data to csv,json,xlsx file
    external_axes : Optional[List[plt.Axes]], optional
        External axes (1 axis is expected in the list), by default None
    """

    df = blockchain_model.get_btc_confirmed_transactions()
    df = df[
        (df["x"] > datetime.fromtimestamp(since))
        & (df["x"] < datetime.fromtimestamp(until))
    ]

    # This plot has 1 axis
    if not external_axes:
        _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
    elif is_valid_axes_count(external_axes, 1):
        (ax,) = external_axes
    else:
        return

    ax.plot(df["x"], df["y"], lw=0.8)
    ax.set_ylabel("Transactions")
    ax.set_title("BTC Confirmed Transactions")
    ax.get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda x, _: lambda_long_number_format(x))
    )

    theme.style_primary_axis(ax)

    if not external_axes:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "btcct",
        df,
    )
