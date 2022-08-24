"""Binance model"""
__docformat__ = "numpy"

import argparse
import logging
from collections import defaultdict
from typing import List, Tuple, Union

import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException

import openbb_terminal.config_terminal as cfg
from openbb_terminal.decorators import log_start_end

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def _get_trading_pairs() -> List[dict]:
    """Helper method that return all trading pairs on binance. Methods ause this data for input for e.g
    building dataframe with all coins, or to build dict of all trading pairs. [Source: Binance]

    Returns
    -------
    List[dict]
        list of dictionaries in format:
        [
            {'symbol': 'ETHBTC', 'status': 'TRADING', 'baseAsset': 'ETH', 'baseAssetPrecision': 8,
            'quoteAsset': 'BTC', 'quotePrecision': 8, 'quoteAssetPrecision': 8,
            'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8,
            'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'],
            'icebergAllowed': True,
            'ocoAllowed': True,
            'quoteOrderQtyMarketAllowed': True,
            'isSpotTradingAllowed': True,
            'isMarginTradingAllowed': True,
            'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.00000100',
            'maxPrice': '922327.00000000', 'tickSize': '0.00000100'},
            {'filterType': 'PERCENT_PRICE', 'multiplierUp': '5', 'multiplierDown': '0.2', 'avgPriceMins': 5},
            {'filterType': 'LOT_SIZE', 'minQty': '0.00100000', 'maxQty': '100000.00000000', 'stepSize': '0.00100000'},
            {'filterType': 'MIN_NOTIONAL', 'minNotional': '0.00010000', 'applyToMarket': True, 'avgPriceMins': 5},
            {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty': '0.00000000',
            'maxQty': '930.49505347', 'stepSize': '0.00000000'}, {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200},
            {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}], 'permissions': ['SPOT', 'MARGIN']},
        ...
        ]
    """
    client = Client(cfg.API_BINANCE_KEY, cfg.API_BINANCE_SECRET)
    ex_info = client.get_exchange_info()["symbols"]
    trading_pairs = [p for p in ex_info if p["status"] == "TRADING"]
    return trading_pairs


@log_start_end(log=logger)
def get_all_binance_trading_pairs() -> pd.DataFrame:
    """Returns all available pairs on Binance in DataFrame format. DataFrame has 3 columns symbol, baseAsset, quoteAsset
    example row: ETHBTC | ETH | BTC
    [Source: Binance]


    Returns
    -------
    pd.DataFrame
        All available pairs on Binance
        Columns: symbol, baseAsset, quoteAsset

    """
    trading_pairs = _get_trading_pairs()
    return pd.DataFrame(trading_pairs)[["symbol", "baseAsset", "quoteAsset"]]


@log_start_end(log=logger)
def get_binance_available_quotes_for_each_coin() -> dict:
    """Helper methods that for every coin available on Binance add all quote assets. [Source: Binance]

    Returns
    -------
    dict:
        All quote assets for given coin
        {'ETH' : ['BTC', 'USDT' ...], 'UNI' : ['ETH', 'BTC','BUSD', ...]

    """
    trading_pairs = _get_trading_pairs()
    results = defaultdict(list)
    for pair in trading_pairs:
        results[pair["baseAsset"]].append(pair["quoteAsset"])
    return results


@log_start_end(log=logger)
def check_valid_binance_str(symbol: str) -> str:
    """Check if symbol is in defined binance. [Source: Binance]"""
    client = Client(cfg.API_BINANCE_KEY, cfg.API_BINANCE_SECRET)
    try:
        client.get_avg_price(symbol=symbol.upper())
        return symbol.upper()
    except BinanceAPIException as e:
        logger.exception("%s is not a valid binance symbol", str(symbol))
        raise argparse.ArgumentTypeError(
            f"{symbol} is not a valid binance symbol"
        ) from e


@log_start_end(log=logger)
def show_available_pairs_for_given_symbol(
    symbol: str = "ETH",
) -> Tuple[Union[str, None], list]:
    """Return all available quoted assets for given symbol. [Source: Binance]

    Parameters
    ----------
    symbol:
        Uppercase symbol of coin e.g BTC, ETH, UNI, LUNA, DOT ...

    Returns
    -------
    str:
        Coin symbol
    list:
        Quoted assets for given symbol: ["BTC", "USDT" , "BUSD"]
    """

    symbol_upper = symbol.upper()
    pairs = get_binance_available_quotes_for_each_coin()
    for k, v in pairs.items():
        if k == symbol_upper:
            return k, v
    return None, []
