"""Portfolio Controller"""
__docformat__ = "numpy"

import argparse
import logging
import os
from pathlib import Path
from typing import List

import pandas as pd
from prompt_toolkit.completion import NestedCompleter

from openbb_terminal import feature_flags as obbff
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    EXPORT_BOTH_RAW_DATA_AND_FIGURES,
    EXPORT_ONLY_FIGURES_ALLOWED,
    EXPORT_ONLY_RAW_DATA_ALLOWED,
    check_positive_float,
)

from openbb_terminal.menu import session
from openbb_terminal.parent_classes import BaseController
from openbb_terminal.portfolio import portfolio_model
from openbb_terminal.portfolio import portfolio_view
from openbb_terminal.portfolio import portfolio_helper
from openbb_terminal.portfolio.portfolio_optimization import po_controller
from openbb_terminal.rich_config import console, MenuText
from openbb_terminal.common.quantitative_analysis import qa_view

# pylint: disable=R1710,E1101,C0415,W0212,too-many-function-args,C0302,too-many-instance-attributes

logger = logging.getLogger(__name__)

portfolios_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "portfolios")


class PortfolioController(BaseController):
    """Portfolio Controller class"""

    CHOICES_COMMANDS = [
        "load",
        "show",
        "bench",
        "alloc",
        "perf",
        "yret",
        "mret",
        "dret",
        "distr",
        "holdv",
        "holdp",
        "maxdd",
        "var",
        "es",
        "sh",
        "so",
        "om",
        "rvol",
        "rsharpe",
        "rsort",
        "rbeta",
        "metric",
        "summary",
    ]
    CHOICES_MENUS = [
        "bro",
        "po",
        "pa",
    ]
    VALID_DISTRIBUTIONS = ["laplace", "student_t", "logistic", "normal"]
    AGGREGATION_METRICS = ["assets", "sectors", "countries", "regions"]
    VALID_METRICS = [
        "volatility",
        "sharpe",
        "sortino",
        "maxdrawdown",
        "rsquare",
        "skew",
        "kurtosis",
        "gaintopain",
        "trackerr",
        "information",
        "tail",
        "commonsense",
        "jensens",
        "calmar",
        "kelly",
        "payoff",
        "profitfactor",
    ]
    PATH = "/portfolio/"

    def __init__(self, queue: List[str] = None):
        """Constructor"""
        super().__init__(queue)
        self.file_types = ["xlsx", "csv"]

        self.DEFAULT_HOLDINGS_PATH = portfolio_helper.DEFAULT_HOLDINGS_PATH

        self.DATA_HOLDINGS_FILES = {
            filepath.name: filepath
            for file_type in self.file_types
            for filepath in Path(self.DEFAULT_HOLDINGS_PATH).rglob(f"*.{file_type}")
            if filepath.is_file()
        }

        self.portfolio_df = pd.DataFrame(
            columns=[
                "Date",
                "Name",
                "Type",
                "Sector",
                "Industry",
                "Country",
                "Price",
                "Quantity",
                "Fees",
                "Premium",
                "Investment",
                "Side",
                "Currency",
            ]
        )

        self.portfolio_name: str = ""
        self.benchmark_name: str = ""
        self.original_benchmark_name = ""
        self.risk_free_rate = 0
        self.portlist: List[str] = os.listdir(self.DEFAULT_HOLDINGS_PATH)
        self.portfolio: portfolio_model.PortfolioModel = (
            portfolio_model.PortfolioModel()
        )

        if session and obbff.USE_PROMPT_TOOLKIT:
            self.update_choices()

    def update_choices(self):

        self.DEFAULT_HOLDINGS_PATH = portfolio_helper.DEFAULT_HOLDINGS_PATH

        self.DATA_HOLDINGS_FILES = {
            filepath.name: filepath
            for file_type in self.file_types
            for filepath in Path(self.DEFAULT_HOLDINGS_PATH).rglob(f"*.{file_type}")
            if filepath.is_file()
        }

        choices: dict = {c: {} for c in self.controller_choices}
        choices["load"]["-f"] = {c: None for c in self.DATA_HOLDINGS_FILES}
        choices["load"]["--file"] = {c: None for c in self.DATA_HOLDINGS_FILES}
        choices["bench"] = {c: None for c in portfolio_helper.BENCHMARK_LIST}
        choices["alloc"] = {c: None for c in self.AGGREGATION_METRICS}
        choices["metric"] = {c: None for c in self.VALID_METRICS}
        self.choices = choices

        choices["support"] = self.SUPPORT_CHOICES
        choices["about"] = self.ABOUT_CHOICES

        self.completer = NestedCompleter.from_nested_dict(choices)

    def print_help(self):
        """Print help"""
        mt = MenuText("portfolio/")
        mt.add_menu("bro")
        mt.add_menu("po")
        mt.add_raw("\n")

        mt.add_cmd("load")
        mt.add_raw("\n")
        mt.add_param("_loaded", self.portfolio_name)
        mt.add_param("_riskfreerate", self.portfolio_name)
        mt.add_raw("\n")
        mt.add_cmd("show")
        mt.add_raw("\n")
        mt.add_cmd("bench")
        mt.add_raw("\n")
        mt.add_param("_benchmark", self.benchmark_name)
        mt.add_raw("\n")

        mt.add_info("_graphs_")
        mt.add_cmd("holdv", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("holdp", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("yret", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("mret", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("dret", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("distr", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("maxdd", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("rvol", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("rsharpe", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("rsort", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("rbeta", self.portfolio_name and self.benchmark_name)

        mt.add_info("_metrics_")
        mt.add_cmd("alloc", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("summary", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("metric", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("perf", self.portfolio_name and self.benchmark_name)

        mt.add_info("_risk_")
        mt.add_cmd("var", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("es", self.portfolio_name and self.benchmark_name)
        mt.add_cmd("os", self.portfolio_name and self.benchmark_name)

        port = bool(self.portfolio_name)
        port_bench = bool(self.portfolio_name) and bool(self.benchmark_name)

        help_text = f"""[menu]
>   bro              brokers holdings, \t\t supports: robinhood, ally, degiro, coinbase
>   po               portfolio optimization, \t optimize your portfolio weights efficiently[/menu]
[cmds]
    load             load data into the portfolio[/cmds]

[param]Loaded orderbook:[/param] {self.portfolio_name or ""}
[param]Risk Free Rate:  [/param] {self.risk_free_rate:.2%}
{("[unvl]", "[cmds]")[port]}
    show             show existing transactions{("[/unvl]", "[/cmds]")[port]}
{("[unvl]", "[cmds]")[port]}
    bench            define the benchmark{("[/unvl]", "[/cmds]")[port]}

[param]Benchmark:[/param] {self.benchmark_name or ""}

[info]Graphs:[/info]{("[unvl]", "[cmds]")[port_bench]}
    holdv            holdings of assets (absolute value)
    holdp            portfolio holdings of assets (in percentage)
    yret             yearly returns
    mret             monthly returns
    dret             daily returns
    distr            distribution of daily returns
    maxdd            maximum drawdown
    rvol             rolling volatility
    rsharpe          rolling sharpe
    rsort            rolling sortino
    rbeta            rolling beta
{("[/unvl]", "[/cmds]")[port_bench]}
[info]Metrics:[/info]{("[unvl]", "[cmds]")[port_bench]}
    alloc            allocation on an asset, sector, countries or regions basis
    summary          all portfolio vs benchmark metrics for a certain period of choice
    metric           portfolio vs benchmark metric for all different periods
    perf             performance of the portfolio versus benchmark{("[/unvl]", "[/cmds]")[port_bench]}

[info]Risk Metrics:[/info]{("[unvl]", "[cmds]")[port]}
    var              display value at risk
    es               display expected shortfall
    om               display omega ratio{("[/unvl]", "[/cmds]")[port]}
        """
        # TODO: Clean up the reports inputs
        # TODO: Edit the allocation to allow the different asset classes
        # [info]Reports:[/info]
        #    ar          annual report for performance of a given portfolio
        console.print(text=help_text, menu="Portfolio")
        self.update_choices()

    def custom_reset(self):
        """Class specific component of reset command"""
        objects_to_reload = ["portfolio"]
        if self.portfolio_name:
            objects_to_reload.append(f"load {self.portfolio_name}")
        if self.original_benchmark_name:
            objects_to_reload.append(f'bench "{self.original_benchmark_name}"')
        return objects_to_reload

    @log_start_end(log=logger)
    def call_bro(self, _):
        """Process bro command"""
        from openbb_terminal.portfolio.brokers.bro_controller import (
            BrokersController,
        )

        self.queue = self.load_class(BrokersController, self.queue)

    @log_start_end(log=logger)
    def call_po(self, _):
        """Process po command"""
        if self.portfolio is None:
            tickers = []
        else:
            tickers = self.portfolio.tickers_list
        self.queue = self.load_class(
            po_controller.PortfolioOptimizationController,
            tickers,
            None,
            None,
            self.queue,
        )

    @log_start_end(log=logger)
    def call_load(self, other_args: List[str]):
        """Process load command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="load",
            description="Load your portfolio",
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            dest="file",
            required="-h" not in other_args,
            help="The file to be loaded",
        )
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            dest="name",
            help="The name that you wish to give to your portfolio",
        )
        parser.add_argument(
            "-r",
            "--rfr",
            type=float,
            default=0,
            dest="risk_free_rate",
            help="Set the risk free rate.",
        )

        ns_parser = self.parse_known_args_and_warn(parser, other_args)

        if ns_parser and ns_parser.file:
            if ns_parser.file in self.DATA_HOLDINGS_FILES:
                file_location = self.DATA_HOLDINGS_FILES[ns_parser.file]
            else:
                file_location = ns_parser.file  # type: ignore

            orderbook = portfolio_model.PortfolioModel.read_orderbook(
                str(file_location)
            )
            self.portfolio = portfolio_model.PortfolioModel(orderbook)
            self.benchmark_name = ""

            if ns_parser.name:
                self.portfolio_name = ns_parser.name
            else:
                self.portfolio_name = ns_parser.file

            # Generate holdings from trades
            self.portfolio.generate_portfolio_data()

            # Add in the Risk-free rate
            self.portfolio.set_risk_free_rate(ns_parser.risk_free_rate)

            console.print(f"\n[bold]Portfolio:[/bold] {self.portfolio_name}")
            console.print(
                f"[bold]Risk Free Rate:[/bold] {self.portfolio.risk_free_rate}"
            )
            console.print()

    @log_start_end(log=logger)
    def call_show(self, _):
        """Process show command"""
        portfolio_view.display_orderbook(self.portfolio, show_index=False)

    @log_start_end(log=logger)
    def call_bench(self, other_args: List[str]):
        """Process bench command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="bench",
            description="Load in a benchmark from a selected list or set your own based on the ticker.",
        )
        parser.add_argument(
            "-b",
            "--benchmark",
            type=str,
            default="SPY",
            nargs="+",
            dest="benchmark",
            required="-h" not in other_args,
            help="Set the benchmark for the portfolio. By default, this is SPDR S&P 500 ETF Trust (SPY).",
        )
        parser.add_argument(
            "-s",
            "--full_shares",
            action="store_true",
            default=False,
            dest="full_shares",
            help="Whether to only make a trade with the benchmark when a full share can be bought (no partial shares).",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-b")

        ns_parser = self.parse_known_args_and_warn(parser, other_args)

        if ns_parser and self.portfolio is not None:
            # Needs to be checked since we want to use the start date of the portfolio when comparing with benchmark
            if self.portfolio_name:
                chosen_benchmark = " ".join(ns_parser.benchmark)

                if chosen_benchmark in portfolio_helper.BENCHMARK_LIST:
                    benchmark_ticker = portfolio_helper.BENCHMARK_LIST[chosen_benchmark]
                    self.original_benchmark_name = chosen_benchmark
                else:
                    benchmark_ticker = chosen_benchmark

                self.portfolio.load_benchmark(benchmark_ticker, ns_parser.full_shares)

                self.benchmark_name = chosen_benchmark

                # Make it so that there is no chance of there being a difference in length between
                # the portfolio and benchmark return DataFrames
                (
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                ) = portfolio_helper.make_equal_length(
                    self.portfolio.returns, self.portfolio.benchmark_returns
                )

                console.print(
                    f"[bold]\nBenchmark:[/bold] {self.benchmark_name} ({benchmark_ticker})"
                )
            else:
                console.print("[red]Please first load orderbook using 'load'[/red]\n")
            console.print()

    @log_start_end(log=logger)
    def call_alloc(self, other_args: List[str]):
        """Process alloc command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="alloc",
            description="""
                Show your allocation to each asset or sector compared to the benchmark.
            """,
        )
        parser.add_argument(
            "-a",
            "--agg",
            default="assets",
            choices=self.AGGREGATION_METRICS,
            dest="agg",
            help="The type of allocation aggregation you wish to do",
        )
        parser.add_argument(
            "-t",
            "--tables",
            action="store_true",
            default=False,
            dest="tables",
            help="Whether to also include the assets/sectors tables of both the benchmark and the portfolio.",
        )
        if other_args:
            if other_args and "-" not in other_args[0][0]:
                other_args.insert(0, "-a")

        ns_parser = self.parse_known_args_and_warn(parser, other_args, limit=10)

        if ns_parser and self.portfolio is not None:
            console.print()
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                if self.portfolio.portfolio_assets_allocation.empty:
                    self.portfolio.calculate_allocations()

                if ns_parser.agg == "assets":
                    portfolio_view.display_assets_allocation(
                        self.portfolio.portfolio_assets_allocation,
                        self.portfolio.benchmark_assets_allocation,
                        ns_parser.limit,
                        ns_parser.tables,
                    )
                elif ns_parser.agg == "sectors":
                    portfolio_view.display_category_allocation(
                        ns_parser.agg,
                        self.portfolio.portfolio_sectors_allocation,
                        self.portfolio.benchmark_sectors_allocation,
                        ns_parser.limit,
                        ns_parser.tables,
                    )
                elif ns_parser.agg == "countries":
                    portfolio_view.display_category_allocation(
                        ns_parser.agg,
                        self.portfolio.portfolio_country_allocation,
                        self.portfolio.benchmark_country_allocation,
                        ns_parser.limit,
                        ns_parser.tables,
                    )
                elif ns_parser.agg == "regions":
                    portfolio_view.display_category_allocation(
                        ns_parser.agg,
                        self.portfolio.portfolio_regional_allocation,
                        self.portfolio.benchmark_regional_allocation,
                        ns_parser.limit,
                        ns_parser.tables,
                    )
                else:
                    console.print(
                        f"{ns_parser.agg} is not an available option. The options "
                        f"are: {', '.join(self.AGGREGATION_METRICS)}"
                    )

    @log_start_end(log=logger)
    def call_perf(self, other_args: List[str]):
        """Process performance command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="performance",
            description="""
                Shows performance of each trade and total performance of the portfolio versus the benchmark.
            """,
        )
        parser.add_argument(
            "-t",
            "--show_trades",
            action="store_true",
            default=False,
            dest="show_trades",
            help="Whether to show performance on all trades in comparison to the benchmark.",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            choices=portfolio_helper.PERIODS,
            dest="period",
            default="all",
            help="The file to be loaded",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")

        ns_parser = self.parse_known_args_and_warn(parser, other_args)

        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):

                portfolio_view.display_performance_vs_benchmark(
                    self.portfolio.portfolio_trades,
                    self.portfolio.benchmark_trades,
                    ns_parser.period,
                    ns_parser.show_trades,
                )

    @log_start_end(log=logger)
    def call_holdv(self, other_args: List[str]):
        """Process holdv command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="holdv",
            description="Display holdings of assets (absolute value)",
        )
        parser.add_argument(
            "-s",
            "--sum",
            action="store_true",
            default=False,
            dest="sum_assets",
            help="Sum all assets value over time",
        )
        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES,
            raw=True,
            limit=10,
        )
        if ns_parser:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_holdings_value(
                    self.portfolio,
                    ns_parser.sum_assets,
                    ns_parser.raw,
                    ns_parser.limit,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_holdp(self, other_args: List[str]):
        """Process holdp command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="holdp",
            description="Display holdings of assets (in percentage)",
        )
        parser.add_argument(
            "-s",
            "--sum",
            action="store_true",
            default=False,
            dest="sum_assets",
            help="Sum all assets percentage over time",
        )
        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES,
            raw=True,
            limit=10,
        )
        if ns_parser:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_holdings_percentage(
                    self.portfolio,
                    ns_parser.sum_assets,
                    ns_parser.raw,
                    ns_parser.limit,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_var(self, other_args: List[str]):
        """Process var command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="var",
            description="""
                Provides value at risk (short: VaR) of the selected portfolio.
            """,
        )
        parser.add_argument(
            "-m",
            "--mean",
            action="store_true",
            default=False,
            dest="use_mean",
            help="If one should use the mean of the portfolio return",
        )
        parser.add_argument(
            "-a",
            "--adjusted",
            action="store_true",
            default=False,
            dest="adjusted",
            help="""
                If the VaR should be adjusted for skew and kurtosis (Cornish-Fisher-Expansion)
            """,
        )
        parser.add_argument(
            "-s",
            "--student",
            action="store_true",
            default=False,
            dest="student_t",
            help="""
                If one should use the student-t distribution
            """,
        )
        parser.add_argument(
            "-p",
            "--percentile",
            action="store",
            dest="percentile",
            type=float,
            default=99.9,
            help="""
                Percentile used for VaR calculations, for example input 99.9 equals a 99.9 Percent VaR
            """,
        )

        ns_parser = self.parse_known_args_and_warn(parser, other_args)

        if ns_parser and self.portfolio is not None:
            if self.portfolio_name:
                if ns_parser.adjusted and ns_parser.student_t:
                    console.print(
                        "Select either the adjusted or the student_t parameter.\n"
                    )
                else:
                    qa_view.display_var(
                        self.portfolio.returns,
                        "Portfolio",
                        ns_parser.use_mean,
                        ns_parser.adjusted,
                        ns_parser.student_t,
                        ns_parser.percentile / 100,
                        True,
                    )
            else:
                console.print(
                    "[red]Please first define the portfolio using 'load'[/red]\n"
                )

    @log_start_end(log=logger)
    def call_es(self, other_args: List[str]):
        """Process es command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="es",
            description="""
                Provides Expected Shortfall (short: ES) of the selected portfolio.
            """,
        )
        parser.add_argument(
            "-m",
            "--mean",
            action="store_true",
            default=False,
            dest="use_mean",
            help="If one should use the mean of the portfolios return",
        )
        parser.add_argument(
            "-d",
            "--dist",
            "--distributions",
            dest="distributions",
            type=str,
            choices=self.VALID_DISTRIBUTIONS,
            default="normal",
            help="Distribution used for the calculations",
        )
        parser.add_argument(
            "-p",
            "--percentile",
            action="store",
            dest="percentile",
            type=float,
            default=99.9,
            help="""
                Percentile used for ES calculations, for example input 99.9 equals a 99.9 Percent Expected Shortfall
            """,
        )

        ns_parser = self.parse_known_args_and_warn(parser, other_args)

        if ns_parser and self.portfolio is not None:
            if self.portfolio_name:
                qa_view.display_es(
                    self.portfolio.returns,
                    "Portfolio",
                    ns_parser.use_mean,
                    ns_parser.distributions,
                    ns_parser.percentile / 100,
                    True,
                )
            else:
                console.print(
                    "[red]Please first define the portfolio using 'load'[/red]\n"
                )

    @log_start_end(log=logger)
    def call_om(self, other_args: List[str]):
        """Process om command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="om",
            description="""
                   Provides omega ratio of the selected portfolio.
               """,
        )
        parser.add_argument(
            "-s",
            "--start",
            action="store",
            dest="start",
            type=float,
            default=0,
            help="""
                   Start of the omega ratio threshold
               """,
        )
        parser.add_argument(
            "-e",
            "--end",
            action="store",
            dest="end",
            type=float,
            default=1.5,
            help="""
                   End of the omega ratio threshold
               """,
        )
        ns_parser = self.parse_known_args_and_warn(parser, other_args)
        if ns_parser and self.portfolio is not None:
            if self.portfolio_name:
                data = self.portfolio.returns[1:]
                qa_view.display_omega(
                    data,
                    ns_parser.start,
                    ns_parser.end,
                )
            else:
                console.print(
                    "[red]Please first define the portfolio (via 'load')[/red]\n"
                )

    @log_start_end(log=logger)
    def call_yret(self, other_args: List[str]):
        """Process yret command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="yret",
            description="End of the year returns",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="all",
            choices=["3y", "5y", "10y", "all"],
            help="Period to select start end of the year returns",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            raw=True,
            export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES,
        )

        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_yearly_returns(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    ns_parser.period,
                    ns_parser.raw,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_mret(self, other_args: List[str]):
        """Process mret command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="mret",
            description="Monthly returns",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="all",
            choices=["3y", "5y", "10y", "all"],
            help="Period to select start end of the year returns",
        )
        parser.add_argument(
            "-s",
            "--show",
            action="store_true",
            default=False,
            dest="show_vals",
            help="Show monthly returns on heatmap",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            raw=True,
            export_allowed=EXPORT_ONLY_FIGURES_ALLOWED,
        )

        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_monthly_returns(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    ns_parser.period,
                    ns_parser.raw,
                    ns_parser.show_vals,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_dret(self, other_args: List[str]):
        """Process dret command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="dret",
            description="Daily returns",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="all",
            choices=["3y", "5y", "10y", "all"],
            help="Period to select start end of the year returns",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            raw=True,
            limit=10,
            export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES,
        )

        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_daily_returns(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    ns_parser.period,
                    ns_parser.raw,
                    ns_parser.limit,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_maxdd(self, other_args: List[str]):
        """Process maxdd command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="maxdd",
            description="Show portfolio maximum drawdown",
        )
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_ONLY_FIGURES_ALLOWED
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_maximum_drawdown(self.portfolio.portfolio_value)

    @log_start_end(log=logger)
    def call_rvol(self, other_args: List[str]):
        """Process rolling volatility command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="rvol",
            description="Show rolling volatility portfolio vs benchmark",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="1y",
            choices=list(portfolio_helper.PERIODS_DAYS.keys()),
            help="Period to apply rolling window",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_rolling_volatility(
                    self.portfolio.benchmark_returns,
                    self.portfolio.returns,
                    period=ns_parser.period,
                    export=ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_rsharpe(self, other_args: List[str]):
        """Process rolling sharpe command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="rsharpe",
            description="Show rolling sharpe portfolio vs benchmark",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="1y",
            choices=list(portfolio_helper.PERIODS_DAYS.keys()),
            help="Period to apply rolling window",
        )
        parser.add_argument(
            "-r",
            "--rfr",
            type=check_positive_float,
            dest="risk_free_rate",
            default=self.risk_free_rate,
            help="Set risk free rate for calculations.",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_rolling_sharpe(
                    self.portfolio.benchmark_returns,
                    self.portfolio.returns,
                    period=ns_parser.period,
                    risk_free_rate=ns_parser.risk_free_rate,
                    export=ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_rsort(self, other_args: List[str]):
        """Process rolling sortino command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="rsort",
            description="Show rolling sortino portfolio vs benchmark",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="1y",
            choices=list(portfolio_helper.PERIODS_DAYS.keys()),
            help="Period to apply rolling window",
        )
        parser.add_argument(
            "-r",
            "--rfr",
            type=check_positive_float,
            dest="risk_free_rate",
            default=self.risk_free_rate,
            help="Set risk free rate for calculations.",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_rolling_sortino(
                    self.portfolio.benchmark_returns,
                    self.portfolio.returns,
                    period=ns_parser.period,
                    risk_free_rate=ns_parser.risk_free_rate,
                    export=ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_rbeta(self, other_args: List[str]):
        """Process rolling beta command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="rbeta",
            description="Show rolling beta portfolio vs benchmark",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            dest="period",
            default="1y",
            choices=list(portfolio_helper.PERIODS_DAYS.keys()),
            help="Period to apply rolling window",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_rolling_beta(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    period=ns_parser.period,
                    export=ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_metric(self, other_args: List[str]):
        """Process metric command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="metric",
            description="Display metric of choice for different periods",
        )
        parser.add_argument(
            "-m",
            "--metric",
            type=str,
            dest="metric",
            default="-h" not in other_args,
            choices=self.VALID_METRICS,
            help="Set metric of choice",
        )
        parser.add_argument(
            "-r",
            "--rfr",
            type=check_positive_float,
            dest="risk_free_rate",
            default=self.risk_free_rate,
            help="Set risk free rate for calculations.",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-m")
        ns_parser = self.parse_known_args_and_warn(
            parser, other_args, export_allowed=EXPORT_ONLY_RAW_DATA_ALLOWED
        )
        if ns_parser:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                if ns_parser.metric == "skew":
                    portfolio_view.display_skewness(self.portfolio, ns_parser.export)
                elif ns_parser.metric == "kurtosis":
                    portfolio_view.display_kurtosis(self.portfolio, ns_parser.export)
                elif ns_parser.metric == "volatility":
                    portfolio_view.display_volatility(self.portfolio, ns_parser.export)
                elif ns_parser.metric == "sharpe":
                    portfolio_view.display_sharpe_ratio(
                        self.portfolio, ns_parser.risk_free_rate, ns_parser.export
                    )
                elif ns_parser.metric == "sortino":
                    portfolio_view.display_sortino_ratio(
                        self.portfolio, ns_parser.risk_free_rate, ns_parser.export
                    )
                elif ns_parser.metric == "maxdrawdown":
                    portfolio_view.display_maximum_drawdown_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "rsquare":
                    portfolio_view.display_rsquare(self.portfolio, ns_parser.export)
                elif ns_parser.metric == "gaintopain":
                    portfolio_view.display_gaintopain_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "trackerr":
                    portfolio_view.display_tracking_error(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "information":
                    portfolio_view.display_information_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "tail":
                    portfolio_view.display_tail_ratio(self.portfolio, ns_parser.export)
                elif ns_parser.metric == "commonsense":
                    portfolio_view.display_common_sense_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "jensens":
                    portfolio_view.display_jensens_alpha(
                        self.portfolio, ns_parser.risk_free_rate, ns_parser.export
                    )
                elif ns_parser.metric == "calmar":
                    portfolio_view.display_calmar_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "kelly":
                    portfolio_view.display_kelly_criterion(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "payoff" and self.portfolio is not None:
                    portfolio_view.display_payoff_ratio(
                        self.portfolio, ns_parser.export
                    )
                elif ns_parser.metric == "profitfactor" and self.portfolio is not None:
                    portfolio_view.display_profit_factor(
                        self.portfolio, ns_parser.export
                    )

    @log_start_end(log=logger)
    def call_distr(self, other_args: List[str]):
        """Process distr command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="distr",
            description="Compute distribution of daily returns",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            choices=portfolio_helper.PERIODS,
            dest="period",
            default="all",
            help="The file to be loaded",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")

        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            raw=True,
            export_allowed=EXPORT_BOTH_RAW_DATA_AND_FIGURES,
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_distribution_returns(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    ns_parser.period,
                    ns_parser.raw,
                    ns_parser.export,
                )

    @log_start_end(log=logger)
    def call_summary(self, other_args: List[str]):
        """Process summary command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="summary",
            description="Display summary of portfolio vs benchmark",
        )
        parser.add_argument(
            "-p",
            "--period",
            type=str,
            choices=portfolio_helper.PERIODS,
            dest="period",
            default="all",
            help="The file to be loaded",
        )
        parser.add_argument(
            "-r",
            "--rfr",
            type=check_positive_float,
            dest="risk_free_rate",
            default=self.risk_free_rate,
            help="Set risk free rate for calculations.",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-p")

        ns_parser = self.parse_known_args_and_warn(
            parser,
            other_args,
            export_allowed=EXPORT_ONLY_RAW_DATA_ALLOWED,
        )
        if ns_parser and self.portfolio is not None:
            if check_portfolio_benchmark_defined(
                self.portfolio_name, self.benchmark_name
            ):
                portfolio_view.display_summary_portfolio_benchmark(
                    self.portfolio.returns,
                    self.portfolio.benchmark_returns,
                    ns_parser.period,
                    ns_parser.risk_free_rate,
                    ns_parser.export,
                )


def check_portfolio_benchmark_defined(portfolio_name: str, benchmark_name: str) -> bool:
    """Check that portfolio and benchmark have been defined

    Parameters
    ----------
    portfolio_name: str
        Portfolio name, will be empty if not defined
    benchmark_name: str
        Benchmark name, will be empty if not defined

    Returns
    -------
    bool
        If both portfolio and benchmark have been defined
    """
    if portfolio_name and benchmark_name:
        return True
    if not portfolio_name:
        if not benchmark_name:
            console.print(
                "[red]Please first define the portfolio (via 'load') "
                "and the benchmark (via 'bench').[/red]\n"
            )
        else:
            console.print("[red]Please first define the portfolio (via 'load')[/red]\n")
    else:
        console.print("[red]Please first define the benchmark (via 'bench')[/red]\n")
    return False
