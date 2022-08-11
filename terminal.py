#!/usr/bin/env python
"""Main Terminal Module"""
__docformat__ = "numpy"

import argparse
import difflib
import logging
import os
import platform
import sys
import webbrowser
from typing import List
from pathlib import Path
import dotenv

from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

from openbb_terminal.common import feedparser_view
from openbb_terminal.core.config.constants import REPO_DIR, ENV_FILE, USER_HOME
from openbb_terminal.core.log.generation.path_tracking_file_handler import (
    PathTrackingFileHandler,
)
from openbb_terminal import feature_flags as obbff
from openbb_terminal.helper_funcs import (
    check_positive,
    get_flair,
    parse_simple_args,
    EXPORT_ONLY_RAW_DATA_ALLOWED,
)
from openbb_terminal.loggers import setup_logging
from openbb_terminal.menu import session
from openbb_terminal.parent_classes import BaseController
from openbb_terminal.rich_config import console, MenuText, translate
from openbb_terminal.terminal_helper import (
    bootup,
    check_for_updates,
    is_reset,
    print_goodbye,
    reset,
    suppress_stdout,
    update_terminal,
    welcome_message,
)
from openbb_terminal.helper_funcs import parse_and_split_input

# pylint: disable=too-many-public-methods,import-outside-toplevel,too-many-branches,no-member

logger = logging.getLogger(__name__)

env_file = str(ENV_FILE)


class TerminalController(BaseController):
    """Terminal Controller class"""

    CHOICES_COMMANDS = [
        "keys",
        "settings",
        "survey",
        "update",
        "featflags",
        "exe",
        "guess",
        "news",
    ]
    CHOICES_MENUS = [
        "stocks",
        "economy",
        "crypto",
        "portfolio",
        "forex",
        "etf",
        "reports",
        "dashboards",
        "funds",
        "alternative",
        "econometrics",
        "sources",
    ]

    PATH = "/"
    ROUTINE_CHOICES = {
        file: None
        for file in os.listdir(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), "routines")
        )
        if file.endswith(".openbb")
    }

    GUESS_TOTAL_TRIES = 0
    GUESS_NUMBER_TRIES_LEFT = 0
    GUESS_SUM_SCORE = 0.0
    GUESS_CORRECTLY = 0

    def __init__(self, jobs_cmds: List[str] = None):
        """Constructor"""
        super().__init__(jobs_cmds)

        if session and obbff.USE_PROMPT_TOOLKIT:
            choices: dict = {c: {} for c in self.controller_choices}
            choices["support"] = self.SUPPORT_CHOICES
            choices["exe"] = self.ROUTINE_CHOICES

            self.completer = NestedCompleter.from_nested_dict(choices)

        self.queue: List[str] = list()

        if jobs_cmds:
            self.queue = parse_and_split_input(
                an_input=" ".join(jobs_cmds), custom_filters=[]
            )

        self.update_success = False

    def print_help(self):
        """Print help"""
        mt = MenuText("")
        mt.add_info("_home_")
        mt.add_cmd("about")
        mt.add_cmd("support")
        mt.add_cmd("survey")
        mt.add_cmd("update")
        mt.add_raw("\n")
        mt.add_info("_configure_")
        mt.add_menu("keys")
        mt.add_menu("featflags")
        mt.add_menu("sources")
        mt.add_menu("settings")
        mt.add_raw("\n")
        mt.add_cmd("news")
        mt.add_cmd("exe")
        mt.add_raw("\n")
        mt.add_info("_main_menu_")
        mt.add_menu("stocks")
        mt.add_menu("crypto")
        mt.add_menu("etf")
        mt.add_menu("economy")
        mt.add_menu("forex")
        mt.add_menu("funds")
        mt.add_menu("alternative")
        mt.add_raw("\n")
        mt.add_info("_others_")
        mt.add_menu("econometrics")
        mt.add_menu("portfolio")
        mt.add_menu("dashboards")
        mt.add_menu("reports")
        console.print(text=mt.menu_text, menu="Home")

    def call_news(self, other_args: List[str]) -> None:
        """Process news command"""
        parse = argparse.ArgumentParser(
            add_help=False,
            prog="news",
            description=translate("news"),
        )
        parse.add_argument(
            "-t",
            "--term",
            dest="term",
            default="",
            nargs="+",
            help="search for a term on the news",
        )
        parse.add_argument(
            "-a",
            "--article",
            dest="article",
            default="bloomberg",
            nargs="+",
            help="articles from where to get news from",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-t")
        news_parser = self.parse_known_args_and_warn(
            parse, other_args, EXPORT_ONLY_RAW_DATA_ALLOWED, limit=5
        )
        if news_parser:
            feedparser_view.display_news(
                " ".join(news_parser.term),
                " ".join(news_parser.article),
                news_parser.limit,
                news_parser.export,
            )

    def call_guess(self, other_args: List[str]) -> None:
        """Process guess command"""
        import time
        import json
        import random

        if self.GUESS_NUMBER_TRIES_LEFT == 0 and self.GUESS_SUM_SCORE < 0.01:
            parser_exe = argparse.ArgumentParser(
                add_help=False,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                prog="guess",
                description="Guess command to achieve task successfully.",
            )
            parser_exe.add_argument(
                "-l",
                "--limit",
                type=check_positive,
                help="Number of tasks to attempt.",
                dest="limit",
                default=1,
            )
            if other_args and "-" not in other_args[0][0]:
                other_args.insert(0, "-l")
                ns_parser_guess = parse_simple_args(parser_exe, other_args)

                if self.GUESS_TOTAL_TRIES == 0:
                    self.GUESS_NUMBER_TRIES_LEFT = ns_parser_guess.limit
                    self.GUESS_SUM_SCORE = 0
                    self.GUESS_TOTAL_TRIES = ns_parser_guess.limit

        try:
            with open(obbff.GUESS_EASTER_EGG_FILE) as f:
                # Load the file as a JSON document
                json_doc = json.load(f)

                task = random.choice(list(json_doc.keys()))  # nosec
                solution = json_doc[task]

                start = time.time()
                console.print(f"\n[yellow]{task}[/yellow]\n")
                an_input = session.prompt("GUESS / $ ")
                time_dif = time.time() - start

                # When there are multiple paths to same solution
                if isinstance(solution, List):
                    if an_input.lower() in [s.lower() for s in solution]:
                        self.queue = an_input.split("/") + ["home"]
                        console.print(
                            f"\n[green]You guessed correctly in {round(time_dif, 2)} seconds![green]\n"
                        )
                        # If we are already counting successes
                        if self.GUESS_TOTAL_TRIES > 0:
                            self.GUESS_CORRECTLY += 1
                            self.GUESS_SUM_SCORE += time_dif
                    else:
                        solutions_texts = "\n".join(solution)
                        console.print(
                            f"\n[red]You guessed wrong! The correct paths would have been:\n{solutions_texts}[/red]\n"
                        )

                # When there is a single path to the solution
                else:
                    if an_input.lower() == solution.lower():
                        self.queue = an_input.split("/") + ["home"]
                        console.print(
                            f"\n[green]You guessed correctly in {round(time_dif, 2)} seconds![green]\n"
                        )
                        # If we are already counting successes
                        if self.GUESS_TOTAL_TRIES > 0:
                            self.GUESS_CORRECTLY += 1
                            self.GUESS_SUM_SCORE += time_dif
                    else:
                        console.print(
                            f"\n[red]You guessed wrong! The correct path would have been:\n{solution}[/red]\n"
                        )

                # Compute average score and provide a result if it's the last try
                if self.GUESS_TOTAL_TRIES > 0:

                    self.GUESS_NUMBER_TRIES_LEFT -= 1
                    if self.GUESS_NUMBER_TRIES_LEFT == 0 and self.GUESS_TOTAL_TRIES > 1:
                        color = (
                            "green"
                            if self.GUESS_CORRECTLY == self.GUESS_TOTAL_TRIES
                            else "red"
                        )
                        console.print(
                            f"[{color}]OUTCOME: You got {int(self.GUESS_CORRECTLY)} out of"
                            f" {int(self.GUESS_TOTAL_TRIES)}.[/{color}]\n"
                        )
                        if self.GUESS_CORRECTLY == self.GUESS_TOTAL_TRIES:
                            avg = self.GUESS_SUM_SCORE / self.GUESS_TOTAL_TRIES
                            console.print(
                                f"[green]Average score: {round(avg, 2)} seconds![/green]\n"
                            )
                        self.GUESS_TOTAL_TRIES = 0
                        self.GUESS_CORRECTLY = 0
                        self.GUESS_SUM_SCORE = 0
                    else:
                        self.queue += ["guess"]

        except Exception as e:
            console.print(
                f"[red]Failed to load guess game from file: "
                f"{obbff.GUESS_EASTER_EGG_FILE}[/red]"
            )
            console.print(f"[red]{e}[/red]")

    @staticmethod
    def call_survey(_) -> None:
        """Process survey command"""
        webbrowser.open("https://openbb.co/survey")

    def call_update(self, _):
        """Process update command"""
        if not obbff.PACKAGED_APPLICATION:
            self.update_success = not update_terminal()
        else:
            console.print(
                "Find the most recent release of the OpenBB Terminal here: "
                "https://openbb.co/products/terminal#get-started\n"
            )

    def call_keys(self, _):
        """Process keys command"""
        from openbb_terminal.keys_controller import KeysController

        self.queue = self.load_class(KeysController, self.queue, env_file)

    def call_settings(self, _):
        """Process settings command"""
        from openbb_terminal.settings_controller import SettingsController

        self.queue = self.load_class(SettingsController, self.queue)

    def call_featflags(self, _):
        """Process feature flags command"""
        from openbb_terminal.featflags_controller import FeatureFlagsController

        self.queue = self.load_class(FeatureFlagsController, self.queue)

    def call_stocks(self, _):
        """Process stocks command"""
        from openbb_terminal.stocks.stocks_controller import StocksController

        self.queue = self.load_class(StocksController, self.queue)

    def call_crypto(self, _):
        """Process crypto command"""
        from openbb_terminal.cryptocurrency.crypto_controller import CryptoController

        self.queue = self.load_class(CryptoController, self.queue)

    def call_economy(self, _):
        """Process economy command"""
        from openbb_terminal.economy.economy_controller import EconomyController

        self.queue = self.load_class(EconomyController, self.queue)

    def call_etf(self, _):
        """Process etf command"""
        from openbb_terminal.etf.etf_controller import ETFController

        self.queue = self.load_class(ETFController, self.queue)

    def call_funds(self, _):
        """Process etf command"""
        from openbb_terminal.mutual_funds.mutual_fund_controller import (
            FundController,
        )

        self.queue = self.load_class(FundController, self.queue)

    def call_forex(self, _):
        """Process forex command"""
        from openbb_terminal.forex.forex_controller import ForexController

        self.queue = self.load_class(ForexController, self.queue)

    def call_reports(self, _):
        """Process reports command"""
        if not obbff.PACKAGED_APPLICATION:
            from openbb_terminal.reports.reports_controller import (
                ReportController,
            )

            self.queue = self.load_class(ReportController, self.queue)
        else:
            console.print("This feature is coming soon.")
            console.print(
                "Use the source code and an Anaconda environment if you are familiar with Python."
            )

    def call_dashboards(self, _):
        """Process dashboards command"""
        if not obbff.PACKAGED_APPLICATION:
            from openbb_terminal.dashboards.dashboards_controller import (
                DashboardsController,
            )

            self.queue = self.load_class(DashboardsController, self.queue)
        else:
            console.print("This feature is coming soon.")
            console.print(
                "Use the source code and an Anaconda environment if you are familiar with Python."
            )

    def call_alternative(self, _):
        """Process alternative command"""
        from openbb_terminal.alternative.alt_controller import (
            AlternativeDataController,
        )

        self.queue = self.load_class(AlternativeDataController, self.queue)

    def call_econometrics(self, _):
        """Process econometrics command"""
        from openbb_terminal.econometrics.econometrics_controller import (
            EconometricsController,
        )

        self.queue = EconometricsController(self.queue).menu()

    def call_portfolio(self, _):
        """Process portfolio command"""
        from openbb_terminal.portfolio.portfolio_controller import (
            PortfolioController,
        )

        self.queue = self.load_class(PortfolioController, self.queue)

    def call_sources(self, _):
        """Process sources command"""
        from openbb_terminal.sources_controller import SourcesController

        self.queue = self.load_class(SourcesController, self.queue)

    def call_exe(self, other_args: List[str]):
        """Process exe command"""
        # Merge rest of string path to other_args and remove queue since it is a dir
        other_args += self.queue

        if not other_args:
            console.print(
                "[red]Provide a path to the routine you wish to execute.\n[/red]"
            )
            return

        full_input = " ".join(other_args)
        if " " in full_input:
            other_args_processed = full_input.split(" ")
        else:
            other_args_processed = [full_input]
        self.queue = []

        path_routine = ""
        args = list()
        for idx, path_dir in enumerate(other_args_processed):
            if path_dir in ("-i", "--input"):
                args = [path_routine[1:]] + other_args_processed[idx:]
                break
            if path_dir not in ("-f", "--file"):
                path_routine += f"/{path_dir}"

        if not args:
            args = [path_routine[1:]]

        parser_exe = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="exe",
            description="Execute automated routine script.",
        )
        parser_exe.add_argument(
            "-f",
            "--file",
            help="The path or .openbb file to run.",
            dest="path",
            default="",
            required="-h" not in args,
        )
        parser_exe.add_argument(
            "-i",
            "--input",
            help="Select multiple inputs to be replaced in the routine and separated by commas. E.g. GME,AMC,BTC-USD",
            dest="routine_args",
            type=lambda s: [str(item) for item in s.split(",")],
        )
        if args and "-" not in args[0][0]:
            args.insert(0, "-f")
        ns_parser_exe = parse_simple_args(parser_exe, args)
        if ns_parser_exe:
            if ns_parser_exe.path:
                if ns_parser_exe.path in self.ROUTINE_CHOICES:
                    path = os.path.join(
                        os.path.abspath(os.path.dirname(__file__)),
                        "routines",
                        ns_parser_exe.path,
                    )
                else:
                    path = ns_parser_exe.path

                with open(path) as fp:
                    raw_lines = [
                        x for x in fp if (not is_reset(x)) and ("#" not in x) and x
                    ]
                    raw_lines = [
                        raw_line.strip("\n")
                        for raw_line in raw_lines
                        if raw_line.strip("\n")
                    ]
                    if ns_parser_exe.routine_args:
                        lines = list()
                        for rawline in raw_lines:
                            templine = rawline
                            for i, arg in enumerate(ns_parser_exe.routine_args):
                                templine = templine.replace(f"$ARGV[{i}]", arg)
                            lines.append(templine)
                    else:
                        lines = raw_lines

                    simulate_argv = f"/{'/'.join([line.rstrip() for line in lines])}"
                    file_cmds = simulate_argv.replace("//", "/home/").split()
                    file_cmds = (
                        insert_start_slash(file_cmds) if file_cmds else file_cmds
                    )
                    cmds_with_params = " ".join(file_cmds)
                    self.queue = [
                        val
                        for val in parse_and_split_input(
                            an_input=cmds_with_params, custom_filters=[]
                        )
                        if val
                    ]

                    if "export" in self.queue[0]:
                        export_path = self.queue[0].split(" ")[1]
                        # If the path selected does not start from the user root, give relative location from root
                        if export_path[0] == "~":
                            export_path = export_path.replace("~", USER_HOME.as_posix())
                        elif export_path[0] != "/":
                            export_path = os.path.join(
                                os.path.dirname(os.path.abspath(__file__)), export_path
                            )

                        # Check if the directory exists
                        if os.path.isdir(export_path):
                            console.print(
                                f"Export data to be saved in the selected folder: '{export_path}'"
                            )
                        else:
                            os.makedirs(export_path)
                            console.print(
                                f"[green]Folder '{export_path}' successfully created.[/green]"
                            )
                        obbff.EXPORT_FOLDER_PATH = export_path
                        self.queue = self.queue[1:]


# pylint: disable=global-statement
def terminal(jobs_cmds: List[str] = None, appName: str = "gst"):
    """Terminal Menu"""
    # TODO: HELP WANTED! Refactor the appName setting if a more elegant solution comes up
    if obbff.PACKAGED_APPLICATION:
        appName = "gst_packaged"

    setup_logging(appName)
    logger.info("START")
    log_settings()

    if jobs_cmds is not None and jobs_cmds:
        logger.info("INPUT: %s", "/".join(jobs_cmds))

    export_path = ""
    if jobs_cmds and "export" in jobs_cmds[0]:
        export_path = jobs_cmds[0].split("/")[0].split(" ")[1]
        jobs_cmds = ["/".join(jobs_cmds[0].split("/")[1:])]

    ret_code = 1
    t_controller = TerminalController(jobs_cmds)
    an_input = ""

    if export_path:
        # If the path selected does not start from the user root, give relative location from terminal root
        if export_path[0] == "~":
            export_path = export_path.replace("~", USER_HOME.as_posix())
        elif export_path[0] != "/":
            export_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), export_path
            )

        # Check if the directory exists
        if os.path.isdir(export_path):
            console.print(
                f"Export data to be saved in the selected folder: '{export_path}'"
            )
        else:
            os.makedirs(export_path)
            console.print(
                f"[green]Folder '{export_path}' successfully created.[/green]"
            )
        obbff.EXPORT_FOLDER_PATH = export_path

    bootup()
    if not jobs_cmds:
        welcome_message()
        t_controller.print_help()
        check_for_updates()

    env_files = [f for f in os.listdir() if f.endswith(".env")]
    if env_files:
        global env_file
        env_file = env_files[0]
        dotenv.load_dotenv(env_file)
    else:
        # create env file
        Path(".env")

    while ret_code:
        if obbff.ENABLE_QUICK_EXIT:
            console.print("Quick exit enabled")
            break

        # There is a command in the queue
        if t_controller.queue and len(t_controller.queue) > 0:
            # If the command is quitting the menu we want to return in here
            if t_controller.queue[0] in ("q", "..", "quit"):
                print_goodbye()
                break

            # Consume 1 element from the queue
            an_input = t_controller.queue[0]
            t_controller.queue = t_controller.queue[1:]

            # Print the current location because this was an instruction and we want user to know what was the action
            if an_input and an_input.split(" ")[0] in t_controller.CHOICES_COMMANDS:
                console.print(f"{get_flair()} / $ {an_input}")

        # Get input command from user
        else:
            # Get input from user using auto-completion
            if session and obbff.USE_PROMPT_TOOLKIT:
                try:
                    if obbff.TOOLBAR_HINT:
                        an_input = session.prompt(
                            f"{get_flair()} / $ ",
                            completer=t_controller.completer,
                            search_ignore_case=True,
                            bottom_toolbar=HTML(
                                '<style bg="ansiblack" fg="ansiwhite">[h]</style> help menu    '
                                '<style bg="ansiblack" fg="ansiwhite">[q]</style> return to previous menu    '
                                '<style bg="ansiblack" fg="ansiwhite">[e]</style> exit terminal    '
                                '<style bg="ansiblack" fg="ansiwhite">[cmd -h]</style> '
                                "see usage and available options    "
                                '<style bg="ansiblack" fg="ansiwhite">[about]</style> Getting Started Documentation'
                            ),
                            style=Style.from_dict(
                                {
                                    "bottom-toolbar": "#ffffff bg:#333333",
                                }
                            ),
                        )
                    else:
                        an_input = session.prompt(
                            f"{get_flair()} / $ ",
                            completer=t_controller.completer,
                            search_ignore_case=True,
                        )
                except (KeyboardInterrupt, EOFError):
                    print_goodbye()
                    break
            # Get input from user without auto-completion
            else:
                an_input = input(f"{get_flair()} / $ ")

        try:
            # Process the input command
            t_controller.queue = t_controller.switch(an_input)
            if an_input in ("q", "quit", "..", "exit"):
                print_goodbye()
                break

            # Check if the user wants to reset application
            if an_input in ("r", "reset") or t_controller.update_success:
                ret_code = reset(t_controller.queue if t_controller.queue else [])
                if ret_code != 0:
                    print_goodbye()
                    break

        except SystemExit:
            logger.exception(
                "The command '%s' doesn't exist on the / menu.",
                an_input,
            )
            console.print(
                f"\nThe command '{an_input}' doesn't exist on the / menu", end=""
            )
            similar_cmd = difflib.get_close_matches(
                an_input.split(" ")[0] if " " in an_input else an_input,
                t_controller.controller_choices,
                n=1,
                cutoff=0.7,
            )
            if similar_cmd:
                if " " in an_input:
                    candidate_input = (
                        f"{similar_cmd[0]} {' '.join(an_input.split(' ')[1:])}"
                    )
                    if candidate_input == an_input:
                        an_input = ""
                        t_controller.queue = []
                        console.print("\n")
                        continue
                    an_input = candidate_input
                else:
                    an_input = similar_cmd[0]

                console.print(f" Replacing by '{an_input}'.")
                t_controller.queue.insert(0, an_input)
            else:
                console.print("\n")


def insert_start_slash(cmds: List[str]) -> List[str]:
    if not cmds[0].startswith("/"):
        cmds[0] = f"/{cmds[0]}"
    if cmds[0].startswith("/home"):
        cmds[0] = f"/{cmds[0][5:]}"
    return cmds


def do_rollover():
    """RollOver the log file."""

    for handler in logging.getLogger().handlers:
        if isinstance(handler, PathTrackingFileHandler):
            handler.doRollover()


def log_settings() -> None:
    """Log settings"""
    settings_dict = {}
    settings_dict["tab"] = "True" if obbff.USE_TABULATE_DF else "False"
    settings_dict["cls"] = "True" if obbff.USE_CLEAR_AFTER_CMD else "False"
    settings_dict["color"] = "True" if obbff.USE_COLOR else "False"
    settings_dict["promptkit"] = "True" if obbff.USE_PROMPT_TOOLKIT else "False"
    settings_dict["predict"] = "True" if obbff.ENABLE_PREDICT else "False"
    settings_dict["thoughts"] = "True" if obbff.ENABLE_THOUGHTS_DAY else "False"
    settings_dict["reporthtml"] = "True" if obbff.OPEN_REPORT_AS_HTML else "False"
    settings_dict["exithelp"] = "True" if obbff.ENABLE_EXIT_AUTO_HELP else "False"
    settings_dict["rcontext"] = "True" if obbff.REMEMBER_CONTEXTS else "False"
    settings_dict["rich"] = "True" if obbff.ENABLE_RICH else "False"
    settings_dict["richpanel"] = "True" if obbff.ENABLE_RICH_PANEL else "False"
    settings_dict["ion"] = "True" if obbff.USE_ION else "False"
    settings_dict["watermark"] = "True" if obbff.USE_WATERMARK else "False"
    settings_dict["autoscaling"] = "True" if obbff.USE_PLOT_AUTOSCALING else "False"
    settings_dict["dt"] = "True" if obbff.USE_DATETIME else "False"
    settings_dict["packaged"] = "True" if obbff.PACKAGED_APPLICATION else "False"
    settings_dict["python"] = str(platform.python_version())
    settings_dict["os"] = str(platform.system())

    logger.info("SETTINGS: %s ", str(settings_dict))

    do_rollover()


def run_scripts(
    path: str,
    test_mode: bool = False,
    verbose: bool = False,
    routines_args: List[str] = None,
):
    """Runs a given .openbb scripts

    Parameters
    ----------
    path : str
        The location of the .openbb file
    test_mode : bool
        Whether the terminal is in test mode
    verbose : bool
        Whether to run tests in verbose mode
    routines_args : List[str]
        One or multiple inputs to be replaced in the routine and separated by commas. E.g. GME,AMC,BTC-USD
    """
    if os.path.isfile(path):
        with open(path) as fp:
            raw_lines = [x for x in fp if (not is_reset(x)) and ("#" not in x) and x]
            raw_lines = [
                raw_line.strip("\n") for raw_line in raw_lines if raw_line.strip("\n")
            ]

            if routines_args:
                lines = list()
                for rawline in raw_lines:
                    templine = rawline
                    for i, arg in enumerate(routines_args):
                        templine = templine.replace(f"$ARGV[{i}]", arg)
                    lines.append(templine)
            else:
                lines = raw_lines

            if test_mode and "exit" not in lines[-1]:
                lines.append("exit")

            export_folder = ""
            if "export" in lines[0]:
                export_folder = lines[0].split("export ")[1].rstrip()
                lines = lines[1:]

            simulate_argv = f"/{'/'.join([line.rstrip() for line in lines])}"
            file_cmds = simulate_argv.replace("//", "/home/").split()
            file_cmds = insert_start_slash(file_cmds) if file_cmds else file_cmds
            if export_folder:
                file_cmds = [f"export {export_folder}{' '.join(file_cmds)}"]
            else:
                file_cmds = [" ".join(file_cmds)]

            if not test_mode:
                terminal(file_cmds, appName="openbb_script")
                # TODO: Add way to track how many commands are tested
            else:
                if verbose:
                    terminal(file_cmds, appName="openbb_script")
                else:
                    with suppress_stdout():
                        terminal(file_cmds, appName="openbb_script")

    else:
        console.print(f"File '{path}' doesn't exist. Launching base terminal.\n")
        if not test_mode:
            terminal()


def main(
    debug: bool,
    test: bool,
    filtert: str,
    paths: List[str],
    verbose: bool,
    routines_args: List[str] = None,
):
    """
    Runs the terminal with various options

    Parameters
    ----------
    debug : bool
        Whether to run the terminal in debug mode
    test : bool
        Whether to run the terminal in integrated test mode
    filtert : str
        Filter test files with given string in name
    paths : List[str]
        The paths to run for scripts or to test
    verbose : bool
        Whether to show output from tests
    routines_args : List[str]
        One or multiple inputs to be replaced in the routine and separated by commas. E.g. GME,AMC,BTC-USD
    """

    if test:
        os.environ["DEBUG_MODE"] = "true"

        if paths == []:
            console.print("Please send a path when using test mode")
            return
        test_files = []
        for path in paths:
            if path.endswith(".openbb"):
                file = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
                test_files.append(file)
            else:
                folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
                files = [
                    f"{folder}/{name}"
                    for name in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, name))
                    and name.endswith(".openbb")
                    and (filtert in f"{folder}/{name}")
                ]
                test_files += files
        test_files.sort()
        SUCCESSES = 0
        FAILURES = 0
        fails = {}
        length = len(test_files)
        i = 0
        console.print("[green]OpenBB Terminal Integrated Tests:\n[/green]")
        for file in test_files:
            file = file.replace("//", "/")
            repo_path_position = file.rfind(REPO_DIR.name)
            if repo_path_position >= 0:
                file_name = file[repo_path_position:].replace("\\", "/")
            else:
                file_name = file
            console.print(f"{file_name}  {((i/length)*100):.1f}%")
            try:
                if not os.path.isfile(file):
                    raise ValueError("Given file does not exist")
                run_scripts(file, test_mode=True, verbose=verbose)
                SUCCESSES += 1
            except Exception as e:
                fails[file] = e
                FAILURES += 1
            i += 1
        if fails:
            console.print("\n[red]Failures:[/red]\n")
            for key, value in fails.items():
                repo_path_position = key.rfind(REPO_DIR.name)
                if repo_path_position >= 0:
                    file_name = key[repo_path_position:].replace("\\", "/")
                else:
                    file_name = key
                logger.error("%s: %s failed", file_name, value)
                console.print(f"{file_name}: {value}\n")
        console.print(
            f"Summary: [green]Successes: {SUCCESSES}[/green] [red]Failures: {FAILURES}[/red]"
        )
    else:
        if debug:
            os.environ["DEBUG_MODE"] = "true"
        if isinstance(paths, list) and paths[0].endswith(".openbb"):
            run_scripts(paths[0], routines_args=routines_args)
        elif paths:
            argv_cmds = list([" ".join(paths).replace(" /", "/home/")])
            argv_cmds = insert_start_slash(argv_cmds) if argv_cmds else argv_cmds
            terminal(argv_cmds)
        else:
            terminal()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="terminal",
        description="The gamestonk terminal.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Runs the terminal in debug mode.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="The path or .openbb file to run.",
        dest="path",
        nargs="+",
        default="",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="test",
        action="store_true",
        default=False,
        help="Whether to run in test mode.",
    )
    parser.add_argument(
        "--filter",
        help="Send a keyword to filter in file name",
        dest="filtert",
        default="",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Select multiple inputs to be replaced in the routine and separated by commas. E.g. GME,AMC,BTC-USD",
        dest="routine_args",
        type=lambda s: [str(item) for item in s.split(",")],
        default=None,
    )

    if sys.argv[1:] and "-" not in sys.argv[1][0]:
        sys.argv.insert(1, "-f")
    ns_parser = parser.parse_args()
    main(
        ns_parser.debug,
        ns_parser.test,
        ns_parser.filtert,
        ns_parser.path,
        ns_parser.verbose,
        ns_parser.routine_args,
    )
