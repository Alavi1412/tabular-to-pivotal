import pytest

from tabular_to_pivotal.data_loader.csv_data_loader import CSVDataLoader
from tabular_to_pivotal.exceptions import DataLoaderError
from tabular_to_pivotal.schemas import LoadedData


def test_load_data():
    loader = CSVDataLoader()
    data: LoadedData = loader.load_data('tests/test_data.csv')
    assert isinstance(data, LoadedData)
    assert len(data.quotes) == 14


def test_load_data_with_invalid_file():
    loader = CSVDataLoader()
    with pytest.raises(DataLoaderError):
        loader.load_data('tests/invalid_file.csv')
