# IMPORTATION STANDARD
from pathlib import Path

# IMPORTATION THIRDPARTY
import pandas as pd
import pytest

# IMPORTATION INTERNAL
from openbb_terminal.helper_funcs import export_data

# pylint: disable=E1101
# pylint: disable=W0603
# pylint: disable=E1111
# pylint: disable=W0621
# pylint: disable=W0613


@pytest.fixture
def mock_compose_export_path(monkeypatch, tmp_path):
    # files in tmp_dir will remain (in separate folders) for 3 sequential runs of pytest
    def mock_return(func_name, *args, **kwargs):
        return tmp_path, f"{func_name}_20220829_235959"

    monkeypatch.setattr("openbb_terminal.helper_funcs.compose_export_path", mock_return)


@pytest.mark.parametrize(
    "export_type, dir_path, func_name, df",
    [
        (
            "csv",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "json",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "xlsx",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "png",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "jpg",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "pdf",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
        (
            "svg",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            pd.DataFrame(),
        ),
    ],
)
def test_export_data_filetypes(
    mock_compose_export_path, export_type, dir_path, func_name, df, tmp_path
):
    export_data(export_type, dir_path, func_name, df)

    assert Path(tmp_path / f"{func_name}_20220829_235959.{export_type}").exists()
    # TODO add assertions to check the validity of the files?


@pytest.mark.parametrize(
    "export_type, dir_path, func_name, data",
    [
        (
            # Dict instead of DataFrame
            "csv",
            "C:/openbb_terminal/common/behavioural_analysis",
            "queries",
            dict({"test": "dict"}),
        ),
    ],
)
def test_export_data_invalid_data(
    mock_compose_export_path, export_type, dir_path, func_name, data
):
    with pytest.raises(AttributeError):
        assert export_data(export_type, dir_path, func_name, data)
