"""Investpy Model"""
__docformat__ = "numpy"

import logging
from datetime import datetime, timedelta
from typing import Tuple

import investpy
import pandas as pd

from openbb_terminal.decorators import log_start_end
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def search_funds(by: str = "name", value: str = "") -> pd.DataFrame:
    """Search investpy for matching funds

    Parameters
    ----------
    by : str
        Field to match on.  Can be name, issuer, isin or symbol
    value : str
        String that will be searched for

    Returns
    -------
    pd.DataFrame
        Dataframe containing matches
    """
    try:
        return investpy.funds.search_funds(by=by, value=value)
    except RuntimeError as e:
        logger.exception(str(e))
        return pd.DataFrame()


@log_start_end(log=logger)
def get_overview(country: str = "united states", limit: int = 20) -> pd.DataFrame:
    """

    Parameters
    ----------
    country: str
        Country to get overview for
    limit: int
        Number of results to get

    Returns
    -------
    pd.DataFrame
        Dataframe containing overview
    """
    return investpy.funds.get_funds_overview(
        country=country, as_json=False, n_results=limit
    )


@log_start_end(log=logger)
def get_fund_symbol_from_name(name: str) -> Tuple[str, str]:
    """Get fund symbol from name through investpy

    Parameters
    ----------
    Name: str
        Name to get fund symbol of

    Returns
    -------
    str
        Name of Symbol matching provided name
    str
        Country in which matching symbol was found
    """
    name_search_results = investpy.search_funds(by="name", value=name)
    if name_search_results.empty:
        return "", ""
    symbol = name_search_results.loc[:, "symbol"][0]
    country = name_search_results.country.values[0]
    console.print(
        f"Name: [cyan][italic]{symbol.upper()}[/italic][/cyan] found for {name} in country: {country.title()}."
    )
    return symbol, country


@log_start_end(log=logger)
def get_fund_name_from_symbol(symbol: str) -> Tuple[str, str]:
    """Get fund name from symbol from investpy

    Parameters
    ----------
    symbol: str
        Symbol to get fund name of

    Returns
    -------
    str
        Name of fund matching provided symbol
    str
        Country matching symbol
    """
    symbol_search_results = investpy.search_funds(by="symbol", value=symbol)
    if symbol_search_results.empty:
        return "", ""
    name = symbol_search_results.loc[:, "name"][0]
    country = symbol_search_results.loc[:, "country"][0]
    console.print(
        f"Name: [cyan][italic]{name.title()}[/italic][/cyan] found for {symbol} in country: {country.title()}."
    )
    return name, country


@log_start_end(log=logger)
def get_fund_info(name: str, country: str = "united states") -> pd.DataFrame:
    """

    Parameters
    ----------
    name: str
        Name of fund (not symbol) to get information
    country: str
        Country of fund

    Returns
    -------
    pd.DataFrame
        Dataframe of fund information
    """
    return investpy.funds.get_fund_information(name, country).T


@log_start_end(log=logger)
def get_fund_historical(
    name: str,
    country: str = "united states",
    by_name: bool = False,
    start_date: datetime = (datetime.now() - timedelta(days=366)),
    end_date: datetime = datetime.now(),
) -> Tuple[pd.DataFrame, str, str, str]:
    """Get historical fund data

    Parameters
    ----------
    name: str
        Fund to get data for.  If using fund name, include `name=True`
    country: str
        Country of fund
    by_name : bool
        Flag to search by name instead of symbol
    start_date: datetime
        Start date of data in format YYYY-MM-DD
    end_date: datetime
        End date of data in format YYYY-MM-DD

    Returns
    -------
    pd.DataFrame:
        Dataframe of OHLC prices
    str:
        Fund name
    str:
        Fund symbol
    str:
        Country that matches search results
    """
    if by_name:
        fund_name = name
        try:
            fund_symbol, matching_country = get_fund_symbol_from_name(name)
        except RuntimeError as e:
            logger.exception(str(e))
            return pd.DataFrame(), name, "", country
    else:
        fund_symbol = name
        try:
            fund_name, matching_country = get_fund_name_from_symbol(name)
        except RuntimeError as e:
            logger.exception(str(e))
            return pd.DataFrame(), "", name, country

    # Note that dates for investpy need to be in the format dd/mm/yyyy
    from_date = start_date.strftime("%d/%m/%Y")
    to_date = end_date.strftime("%d/%m/%Y")
    search_country = matching_country if matching_country else country
    try:
        return (
            investpy.funds.get_fund_historical_data(
                fund_name, search_country, from_date=from_date, to_date=to_date
            ),
            fund_name,
            fund_symbol,
            matching_country,
        )
    except RuntimeError as e:
        logger.exception(str(e))
        return pd.DataFrame(), fund_name, fund_symbol, search_country
