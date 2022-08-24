"""Avanza Model"""
__docformat__ = "numpy"

# pylint: disable=E1101

import logging
import os
import requests

import pandas as pd

from openbb_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_data(name: str):
    """Gets the data from Avanza

    Parameters
    ----------
    name: str
        Full name of the fund
    """
    ava_fund = pd.read_csv(
        os.path.join("openbb_terminal", "mutual_funds", "avanza_fund_ID.csv"),
        index_col=0,
    )
    ava_fund.index = ava_fund.index.str.upper()
    fund_id = ava_fund.loc[name, "ID"]
    url = f"https://www.avanza.se/_api/fund-guide/guide/{fund_id}"
    response = requests.get(url)
    fund_data = response.json()
    return fund_data
