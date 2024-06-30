from abc import ABC, abstractmethod

from tabular_to_pivotal.logger import get_logger
from tabular_to_pivotal.schemas import LoadedData


class DataLoaderAbstract(ABC):
    total_rows_count = 0
    valid_rows_count = 0
    shorthands = set()

    @abstractmethod
    def load_data(self, file_path: str) -> LoadedData:
        pass

    def log_summary(self):
        logger = get_logger(self.__class__.__name__)
        logger.info(
            f"Normalized {self.total_rows_count} rows: Valid {self.valid_rows_count}, \
                Skipped {self.total_rows_count - self.valid_rows_count}"
        )
