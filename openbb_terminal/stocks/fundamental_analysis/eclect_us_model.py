"""Eclect.us model"""
__docformat__ = "numpy"

import logging
from collections import OrderedDict

import requests

from openbb_terminal.decorators import log_start_end

# pylint: disable=R1718


logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_filings_analysis(symbol: str) -> str:
    """Save time reading SEC filings with the help of machine learning. [Source: https://eclect.us]

    Parameters
    ----------
    symbol: str
        Ticker symbol to see analysis of filings

    Returns
    -------
    str
        Analysis of filings text
    """

    response = requests.get(f"https://api.eclect.us/symbol/{symbol.lower()}?page=1")

    if response.status_code != 200:
        filings_analysis = ""
    else:
        response_dict = response.json()

        rf_highlights = "[bold]\n\tRISK FACTORS:[/bold]\n"
        rf_highlights_list = [
            sentence["sentence"] for sentence in response_dict[0]["rf_highlights"]
        ]
        rf_highlights_list = list(OrderedDict.fromkeys(rf_highlights_list))
        rf_highlights_txt = "\n\n".join(rf_highlights_list)

        daa_highlights = "[bold]\n\tDISCUSSION AND ANALYSIS:[/bold]\n"
        daa_highlights_list = [
            sentence["sentence"] for sentence in response_dict[0]["daa_highlights"]
        ]
        daa_highlights_list = list(OrderedDict.fromkeys(daa_highlights_list))
        daa_highlights += "\n\n".join(daa_highlights_list)

        if rf_highlights_txt:
            filings_analysis = rf_highlights + rf_highlights_txt + "\n" + daa_highlights
        else:
            filings_analysis = daa_highlights

    return filings_analysis
