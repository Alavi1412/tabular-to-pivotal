from tabular_to_pivotal import transformer
from tabular_to_pivotal.data_loader.data_loader_factory import DataLoaderFactory
from tabular_to_pivotal.data_loader.schemas import DataLoaderType


def load_and_transform(input_file: str, output_file: str, loader_type: DataLoaderType = DataLoaderType.CSV) -> None:
    data_loader = DataLoaderFactory.get_data_loader(loader_type)
    data = data_loader.load_data(input_file)
    data.enforce_publication_date_order()
    transformer.sort_and_save_pivot_data(data, output_file)
