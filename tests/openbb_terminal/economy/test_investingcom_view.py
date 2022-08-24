# IMPORTATION STANDARD
# import gzip

# IMPORTATION THIRDPARTY
# import pandas as pd

import datetime
import pytest

# IMPORTATION INTERNAL
from openbb_terminal.economy import investingcom_view


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_yieldcurve():
    investingcom_view.display_yieldcurve(country="portugal", export="")


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_display_economic_calendar():
    investingcom_view.display_economic_calendar(
        country="united states",
        importance="high",
        category="Employment",
        start_date=datetime.date(2022, 7, 7),
        end_date=datetime.date(2022, 7, 8),
    )
