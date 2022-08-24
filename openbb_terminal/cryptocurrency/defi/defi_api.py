"""Defi context API."""
import os
from openbb_terminal.helper_classes import ModelsNamespace as _models

# flake8: noqa
# pylint: disable=unused-import

# Menu commands
from .terramoney_fcd_view import display_account_staking_info as sinfo
from .terramoney_fcd_view import display_validators as validators
from .terramoney_fcd_view import display_account_growth as gacc
from .terramoney_fcd_view import display_staking_ratio_history as sratio
from .terramoney_fcd_view import display_staking_returns_history as sreturn
from .defipulse_view import display_defipulse as dpi
from .llama_view import display_grouped_defi_protocols as gdapps
from .llama_view import display_historical_tvl as dtvl
from .llama_view import display_defi_protocols as ldapps
from .llama_view import display_defi_tvl as stvl
from .substack_view import display_newsletters as newsletter
from .graph_view import display_uni_tokens as tokens
from .graph_view import display_uni_stats as stats
from .graph_view import display_recently_added as pairs
from .graph_view import display_uni_pools as pools
from .graph_view import display_last_uni_swaps as swaps
from .coindix_view import display_defi_vaults as vaults


# Models
models = _models(os.path.abspath(os.path.dirname(__file__)))
