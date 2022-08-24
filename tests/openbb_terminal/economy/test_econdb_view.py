# IMPORTATION THIRDPARTY
import pytest

# IMPORTATION INTERNAL
from openbb_terminal.economy import econdb_view


@pytest.mark.vcr
@pytest.mark.parametrize(
    "parameters, countries, start_date, end_date, convert_currency",
    [
        [["RGDP"], ["United States", "Germany"], "2020-01-01", "2020-10-02", False],
        [["EMP", "PPI"], ["France"], "2010-01-01", "2019-01-01", False],
        [["GDP", "RGDP"], ["Italy", "Netherlands"], "2016-01-01", "2016-10-10", False],
    ],
)
def test_show_macro_data(
    mocker, parameters, countries, start_date, end_date, convert_currency
):
    mocker.patch(target="openbb_terminal.helper_classes.TerminalStyle.visualize_output")
    econdb_view.show_macro_data(
        parameters, countries, start_date, end_date, convert_currency
    )


@pytest.mark.vcr
@pytest.mark.record_stdout
@pytest.mark.parametrize(
    "instruments, maturities, frequency, start_date, end_date",
    [
        [["nominal", "inflation"], ["3y", "5y"], "monthly", "2020-01-01", "2020-02-03"],
        [["nominal"], ["1m", "30y"], "annually", "2015-01-04", "2015-01-28"],
        [["average", "inflation"], ["3y", "5y"], "weekly", "2018-06-05", "2018-07-06"],
    ],
)
def test_show_treasuries(
    mocker, instruments, maturities, frequency, start_date, end_date
):
    mocker.patch(target="openbb_terminal.helper_classes.TerminalStyle.visualize_output")
    econdb_view.show_treasuries(
        instruments, maturities, frequency, start_date, end_date
    )


@pytest.mark.vcr
@pytest.mark.record_stdout
def test_show_treasury_maturities():
    econdb_view.show_treasury_maturities()
