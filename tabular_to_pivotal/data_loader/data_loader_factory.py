from tabular_to_pivotal.data_loader.csv_data_loader import CSVDataLoader
from tabular_to_pivotal.data_loader.data_loader_abstract import DataLoaderAbstract
from tabular_to_pivotal.exceptions import DataLoaderError


class DataLoaderFactory:

    @staticmethod
    def get_data_loader(loader_type: str) -> DataLoaderAbstract:
        if loader_type == 'csv':
            return CSVDataLoader()
        else:
            raise DataLoaderError(f"Data loader for type '{loader_type}' is not implemented")
