"""The BitQuery view"""
__docformat__ = "numpy"

import logging
import os

from openbb_terminal.cryptocurrency.dataframe_helpers import (
    lambda_very_long_number_formatter,
)
from openbb_terminal.cryptocurrency.onchain import bitquery_model
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data, print_rich_table
from openbb_terminal.decorators import check_api_key

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_dex_trades(
    trade_amount_currency: str = "USD",
    kind: str = "dex",
    top: int = 20,
    days: int = 90,
    sortby: str = "tradeAmount",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Trades on Decentralized Exchanges aggregated by DEX or Month
    [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    kind: str
        Aggregate trades by dex or time
    trade_amount_currency: str
        Currency of displayed trade amount. Default: USD
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    days:  int
        Last n days to query data. Maximum 365 (bigger numbers can cause timeouts
        on server side)
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    if kind == "time":
        df = bitquery_model.get_dex_trades_monthly(trade_amount_currency, days, ascend)
    else:
        df = bitquery_model.get_dex_trades_by_exchange(
            trade_amount_currency, days, sortby, ascend
        )

    if not df.empty:
        df_data = df.copy()

        df[["tradeAmount", "trades"]] = df[["tradeAmount", "trades"]].applymap(
            lambda x: lambda_very_long_number_formatter(x)
        )

        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
            title="Trades on Decentralized Exchanges",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "lt",
            df_data,
        )


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_daily_volume_for_given_pair(
    symbol: str = "WBTC",
    vs: str = "USDT",
    top: int = 20,
    sortby: str = "date",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Display daily volume for given pair
    [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    symbol: str
        ERC20 token symbol or address
    vs: str
        Quote currency.
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    export : str
        Export dataframe data to csv,json,xlsx file

    Returns
    -------
    pd.DataFrame
        Token volume on different decentralized exchanges
    """

    df = bitquery_model.get_daily_dex_volume_for_given_pair(
        symbol=symbol,
        vs=vs,
        limit=top,
        sortby=sortby,
        ascend=ascend,
    )

    if df.empty:
        return

    df_data = df.copy()

    df[["tradeAmount", "trades"]] = df[["tradeAmount", "trades"]].applymap(
        lambda x: lambda_very_long_number_formatter(x)
    )

    print_rich_table(
        df.head(top),
        headers=list(df.columns),
        show_index=False,
        title="Daily Volume for Pair",
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "dvcp",
        df_data,
    )


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_dex_volume_for_token(
    symbol: str = "WBTC",
    trade_amount_currency: str = "USD",
    top: int = 10,
    sortby: str = "tradeAmount",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Display token volume on different Decentralized Exchanges.
    [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    symbol: str
        ERC20 token symbol or address
    trade_amount_currency: str
        Currency of displayed trade amount. Default: USD
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    export : str
        Export dataframe data to csv,json,xlsx file
    Returns
    -------
    pd.DataFrame
        Token volume on different decentralized exchanges
    """

    df = bitquery_model.get_token_volume_on_dexes(
        symbol=symbol,
        trade_amount_currency=trade_amount_currency,
        sortby=sortby,
        ascend=ascend,
    )
    if not df.empty:
        df_data = df.copy()
        df[["tradeAmount", "trades"]] = df[["tradeAmount", "trades"]].applymap(
            lambda x: lambda_very_long_number_formatter(x)
        )

        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
            title="Token Volume on Exchanges",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "tv",
            df_data,
        )


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_ethereum_unique_senders(
    interval: str = "days",
    limit: int = 10,
    sortby: str = "date",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Display number of unique ethereum addresses which made a transaction in given time interval
     [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    interval: str
        Time interval in which ethereum address made transaction. month, week or day
    limit: int
        Number of records to display. It's calculated base on provided interval.
        If interval is month then calculation is made in the way: limit * 30 = time period,
        in case if interval is set to week, then time period is calculated as limit * 7.
        For better user experience maximum time period in days is equal to 90.
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    export : str
        Export dataframe data to csv,json,xlsx file
    Returns
    -------
    pd.DataFrame
        Number of unique ethereum addresses which made a transaction in given time interval
    """

    df = bitquery_model.get_ethereum_unique_senders(interval, limit, sortby, ascend)
    if not df.empty:
        df[["uniqueSenders", "transactions", "maximumGasPrice"]] = df[
            ["uniqueSenders", "transactions", "maximumGasPrice"]
        ].applymap(lambda x: lambda_very_long_number_formatter(x))

        df_data = df.copy()

        print_rich_table(
            df,
            headers=list(df.columns),
            show_index=False,
            title="Unique Ethereum Addresses",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "ueat",
            df_data,
        )


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_most_traded_pairs(
    exchange="Uniswap",
    days: int = 10,
    top: int = 10,
    sortby: str = "tradeAmount",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Display most traded crypto pairs on given decentralized exchange in chosen time period.
     [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    exchange:
        Decentralized exchange name
    days:
        Number of days taken into calculation account.
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    export : str
        Export dataframe data to csv,json,xlsx file
    Returns
    -------
    pd.DataFrame
        Most traded crypto pairs on given decentralized exchange in chosen time period.
    """

    df = bitquery_model.get_most_traded_pairs(
        exchange=exchange, limit=days, sortby=sortby, ascend=ascend
    )
    if not df.empty:
        df_data = df.copy()
        df[["tradeAmount", "trades"]] = df[["tradeAmount", "trades"]].applymap(
            lambda x: lambda_very_long_number_formatter(x)
        )

        print_rich_table(
            df.head(top),
            headers=list(df.columns),
            show_index=False,
            title="Most Traded Crypto Pairs",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "ttcp",
            df_data,
        )


@log_start_end(log=logger)
@check_api_key(["API_BITQUERY_KEY"])
def display_spread_for_crypto_pair(
    symbol="ETH",
    vs="USDC",
    days: int = 10,
    sortby: str = "date",
    ascend: bool = True,
    export: str = "",
) -> None:
    """Display an average bid and ask prices, average spread for given crypto pair for chosen
    time period. [Source: https://graphql.bitquery.io/]

    Parameters
    ----------
    days:  int
        Last n days to query data
    symbol: str
        ERC20 token symbol
    vs: str
        Quoted currency.
    sortby: str
        Key by which to sort data
    ascend: bool
        Flag to sort data ascending
    export : str
        Export dataframe data to csv,json,xlsx file

    Returns
    -------
    pd.DataFrame
        Average bid and ask prices, spread for given crypto pair for chosen time period
    """

    df = bitquery_model.get_spread_for_crypto_pair(
        symbol=symbol, vs=vs, limit=days, sortby=sortby, ascend=ascend
    )
    if not df.empty:

        print_rich_table(
            df,
            headers=list(df.columns),
            show_index=False,
            title="Average Spread for Given Crypto",
        )

        export_data(
            export,
            os.path.dirname(os.path.abspath(__file__)),
            "baas",
            df,
        )
