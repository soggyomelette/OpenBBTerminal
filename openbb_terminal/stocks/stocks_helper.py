"""Main helper"""
__docformat__ = "numpy"

import logging
import os
from datetime import datetime, timedelta, date
from typing import List, Union, Optional, Iterable

import financedatabase as fd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import mplfinance as mpf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pyEX
import pytz
import requests

import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from numpy.core.fromnumeric import transpose
from plotly.subplots import make_subplots
from scipy import stats

from openbb_terminal import config_terminal as cfg
from openbb_terminal.helper_funcs import (
    export_data,
    plot_autoscale,
    print_rich_table,
    lambda_long_number_format_y_axis,
)
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)

# pylint: disable=no-member,too-many-branches,C0302,R0913

INTERVALS = [1, 5, 15, 30, 60]
SOURCES = ["yf", "av", "iex"]

market_coverage_suffix = {
    "USA": ["CBT", "CME", "NYB", "CMX", "NYM", "US", ""],
    "Argentina": ["BA"],
    "Austria": ["VI"],
    "Australia": ["AX"],
    "Belgium": ["BR"],
    "Brazil": ["SA"],
    "Canada": ["CN", "NE", "TO", "V"],
    "Chile": ["SN"],
    "China": ["SS", "SZ"],
    "Czech-Republic": ["PR"],
    "Denmark": ["CO"],
    "Egypt": ["CA"],
    "Estonia": ["TL"],
    "Europe": ["NX"],
    "Finland": ["HE"],
    "France": ["PA"],
    "Germany": ["BE", "BM", "DU", "F", "HM", "HA", "MU", "SG", "DE"],
    "Greece": ["AT"],
    "Hong-Kong": ["HK"],
    "Hungary": ["BD"],
    "Iceland": ["IC"],
    "India": ["BO", "NS"],
    "Indonesia": ["JK"],
    "Ireland": ["IR"],
    "Israel": ["TA"],
    "Italy": ["MI"],
    "Japan": ["T", "S"],
    "Latvia": ["RG"],
    "Lithuania": ["VS"],
    "Malaysia": ["KL"],
    "Mexico": ["MX"],
    "Netherlands": ["AS"],
    "New-Zealand": ["NZ"],
    "Norway": ["OL"],
    "Portugal": ["LS"],
    "Qatar": ["QA"],
    "Russia": ["ME"],
    "Singapore": ["SI"],
    "South-Africa": ["JO"],
    "South-Korea": ["KS", "KQ"],
    "Spain": ["MC"],
    "Saudi-Arabia": ["SAU"],
    "Sweden": ["ST"],
    "Switzerland": ["SW"],
    "Taiwan": ["TWO", "TW"],
    "Thailand": ["BK"],
    "Turkey": ["IS"],
    "United-Kingdom": ["L", "IL"],
    "Venezuela": ["CR"],
}

INCOME_PLOT = {
    "av": [
        "reported_currency",
        "gross_profit",
        "total_revenue",
        "cost_of_revenue",
        "cost_of_goods_and_services_sold",
        "operating_income",
        "selling_general_and_administrative",
        "research_and_development",
        "operating_expenses",
        "investment_income_net",
        "net_interest_income",
        "interest_income",
        "interest_expense",
        "non_interest_income",
        "other_non_operating_income",
        "depreciation",
        "depreciation_and_amortization",
        "income_before_tax",
        "income_tax_expense",
        "interest_and_debt_expense",
        "net_income_from_continuing_operations",
        "comprehensive_income_net_of_tax",
        "ebit",
        "ebitda",
        "net_income",
    ],
    "polygon": [
        "cost_of_revenue",
        "diluted_earnings_per_share",
        "costs_and_expenses",
        "gross_profit",
        "non_operating_income_loss",
        "operating_income_loss",
        "participating_securities_distributed_and_undistributed_earnings_loss_basic",
        "income_tax_expense_benefit",
        "net_income_loss_attributable_to_parent",
        "net_income_loss",
        "income_tax_expense_benefit_deferred",
        "preferred_stock_dividends_and_other_adjustments",
        "operating_expenses",
        "income_loss_from_continuing_operations_before_tax",
        "net_income_loss_attributable_to_non_controlling_interest",
        "income_loss_from_continuing_operations_after_tax",
        "revenues",
        "net_income_loss_available_to_common_stockholders_basic",
        "benefits_costs_expenses",
        "basic_earnings_per_share",
        "interest_expense_operating",
        "income_loss_before_equity_method_investments",
    ],
    "yf": [
        "total_revenue",
        "cost_of_revenue",
        "gross_profit",
        "research_development",
        "selling_general_and_administrative",
        "total_operating_expenses",
        "operating_income_or_loss",
        "interest_expense",
        "total_other_income/expenses_net",
        "income_before_tax",
        "income_tax_expense",
        "income_from_continuing_operations",
        "net_income",
        "net_income_available_to_common_shareholders",
        "basic_eps",
        "diluted_eps",
        "basic_average_shares",
        "diluted_average_shares",
        "ebitda",
    ],
    "fmp": [
        "reported_currency",
        "cik",
        "filling_date",
        "accepted_date",
        "calendar_year",
        "period",
        "revenue",
        "cost_of_revenue",
        "gross_profit",
        "gross_profit_ratio",
        "research_and_development_expenses",
        "general_and_administrative_expenses",
        "selling_and_marketing_expenses",
        "selling_general_and_administrative_expenses",
        "other_expenses",
        "operating_expenses",
        "cost_and_expenses",
        "interest_income",
        "interest_expense",
        "depreciation_and_amortization",
        "ebitda",
        "ebitda_ratio",
        "operating_income",
        "operating_income_ratio",
        "total_other_income_expenses_net",
        "income_before_tax",
        "income_before_tax_ratio",
        "income_tax_expense",
        "net_income",
        "net_income_ratio",
        "eps",
        "eps_diluted",
        "weighted_average_shs_out",
        "weighted_average_shs_out_dil",
        "link",
        "final_link",
    ],
}
BALANCE_PLOT = {
    "av": [
        "reported_currency",
        "total_assets",
        "total_current_assets",
        "cash_and_cash_equivalents_at_carrying_value",
        "cash_and_short_term_investments",
        "inventory",
        "current_net_receivables",
        "total_non_current_assets",
        "property_plant_equipment",
        "accumulated_depreciation_amortization_ppe",
        "intangible_assets",
        "intangible_assets_excluding_goodwill",
        "goodwill",
        "investments",
        "long_term_investments",
        "short_term_investments",
        "other_current_assets",
        "other_non_currrent_assets",
        "total_liabilities",
        "total_current_liabilities",
        "current_accounts_payable",
        "deferred_revenue",
        "current_debt",
        "short_term_debt",
        "total_non_current_liabilities",
        "capital_lease_obligations",
        "long_term_debt",
        "current_long_term_debt",
        "long_term_debt_non_current",
        "short_long_term_debt_total",
        "other_current_liabilities",
        "other_non_current_liabilities",
        "total_shareholder_equity",
        "treasury_stock",
        "retained_earnings",
        "common_stock",
        "common_stock_shares_outstanding",
    ],
    "polygon": [
        "equity_attributable_to_non_controlling_interest",
        "liabilities",
        "non_current_assets",
        "equity",
        "assets",
        "current_assets",
        "equity_attributable_to_parent",
        "current_liabilities",
        "non_current_liabilities",
        "fixed_assets",
        "other_than_fixed_non_current_assets",
        "liabilities_and_equity",
    ],
    "yf": [
        "cash_and_cash_equivalents",
        "other_short-term_investments",
        "total_cash",
        "net_receivables",
        "inventory",
        "other_current_assets",
        "total_current_assets",
        "gross_property, plant_and_equipment",
        "accumulated_depreciation",
        "net_property, plant_and_equipment",
        "equity_and_other_investments",
        "other_long-term_assets",
        "total_non-current_assets",
        "total_assets",
        "current_debt",
        "accounts_payable",
        "deferred_revenues",
        "other_current_liabilities",
        "total_current_liabilities",
        "long-term_debt",
        "deferred_tax_liabilities",
        "deferred_revenues",
        "other_long-term_liabilities",
        "total_non-current_liabilities",
        "total_liabilities",
        "common_stock",
        "retained_earnings",
        "accumulated_other_comprehensive_income",
        "total_stockholders'_equity",
        "total_liabilities_and_stockholders'_equity",
    ],
    "fmp": [
        "reported_currency",
        "cik",
        "filling_date",
        "accepted_date",
        "calendar_year",
        "period",
        "cash_and_cash_equivalents",
        "short_term_investments",
        "cash_and_short_term_investments",
        "net_receivables",
        "inventory",
        "other_current_assets",
        "total_current_assets",
        "property_plant_equipment_net",
        "goodwill",
        "intangible_assets",
        "goodwill_and_intangible_assets",
        "long_term_investments",
        "tax_assets",
        "other_non_current_assets",
        "total_non_current_assets",
        "other_assets",
        "total_assets",
        "account_payables",
        "short_term_debt",
        "tax_payables",
        "deferred_revenue",
        "other_current_liabilities",
        "total_current_liabilities",
        "long_term_debt",
        "deferred_revenue_non_current",
        "deferred_tax_liabilities_non_current",
        "other_non_current_liabilities",
        "total_non_current_liabilities",
        "other_liabilities",
        "capital_lease_obligations",
        "total_liabilities",
        "preferred_stock",
        "common_stock",
        "retained_earnings",
        "accumulated_other_comprehensive_income_loss",
        "other_total_stockholders_equity",
        "total_stockholders_equity",
        "total_liabilities_and_stockholders_equity",
        "minority_interest",
        "total_equity",
        "total_liabilities_and_total_equity",
        "total_investments",
        "total_debt",
        "net_debt",
        "link",
        "final_link",
    ],
}
CASH_PLOT = {
    "av": [
        "reported_currency",
        "operating_cash_flow",
        "payments_for_operating_activities",
        "proceeds_from_operating_activities",
        "change_in_operating_liabilities",
        "change_in_operating_assets",
        "depreciation_depletion_and_amortization",
        "capital_expenditures",
        "change_in_receivables",
        "change_in_inventory",
        "profit_loss",
        "cash_flow_from_investment",
        "cash_flow_from_financing",
        "proceeds_from_repayments_of_short_term_debt",
        "payments_for_repurchase_of_common_stock",
        "payments_for_repurchase_of_equity",
        "payments_for_repurchase_of_preferred_stock",
        "dividend_payout",
        "dividend_payout_common_stock",
        "dividend_payout_preferred_stock",
        "proceeds_from_issuance_of_common_stock",
        "proceeds_from_issuance_of_long_term_debt_and_capital_securities_net",
        "proceeds_from_issuance_of_preferred_stock",
        "proceeds_from_repurchase_of_equity",
        "proceeds_from_sale_of_treasury_stock",
        "change_in_cash_and_cash_equivalents",
        "change_in_exchange_rate",
        "net_income",
    ],
    "polygon": [
        "net_cash_flow_from_financing_activities_continuing",
        "net_cash_flow_continuing",
        "net_cash_flow_from_investing_activities",
        "net_cash_flow",
        "net_cash_flow_from_operating_activities",
        "net_cash_flow_from_financing_activities",
        "net_cash_flow_from_operating_activities_continuing",
        "net_cash_flow_from_investing_activities_continuing",
    ],
    "yf": [
        "net_income",
        "depreciation_&_amortisation",
        "deferred_income_taxes",
        "stock-based_compensation",
        "change_in working_capital",
        "accounts_receivable",
        "inventory",
        "accounts_payable",
        "other_working_capital",
        "other_non-cash_items",
        "net_cash_provided_by_operating_activities",
        "investments_in_property, plant_and_equipment",
        "acquisitions, net",
        "purchases_of_investments",
        "sales/maturities_of_investments",
        "other_investing_activities",
        "net_cash_used_for_investing_activities",
        "debt_repayment",
        "common_stock_issued",
        "common_stock_repurchased",
        "dividends_paid",
        "other_financing_activities",
        "net_cash_used_provided_by_(used_for)_financing_activities",
        "net_change_in_cash",
        "cash_at_beginning_of_period",
        "cash_at_end_of_period",
        "operating_cash_flow",
        "capital_expenditure",
        "free_cash_flow",
    ],
    "fmp": [
        "reported_currency",
        "cik",
        "filling_date",
        "accepted_date",
        "calendar_year",
        "period",
        "net_income",
        "depreciation_and_amortization",
        "deferred_income_tax",
        "stock_based_compensation",
        "change_in_working_capital",
        "accounts_receivables",
        "inventory",
        "accounts_payables",
        "other_working_capital",
        "other_non_cash_items",
        "net_cash_provided_by_operating_activities",
        "investments_in_property_plant_and_equipment",
        "acquisitions_net",
        "purchases_of_investments",
        "sales_maturities_of_investments",
        "other_investing_activites",
        "net_cash_used_for_investing_activites",
        "debt_repayment",
        "common_stock_issued",
        "common_stock_repurchased",
        "dividends_paid",
        "other_financing_activites",
        "net_cash_used_provided_by_financing_activities",
        "effect_of_forex_changes_on_cash",
        "net_change_in_cash",
        "cash_at_end_of_period",
        "cash_at_beginning_of_period",
        "operating_cash_flow",
        "capital_expenditure",
        "free_cash_flow",
        "link",
        "final_link",
    ],
}
exchange_mappings = (
    pd.read_csv(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "mappings", "Mic_Codes.csv"
        ),
        index_col=0,
        header=None,
    )
    .squeeze("columns")
    .to_dict()
)


def search(
    query: str = "",
    country: str = "",
    sector: str = "",
    industry: str = "",
    exchange_country: str = "",
    limit: int = 0,
    export: str = "",
) -> None:
    """Search selected query for tickers.

    Parameters
    ----------
    query : str
        The search term used to find company tickers
    country: str
        Search by country to find stocks matching the criteria
    sector : str
        Search by sector to find stocks matching the criteria
    industry : str
        Search by industry to find stocks matching the criteria
    exchange_country: str
        Search by exchange country to find stock matching
    limit : int
        The limit of companies shown.
    export : str
        Export data
    """
    if country:
        if sector:
            if industry:
                data = fd.select_equities(
                    country=country,
                    sector=sector,
                    industry=industry,
                    exclude_exchanges=False,
                )
            else:  # no industry
                data = fd.select_equities(
                    country=country,
                    sector=sector,
                    exclude_exchanges=False,
                )
        else:  # no sector
            if industry:
                data = fd.select_equities(
                    country=country,
                    industry=industry,
                    exclude_exchanges=False,
                )
            else:  # no industry
                data = fd.select_equities(
                    country=country,
                    exclude_exchanges=False,
                )

    else:  # no country
        if sector:
            if industry:
                data = fd.select_equities(
                    sector=sector,
                    industry=industry,
                    exclude_exchanges=False,
                )
            else:  # no industry
                data = fd.select_equities(
                    sector=sector,
                    exclude_exchanges=False,
                )
        else:  # no sector
            if industry:
                data = fd.select_equities(
                    industry=industry,
                    exclude_exchanges=False,
                )
            else:  # no industry
                data = fd.select_equities(
                    exclude_exchanges=False,
                )

    if not data:
        console.print("No companies found.\n")
        return

    if query:
        d = fd.search_products(
            data, query, search="long_name", case_sensitive=False, new_database=None
        )
    else:
        d = data

    if not d:
        console.print("No companies found.\n")
        return

    df = pd.DataFrame.from_dict(d).T[["long_name", "country", "sector", "industry"]]
    if exchange_country:
        if exchange_country in market_coverage_suffix:
            suffix_tickers = [
                ticker.split(".")[1] if "." in ticker else ""
                for ticker in list(df.index)
            ]
            df = df[
                [
                    val in market_coverage_suffix[exchange_country]
                    for val in suffix_tickers
                ]
            ]

    exchange_suffix = {}
    for k, v in market_coverage_suffix.items():
        for x in v:
            exchange_suffix[x] = k

    df["exchange"] = [
        exchange_suffix.get(ticker.split(".")[1]) if "." in ticker else "USA"
        for ticker in list(df.index)
    ]

    title = "Companies found"
    if query:
        title += f" on term {query}"
    if exchange_country:
        title += f" {exchange_country} exchange"
    if country:
        title += f" in {country}"
    if sector:
        title += f" within {sector}"
        if industry:
            title += f" and {industry}"
    if not sector and industry:
        title += f" within {industry}"

    print_rich_table(
        df.iloc[:limit] if limit else df,
        show_index=True,
        headers=["Name", "Country", "Sector", "Industry", "Exchange"],
        title=title,
    )

    export_data(export, os.path.dirname(os.path.abspath(__file__)), "search", df)


# pylint:disable=too-many-return-statements
def load(
    symbol: str,
    start_date: datetime = (datetime.now() - timedelta(days=1100)),
    interval: int = 1440,
    end_date: datetime = datetime.now(),
    prepost: bool = False,
    source: str = "yf",
    iexrange: str = "ytd",
    weekly: bool = False,
    monthly: bool = False,
):
    """
    Load a symbol to perform analysis using the string above as a template. Optional arguments and their
    descriptions are listed above. The default source is, yFinance (https://pypi.org/project/yfinance/).
    Alternatively, one may select either AlphaVantage (https://www.alphavantage.co/documentation/)
    or IEX Cloud (https://iexcloud.io/docs/api/) as the data source for the analysis.
    Please note that certain analytical features are exclusive to the source.

    To load a symbol from an exchange outside of the NYSE/NASDAQ default, use yFinance as the source and
    add the corresponding exchange to the end of the symbol. i.e. ‘BNS.TO’.

    BNS is a dual-listed stock, there are separate options chains and order books for each listing.
    Opportunities for arbitrage may arise from momentary pricing discrepancies between listings
    with a dynamic exchange rate as a second order opportunity in ForEx spreads.

    Find the full list of supported exchanges here:
    https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html

    Certain analytical features, such as VWAP, require the ticker to be loaded as intraday
    using the ‘-i x’ argument.  When encountering this error, simply reload the symbol using
    the interval argument. i.e. ‘load -t BNS -s YYYY-MM-DD -i 1 -p’ loads one-minute intervals,
    including Pre/After Market data, using the default source, yFinance.

    Certain features, such as the Prediction menu, require the symbol to be loaded as daily and not intraday.

    Parameters
    ----------
    symbol: str
        Ticker to get data
    start_date: datetime
        Start date to get data from with
    interval: int
        Interval (in minutes) to get data 1, 5, 15, 30, 60 or 1440
    end_date: datetime
        End date to get data from with
    prepost: bool
        Pre and After hours data
    source: str
        Source of data extracted
    iexrange: str
        Timeframe to get IEX data.
    weekly: bool
        Flag to get weekly data
    monthly: bool
        Flag to get monthly data

    Returns
    -------
    df_stock_candidate: pd.DataFrame
        Dataframe of data
    """

    # Daily
    if interval == 1440:

        # Alpha Vantage Source
        if source == "av":
            try:
                ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format="pandas")
                # pylint: disable=unbalanced-tuple-unpacking
                df_stock_candidate, _ = ts.get_daily_adjusted(
                    symbol=symbol, outputsize="full"
                )
            except Exception as e:
                console.print(e, "")
                return pd.DataFrame()

            df_stock_candidate.columns = [
                val.split(". ")[1].capitalize() for val in df_stock_candidate.columns
            ]

            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "Adjusted close": "Adj Close",
                }
            )

            # Check that loading a stock was not successful
            # pylint: disable=no-member
            if df_stock_candidate.empty:
                console.print("No data found.\n")
                return pd.DataFrame()

            df_stock_candidate.index = df_stock_candidate.index.tz_localize(None)

            # pylint: disable=no-member
            df_stock_candidate.sort_index(ascending=True, inplace=True)

            # Slice dataframe from the starting date YYYY-MM-DD selected
            df_stock_candidate = df_stock_candidate[
                (df_stock_candidate.index >= start_date.strftime("%Y-%m-%d"))
                & (df_stock_candidate.index <= end_date.strftime("%Y-%m-%d"))
            ]

        # Yahoo Finance Source
        elif source == "yf":

            # TODO: Better handling of interval with week/month
            int_ = "1d"
            int_string = "Daily"
            if weekly:
                int_ = "1wk"
                int_string = "Weekly"
            if monthly:
                int_ = "1mo"
                int_string = "Monthly"

            # Win10 version of mktime cannot cope with dates before 1970
            if os.name == "nt" and start_date < datetime(1970, 1, 1):
                start_date = datetime(
                    1970, 1, 2
                )  # 1 day buffer in case of timezone adjustments

            # Adding a dropna for weekly and monthly because these include weird NaN columns.
            df_stock_candidate = yf.download(
                symbol, start=start_date, end=end_date, progress=False, interval=int_
            ).dropna(axis=0)

            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                console.print("")
                return pd.DataFrame()

            df_stock_candidate.index.name = "date"

        # IEX Cloud Source
        elif source == "iex":
            df_stock_candidate = pd.DataFrame()

            try:
                client = pyEX.Client(api_token=cfg.API_IEX_TOKEN, version="v1")

                df_stock_candidate = client.chartDF(symbol, timeframe=iexrange)

                # Check that loading a stock was not successful
                if df_stock_candidate.empty:
                    console.print("No data found.\n")
                    return df_stock_candidate

            except Exception as e:
                if "The API key provided is not valid" in str(e):
                    console.print("[red]Invalid API Key[/red]\n")
                else:
                    console.print(e, "\n")

                return df_stock_candidate

            df_stock_candidate = df_stock_candidate[
                ["close", "fHigh", "fLow", "fOpen", "fClose", "volume"]
            ]
            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "close": "Close",
                    "fHigh": "High",
                    "fLow": "Low",
                    "fOpen": "Open",
                    "fClose": "Adj Close",
                    "volume": "Volume",
                }
            )

            df_stock_candidate.sort_index(ascending=True, inplace=True)

        # Polygon source
        elif source == "polygon":

            # Polygon allows: day, minute, hour, day, week, month, quarter, year
            timespan = "day"
            if weekly or monthly:
                timespan = "week" if weekly else "month"

            request_url = (
                f"https://api.polygon.io/v2/aggs/ticker/"
                f"{symbol.upper()}/range/1/{timespan}/"
                f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?adjusted=true"
                f"&sort=desc&limit=49999&apiKey={cfg.API_POLYGON_KEY}"
            )
            r = requests.get(request_url)
            if r.status_code != 200:
                console.print("[red]Error in polygon request[/red]")
                return pd.DataFrame()

            r_json = r.json()
            if "results" not in r_json.keys():
                console.print("[red]No results found in polygon reply.[/red]")
                return pd.DataFrame()

            df_stock_candidate = pd.DataFrame(r_json["results"])

            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "o": "Open",
                    "c": "Adj Close",
                    "h": "High",
                    "l": "Low",
                    "t": "date",
                    "v": "Volume",
                    "n": "Transactions",
                }
            )
            df_stock_candidate["date"] = pd.to_datetime(
                df_stock_candidate.date, unit="ms"
            )
            # TODO: Clean up Close vs Adj Close throughout
            df_stock_candidate["Close"] = df_stock_candidate["Adj Close"]
            df_stock_candidate = df_stock_candidate.sort_values(by="date")
            df_stock_candidate = df_stock_candidate.set_index("date")

        s_start = df_stock_candidate.index[0]
        s_interval = f"{interval}min"
        int_string = "Daily" if interval == 1440 else "Intraday"

    else:

        if source == "yf":
            s_int = str(interval) + "m"
            s_interval = s_int + "in"
            d_granularity = {"1m": 6, "5m": 59, "15m": 59, "30m": 59, "60m": 729}

            s_start_dt = datetime.utcnow() - timedelta(days=d_granularity[s_int])
            s_date_start = s_start_dt.strftime("%Y-%m-%d")

            df_stock_candidate = yf.download(
                symbol,
                start=s_date_start
                if s_start_dt > start_date
                else start_date.strftime("%Y-%m-%d"),
                progress=False,
                interval=s_int,
                prepost=prepost,
            )

            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                console.print()
                return pd.DataFrame()

            df_stock_candidate.index = df_stock_candidate.index.tz_localize(None)

            if s_start_dt > start_date:
                s_start = pytz.utc.localize(s_start_dt)
            else:
                s_start = start_date

            df_stock_candidate.index.name = "date"

        elif source == "polygon":
            request_url = (
                f"https://api.polygon.io/v2/aggs/ticker/"
                f"{symbol.upper()}/range/{interval}/minute/{start_date.strftime('%Y-%m-%d')}"
                f"/{end_date.strftime('%Y-%m-%d')}"
                f"?adjusted=true&sort=desc&limit=49999&apiKey={cfg.API_POLYGON_KEY}"
            )
            r = requests.get(request_url)
            if r.status_code != 200:
                console.print("[red]Error in polygon request[/red]")
                return pd.DataFrame()

            r_json = r.json()
            if "results" not in r_json.keys():
                console.print("[red]No results found in polygon reply.[/red]")
                return pd.DataFrame()

            df_stock_candidate = pd.DataFrame(r_json["results"])

            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "o": "Open",
                    "c": "Close",
                    "h": "High",
                    "l": "Low",
                    "t": "date",
                    "v": "Volume",
                    "n": "Transactions",
                }
            )
            df_stock_candidate["date"] = pd.to_datetime(
                df_stock_candidate.date, unit="ms"
            )
            df_stock_candidate["Adj Close"] = df_stock_candidate.Close
            df_stock_candidate = df_stock_candidate.sort_values(by="date")

            df_stock_candidate = df_stock_candidate.set_index("date")
            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                console.print()
                return pd.DataFrame()

            df_stock_candidate.index = (
                df_stock_candidate.index.tz_localize(tz="UTC")
                .tz_convert("US/Eastern")
                .tz_localize(None)
            )
            s_start_dt = df_stock_candidate.index[0]

            if s_start_dt > start_date:
                s_start = pytz.utc.localize(s_start_dt)
            else:
                s_start = start_date
            s_interval = f"{interval}min"
        int_string = "Intraday"

    s_intraday = (f"Intraday {s_interval}", int_string)[interval == 1440]

    console.print(
        f"\nLoading {s_intraday} {symbol.upper()} stock "
        f"with starting period {s_start.strftime('%Y-%m-%d')} for analysis.",
    )

    return df_stock_candidate


def display_candle(
    symbol: str,
    data: pd.DataFrame,
    use_matplotlib: bool = True,
    intraday: bool = False,
    add_trend: bool = False,
    ma: Optional[Iterable[int]] = None,
    asset_type: str = "Stock",
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Shows candle plot of loaded ticker. [Source: Yahoo Finance, IEX Cloud or Alpha Vantage]

    Parameters
    ----------
    symbol: str
        Ticker name
    data: pd.DataFrame
        Stock dataframe
    use_matplotlib: bool
        Flag to use matplotlib instead of interactive plotly chart
    intraday: bool
        Flag for intraday data for plotly range breaks
    add_trend: bool
        Flag to add high and low trends to chart
    ma: Tuple[int]
        Moving averages to add to the candle
    asset_type_: str
        String to include in title
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axes are expected in the list), by default None
    asset_type_: str
        String to include in title
    """
    if add_trend:
        if (data.index[1] - data.index[0]).total_seconds() >= 86400:
            data = find_trendline(data, "OC_High", "high")
            data = find_trendline(data, "OC_Low", "low")

    if use_matplotlib:
        ap0 = []
        if add_trend:
            if "OC_High_trend" in data.columns:
                ap0.append(
                    mpf.make_addplot(
                        data["OC_High_trend"],
                        color=cfg.theme.up_color,
                        secondary_y=False,
                    ),
                )

            if "OC_Low_trend" in data.columns:
                ap0.append(
                    mpf.make_addplot(
                        data["OC_Low_trend"],
                        color=cfg.theme.down_color,
                        secondary_y=False,
                    ),
                )

        candle_chart_kwargs = {
            "type": "candle",
            "style": cfg.theme.mpf_style,
            "volume": True,
            "addplot": ap0,
            "xrotation": cfg.theme.xticks_rotation,
            "scale_padding": {"left": 0.3, "right": 1, "top": 0.8, "bottom": 0.8},
            "update_width_config": {
                "candle_linewidth": 0.6,
                "candle_width": 0.8,
                "volume_linewidth": 0.8,
                "volume_width": 0.8,
            },
            "warn_too_much_data": 10000,
        }

        kwargs = {"mav": ma} if ma else {}

        if external_axes is None:
            candle_chart_kwargs["returnfig"] = True
            candle_chart_kwargs["figratio"] = (10, 7)
            candle_chart_kwargs["figscale"] = 1.10
            candle_chart_kwargs["figsize"] = plot_autoscale()
            candle_chart_kwargs["warn_too_much_data"] = 100_000

            fig, ax = mpf.plot(data, **candle_chart_kwargs, **kwargs)
            lambda_long_number_format_y_axis(data, "Volume", ax)

            fig.suptitle(
                f"{asset_type} {symbol}",
                x=0.055,
                y=0.965,
                horizontalalignment="left",
            )

            if ma:
                # Manually construct the chart legend
                colors = []

                for i, _ in enumerate(ma):
                    colors.append(cfg.theme.get_colors()[i])

                lines = [Line2D([0], [0], color=c) for c in colors]
                labels = ["MA " + str(label) for label in ma]
                ax[0].legend(lines, labels)

            cfg.theme.visualize_output(force_tight_layout=False)
        else:
            if len(external_axes) != 2:
                logger.error("Expected list of one axis item.")
                console.print("[red]Expected list of 2 axis items.\n[/red]")
                return
            ax1, ax2 = external_axes
            candle_chart_kwargs["ax"] = ax1
            candle_chart_kwargs["volume"] = ax2
            mpf.plot(data, **candle_chart_kwargs)

    else:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=(f"{symbol}", "Volume"),
            row_width=[0.2, 0.7],
        )
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data.Open,
                high=data.High,
                low=data.Low,
                close=data.Close,
                name="OHLC",
            ),
            row=1,
            col=1,
        )
        if ma:
            plotly_colors = [
                "black",
                "teal",
                "blue",
                "purple",
                "orange",
                "gray",
                "deepskyblue",
            ]
            for idx, ma_val in enumerate(ma):
                temp = data["Adj Close"].copy()
                temp[f"ma{ma_val}"] = data["Adj Close"].rolling(ma_val).mean()
                temp = temp.dropna()
                fig.add_trace(
                    go.Scatter(
                        x=temp.index,
                        y=temp[f"ma{ma_val}"],
                        name=f"MA{ma_val}",
                        mode="lines",
                        line=go.scatter.Line(
                            color=plotly_colors[np.mod(idx, len(plotly_colors))]
                        ),
                    ),
                    row=1,
                    col=1,
                )

        if add_trend:
            if "OC_High_trend" in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data["OC_High_trend"],
                        name="High Trend",
                        mode="lines",
                        line=go.scatter.Line(color="green"),
                    ),
                    row=1,
                    col=1,
                )
            if "OC_Low_trend" in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data["OC_Low_trend"],
                        name="Low Trend",
                        mode="lines",
                        line=go.scatter.Line(color="red"),
                    ),
                    row=1,
                    col=1,
                )

        colors = [
            "red" if row.Open < row["Adj Close"] else "green"
            for _, row in data.iterrows()
        ]
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data.Volume,
                name="Volume",
                marker_color=colors,
            ),
            row=2,
            col=1,
        )
        fig.update_layout(
            yaxis_title="Stock Price ($)",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="1m",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=3,
                                label="3m",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(
                                count=1,
                                label="1y",
                                step="year",
                                stepmode="backward",
                            ),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=False),
                type="date",
            ),
        )

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=[
                        dict(
                            label="linear",
                            method="relayout",
                            args=[{"yaxis.type": "linear"}],
                        ),
                        dict(
                            label="log", method="relayout", args=[{"yaxis.type": "log"}]
                        ),
                    ]
                )
            ]
        )

        if intraday:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(bounds=[20, 9], pattern="hour"),
                ]
            )

        fig.show(config=dict({"scrollZoom": True}))


def quote(symbol: str):
    """Ticker quote

    Parameters
    ----------
    symbol : str
        Ticker
    """
    ticker = yf.Ticker(symbol)

    try:
        quote_df = pd.DataFrame(
            [
                {
                    "Symbol": ticker.info["symbol"],
                    "Name": ticker.info["shortName"],
                    "Price": ticker.info["regularMarketPrice"],
                    "Open": ticker.info["regularMarketOpen"],
                    "High": ticker.info["dayHigh"],
                    "Low": ticker.info["dayLow"],
                    "Previous Close": ticker.info["previousClose"],
                    "Volume": ticker.info["volume"],
                    "52 Week High": ticker.info["fiftyTwoWeekHigh"],
                    "52 Week Low": ticker.info["fiftyTwoWeekLow"],
                }
            ]
        )

        quote_df["Change"] = quote_df["Price"] - quote_df["Previous Close"]
        quote_df["Change %"] = quote_df.apply(
            lambda x: f'{((x["Change"] / x["Previous Close"]) * 100):.2f}%',
            axis="columns",
        )
        for c in [
            "Price",
            "Open",
            "High",
            "Low",
            "Previous Close",
            "52 Week High",
            "52 Week Low",
            "Change",
        ]:
            quote_df[c] = quote_df[c].apply(lambda x: f"{x:.2f}")
        quote_df["Volume"] = quote_df["Volume"].apply(lambda x: f"{x:,}")

        quote_df = quote_df.set_index("Symbol")

        quote_data = transpose(quote_df)

        print_rich_table(quote_data, title="Ticker Quote", show_index=True)

    except KeyError:
        logger.exception("Invalid stock ticker")
        console.print(f"Invalid stock ticker: {symbol}")


def load_ticker(
    ticker: str, start_date: Union[str, datetime], end_date: Union[str, datetime] = ""
) -> pd.DataFrame:
    """Loads a ticker data from Yahoo Finance, adds a data index column data_id and Open-Close High/Low columns.

    Parameters
    ----------
    ticker : str
        The stock ticker.
    start_date : Union[str,datetime]
        Start date to load stock ticker data formatted YYYY-MM-DD.
    end_date : Union[str,datetime]
        End date to load stock ticker data formatted YYYY-MM-DD.

    Returns
    -------
    DataFrame
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    if end_date:
        df_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    else:
        df_data = yf.download(ticker, start=start_date, progress=False)

    df_data.index = pd.to_datetime(df_data.index)
    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    return df_data


def process_candle(df: pd.DataFrame) -> pd.DataFrame:
    """Process DataFrame into candle style plot

    Parameters
    ----------
    df : DataFrame
        Stock dataframe.

    Returns
    -------
    DataFrame
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    df_data = df.copy()
    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    df_data["ma20"] = df_data["Close"].rolling(20).mean().fillna(method="bfill")
    df_data["ma50"] = df_data["Close"].rolling(50).mean().fillna(method="bfill")

    return df_data


def find_trendline(
    df_data: pd.DataFrame, y_key: str, high_low: str = "high"
) -> pd.DataFrame:
    """Attempts to find a trend line based on y_key column from a given stock ticker data frame.

    Parameters
    ----------
    df_data : DataFrame
        The stock ticker data frame with at least date_id, y_key columns.
    y_key : str
        Column name to base the trend line on.
    high_low: str, optional
        Either "high" or "low". High is the default.

    Returns
    -------
    DataFrame
        If a trend is successfully found,
            An updated Panda's data frame with a trend data {y_key}_trend column.
        If no trend was found,
            An original Panda's data frame
    """

    for iteration in [3, 4, 5, 6, 7]:
        df_temp = df_data.copy()
        while len(df_temp) > iteration:
            reg = stats.linregress(
                x=df_temp["date_id"],
                y=df_temp[y_key],
            )

            if high_low == "high":
                df_temp = df_temp.loc[
                    df_temp[y_key] > reg[0] * df_temp["date_id"] + reg[1]
                ]
            else:
                df_temp = df_temp.loc[
                    df_temp[y_key] < reg[0] * df_temp["date_id"] + reg[1]
                ]

        if len(df_temp) > 1:
            break

    if len(df_temp) == 1:
        return df_data

    reg = stats.linregress(
        x=df_temp["date_id"],
        y=df_temp[y_key],
    )

    df_data[f"{y_key}_trend"] = reg[0] * df_data["date_id"] + reg[1]

    return df_data


def additional_info_about_ticker(ticker: str) -> str:
    """Information about trading the ticker such as exchange, currency, timezone and market status

    Parameters
    ----------
    ticker : str
        The stock ticker to extract if stock market is open or not

    Returns
    -------
    str
        Additional information about trading the ticker
    """
    extra_info = ""

    if ticker:
        if ".US" in ticker.upper():
            ticker = ticker.rstrip(".US")
            ticker = ticker.rstrip(".us")
        ticker_info = yf.Ticker(ticker).info
        extra_info += "\n[param]Company:  [/param]"
        if "shortName" in ticker_info and ticker_info["shortName"]:
            extra_info += ticker_info["shortName"]
        extra_info += "\n[param]Exchange: [/param]"
        if "exchange" in ticker_info and ticker_info["exchange"]:
            exchange_name = ticker_info["exchange"]
            extra_info += (
                exchange_mappings["X" + exchange_name]
                if "X" + exchange_name in exchange_mappings
                else exchange_name
            )

        extra_info += "\n[param]Currency: [/param]"
        if "currency" in ticker_info and ticker_info["currency"]:
            extra_info += ticker_info["currency"]

    else:
        extra_info += "\n[param]Company: [/param]"
        extra_info += "\n[param]Exchange: [/param]"
        extra_info += "\n[param]Currency: [/param]"

    return extra_info + "\n"


def clean_fraction(num, denom):
    """Returns the decimal value or NA if the operation cannot be performed

    Parameters
    ----------
    num : Any
        The numerator for the fraction
    denom : Any
        The denominator for the fraction

    Returns
    ----------
    val : Any
        The value of the fraction
    """
    try:
        return num / denom
    except TypeError:
        return "N/A"


def load_custom(file_path: str) -> pd.DataFrame:
    """Loads in a custom csv file

    Parameters
    ----------
    file_path: str
        Path to file

    Returns
    -------
    pd.DataFrame:
        Dataframe of stock data
    """
    # Double check that the file exists
    if not os.path.exists(file_path):
        console.print("[red]File path does not exist.[/red]\n")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    console.print(f"Loaded data has columns: {', '.join(df.columns.to_list())}\n")

    # Nasdaq specific
    if "Close/Last" in df.columns:
        df = df.rename(columns={"Close/Last": "Close"})
    if "Last" in df.columns:
        df = df.rename(columns={"Last": "Close"})

    df.columns = [col.lower().rstrip().lstrip() for col in df.columns]

    for col in df.columns:
        if col in ["date", "time", "timestamp", "datetime"]:
            df[col] = pd.to_datetime(df[col])
            df = df.set_index(col)
            console.print(f"Column [blue]{col.title()}[/blue] set as index.")

    df.columns = [col.title() for col in df.columns]
    df.index.name = df.index.name.title()

    df = df.applymap(
        lambda x: clean_function(x) if not isinstance(x, (int, float)) else x
    )
    if "Adj Close" not in df.columns:
        df["Adj Close"] = df.Close.copy()

    return df


def clean_function(entry: str) -> Union[str, float]:
    """Helper function for cleaning stock data from csv.  This can be customized for csvs"""
    # If there is a digit, get rid of common characters and return float
    if any(char.isdigit() for char in entry):
        return float(entry.replace("$", "").replace(",", ""))
    return entry


def show_quick_performance(stock_df: pd.DataFrame, ticker: str):
    """Show quick performance stats of stock prices.  Daily prices expected"""
    closes = stock_df["Adj Close"]
    volumes = stock_df["Volume"]

    perfs = {
        "1 Day": 100 * closes.pct_change(2)[-1],
        "1 Week": 100 * closes.pct_change(5)[-1],
        "1 Month": 100 * closes.pct_change(21)[-1],
        "1 Year": 100 * closes.pct_change(252)[-1],
    }
    if "2022-01-03" in closes.index:
        closes_ytd = closes[closes.index > f"{date.today().year}-01-01"]
        perfs["YTD"] = 100 * (closes_ytd[-1] - closes_ytd[0]) / closes_ytd[0]
    else:
        perfs["Period"] = 100 * (closes[-1] - closes[0]) / closes[0]

    df = pd.DataFrame.from_dict(perfs, orient="index").dropna().T
    df = df.applymap(lambda x: str(round(x, 2)) + " %")
    df = df.applymap(lambda x: f"[red]{x}[/red]" if "-" in x else f"[green]{x}[/green]")
    if len(closes) > 252:
        df["Volatility (1Y)"] = (
            str(round(100 * np.sqrt(252) * closes[-252:].pct_change().std(), 2)) + " %"
        )
    else:
        df["Volatility (Ann)"] = (
            str(round(100 * np.sqrt(252) * closes.pct_change().std(), 2)) + " %"
        )
    if len(volumes) > 10:
        df["Volume (10D avg)"] = (
            str(round(np.mean(volumes[-12:-2]) / 1_000_000, 2)) + " M"
        )

    df["Last Price"] = str(round(closes[-1], 2))
    print_rich_table(
        df, show_index=False, headers=df.columns, title=f"{ticker.upper()} Performance"
    )


def show_codes_polygon(ticker: str):
    """Show FIGI, SIC and SIK codes for ticker

    Parameters
    ----------
    ticker: str
        Stock ticker
    """
    link = f"https://api.polygon.io/v3/reference/tickers/{ticker.upper()}?apiKey={cfg.API_POLYGON_KEY}"
    if cfg.API_POLYGON_KEY == "REPLACE_ME":
        console.print("[red]Polygon API key missing[/red]\n")
        return
    r = requests.get(link)
    if r.status_code != 200:
        console.print("[red]Error in polygon request[/red]\n")
        return
    r_json = r.json()
    if "results" not in r_json.keys():
        console.print("[red]Results not found in polygon request[/red]")
        return
    r_json = r_json["results"]
    cols = ["cik", "composite_figi", "share_class_figi", "sic_code"]
    vals = []
    for col in cols:
        vals.append(r_json[col])
    df = pd.DataFrame({"codes": [c.upper() for c in cols], "vals": vals})
    df.codes = df.codes.apply(lambda x: x.replace("_", " "))
    print_rich_table(
        df, show_index=False, headers=["", ""], title=f"{ticker.upper()} Codes"
    )
