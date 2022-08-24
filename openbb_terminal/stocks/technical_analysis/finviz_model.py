"""Finviz model"""
__docformat__ = "numpy"

import logging

import requests
from finvizfinance.quote import finvizfinance
from finvizfinance.util import headers

from openbb_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_finviz_image(symbol: str) -> bytes:
    """Get finviz image for given ticker

    Parameters
    ----------
    symbol: str
        Ticker symbol

    Returns
    -------
    bytes
        Image in byte format
    """
    stock = finvizfinance(symbol)
    image_url = stock.ticker_charts(urlonly=True)

    r = requests.get(image_url, stream=True, headers=headers, timeout=5)
    r.raise_for_status()
    r.raw.decode_content = True
    return r.content
