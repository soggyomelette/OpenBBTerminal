"""Finviz View"""
__docformat__ = "numpy"

import os
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots

from openbb_terminal.stocks.discovery import finviz_model
from openbb_terminal.rich_config import console
from openbb_terminal.helper_funcs import export_data


def display_heatmap(timeframe: str, export: str = ""):
    """Display heatmap from finviz

    Parameters
    ----------
    timeframe: str
        Timeframe for performance
    export: str
        Format to export data
    """
    console.print("")
    dfs = finviz_model.get_heatmap_data(timeframe)
    if dfs.empty:
        return
    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "heatmap",
        dfs,
    )
    color_bin = [-1, -0.02, -0.01, -0.00001, 0.00001, 0.01, 0.02, 1]
    dfs["colors"] = pd.cut(
        dfs["Change"],
        bins=color_bin,
        labels=[
            "rgb(246, 53, 56)",
            "rgb(191, 64, 69)",
            "rgb(139, 68, 78)",
            "grey",
            "rgb(53, 118, 78)",
            "rgb(47, 158, 79)",
            "rgb(48, 204, 90)",
        ],
    )
    path_tree = [px.Constant("SP 500"), "Sector", "Ticker"]
    fig = make_subplots(
        print_grid=False,
        vertical_spacing=0.02,
        horizontal_spacing=-0,
        specs=[[{"type": "domain"}]],
        rows=1,
        cols=1,
    )
    treemap = px.treemap(
        dfs,
        path=path_tree,
        values="value",
        custom_data=["Change"],
        color="colors",
        color_discrete_map={
            "(?)": "#262931",
            "grey": "grey",
            "rgb(246, 53, 56)": "rgb(246, 53, 56)",
            "rgb(191, 64, 69)": "rgb(191, 64, 69)",
            "rgb(139, 68, 78)": "rgb(139, 68, 78)",
            "rgb(53, 118, 78)": "rgb(53, 118, 78)",
            "rgb(47, 158, 79)": "rgb(47, 158, 79)",
            "rgb(48, 204, 90)": "rgb(48, 204, 90)",
        },
    )
    fig.add_trace(treemap["data"][0], row=1, col=1)

    fig.data[
        0
    ].texttemplate = (
        "<br> <br> <b>%{label}<br>    %{customdata[0]:.2f}% <br> <br> <br><br><b>"
    )
    fig.data[0].insidetextfont = dict(
        family="Arial Black",
        size=50,
        color="white",
    )

    fig.update_traces(
        textinfo="label+text+value",
        textposition="middle center",
        selector=dict(type="treemap"),
        marker_line_width=0.3,
        marker_pad_b=20,
        marker_pad_l=0,
        marker_pad_r=0,
        marker_pad_t=50,
        tiling_pad=2,
    )
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode=False,
        font=dict(
            family="Arial Black",
            size=20,
            color="white",
        ),
    )

    fig.show()
