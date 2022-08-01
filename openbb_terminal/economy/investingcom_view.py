""" Investing.com View """
__docformat__ = "numpy"

import logging
import os
from typing import Optional, List

import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.config_terminal import theme
from openbb_terminal.decorators import log_start_end
from openbb_terminal.economy import investingcom_model
from openbb_terminal.helper_funcs import (
    export_data,
    plot_autoscale,
    print_rich_table,
)
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)

register_matplotlib_converters()

tenors_dict = {
    "1M": 1 / 12,
    "3M": 0.25,
    "6M": 0.5,
    "9M": 0.75,
    "1Y": 1,
    "2Y": 2,
    "3Y": 3,
    "4Y": 4,
    "5Y": 5,
    "6Y": 6,
    "7Y": 7,
    "8Y": 8,
    "9Y": 9,
    "10Y": 10,
    "15Y": 15,
    "20Y": 20,
    "25Y": 25,
    "30Y": 30,
    "50Y": 50,
}


@log_start_end(log=logger)
def display_yieldcurve(
    country: str,
    external_axes: Optional[List[plt.Axes]] = None,
    raw: bool = False,
    export: str = "",
):
    """Display yield curve. [Source: Investing.com]

    Parameters
    ----------
    country: str
        Country to display
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = investingcom_model.get_yieldcurve(country)
    if df is not None:
        df = df.replace(float("NaN"), "")

        if df.empty:
            console.print(
                f"[red]Yield data not found for \
                          {country.title()}[/red].\n"
            )
            return
        if external_axes is None:
            _, ax = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)

        else:
            if len(external_axes) != 1:
                logger.error("Expected list of 3 axis items")
                console.print("[red]Expected list of 3 axis items.\n[/red]")
                return
            (ax,) = external_axes

        tenors = []
        for i, row in df.iterrows():
            t = row["Tenor"][-3:].strip()
            df.at[i, "Tenor"] = t
            if t[-1] == "M":
                tenors.append(int(t[:-1]) / 12)
            elif t[-1] == "Y":
                tenors.append(int(t[:-1]))

        ax.plot(tenors, df["Current"], "-o")
        ax.set_xlabel("Maturity")
        ax.set_ylabel("Rate (%)")
        theme.style_primary_axis(ax)
        if external_axes is None:
            ax.set_title(f"Yield Curve for {country.title()} ")
            theme.visualize_output()

        if raw:
            print_rich_table(
                df,
                headers=list(df.columns),
                show_index=False,
                title=f"{country.title()} Yield Curve",
                floatfmt=".3f",
            )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "ycrv",
            df,
        )


@log_start_end(log=logger)
def display_economic_calendar(
    countries: str,
    importances: str,
    categories: str,
    from_date: datetime.date,
    to_date: datetime.date,
    limit=10,
    export: str = "",
):
    """Display economic calendar. [Source: Investing.com]

    Parameters
    ----------
    countries: str
        Country selected from allowed list
    importances: str
        Importance selected from high, medium, low or all
    categories: str
        Event category. E.g. Employment, Inflation, among others
    from_date: datetime.date
        First date to get events if applicable
    to_date: datetime.date
        Last date to get events if applicable
    limit: int
        The maximum number of events to show, default is 10.
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    countries_list = []
    importances_list = []
    categories_list = []

    if countries:
        countries_list = [countries.lower()]
    if importances:
        importances_list = [importances.lower()]
    if categories:
        categories_list = [categories.title()]

    df, time_zone = investingcom_model.get_economic_calendar(
        countries_list, importances_list, categories_list, from_date, to_date
    )

    if time_zone is None:
        time_zone = "GMT"
        console.print("[red]Error on timezone, default was used.[/red]\n")

    if df.empty:
        logger.error("No data")
        console.print("[red]No data.[/red]\n")
    else:
        df.fillna(value="", inplace=True)

        print_rich_table(
            df[:limit],
            headers=list(df.columns),
            show_index=False,
            title=f"Economic Calendar ({time_zone})",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "ecocal",
            df,
        )
