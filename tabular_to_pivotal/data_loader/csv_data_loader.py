import csv
from typing import Dict, List

from pydantic import ValidationError

from tabular_to_pivotal.data_loader.data_loader_abstract import DataLoaderAbstract
from tabular_to_pivotal.exceptions import DataLoaderError
from tabular_to_pivotal.logger import get_logger
from tabular_to_pivotal.schemas import LoadedData, Quote

logger = get_logger(__name__)


class CSVDataLoader(DataLoaderAbstract):

    def load_data(self, file_path: str) -> LoadedData:
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file)
                raw_data = [self._map_row_to_dict(row) for row in csv_reader]
                normalized_data = self._normalize_data(raw_data)
                self.log_summary()
                return LoadedData(
                    quotes=normalized_data,
                    total_rows_count=self.total_rows_count,
                    valid_rows_count=self.valid_rows_count,
                    shorthands=self.shorthands,
                )
        except Exception as e:
            logger.error(f"Error loading CSV data: {e}")
            raise DataLoaderError(f"Failed to load data from {file_path}")

    def _map_row_to_dict(self, row: List[str]) -> Dict[str, str]:
        keys = ['publication_date', 'shorthand', 'start', 'end', 'price']
        if len(row) != len(keys):
            logger.warning(f"Skipping row with incorrect number of fields: {row}")
            return {}
        return {keys[i]: row[i] for i in range(len(keys))}

    def _normalize_data(self, data: List[Dict[str, str]]) -> List[Quote]:
        self.total_rows_count = len(data)
        valid_data = []
        for row in data:
            if not row:
                continue
            try:
                quote = Quote.model_validate(row)
                valid_data.append(quote)
                self.shorthands.add(quote.shorthand)
            except ValidationError as e:
                logger.warning(f"Skipping row due to validation error: {row} ({e})")
        self.valid_rows_count = len(valid_data)
        logger.info(
            f"Normalized {self.valid_rows_count} rows: Valid {self.valid_rows_count}, \
                Skipped {self.total_rows_count - self.valid_rows_count}"
        )
        return valid_data
