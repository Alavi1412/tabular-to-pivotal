import csv
from datetime import datetime
from typing import Dict, List

from pydantic import ValidationError

from tabular_to_pivotal.data_loader.data_loader_abstract import DataLoaderAbstract
from tabular_to_pivotal.exceptions import DataLoaderError
from tabular_to_pivotal.logger import get_logger
from tabular_to_pivotal.schemas import LoadedData, Quote
from tabular_to_pivotal.utils import (
    generate_start_and_end_from_shorthand,
    validate_shorthand,
)

logger = get_logger(__name__)


class CSVDataLoader(DataLoaderAbstract):

    def load_data(self, file_path: str) -> LoadedData:
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file)
                raw_data = self._preprocess_data([row for row in csv_reader])
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

    def _preprocess_data(self, rows: List[List[str]]) -> List[Dict[str, str]]:
        return [self._map_row_to_dict(fixed_row) for row in rows for fixed_row in self._handle_broken_rows(row)]

    def _handle_broken_rows(self, row: List[str]) -> List[List[str]]:
        correct_items_per_row = 5

        if len(row) == correct_items_per_row:
            return [row]

        splitted_rows = self._split_row(row, correct_items_per_row)

        if self._are_all_rows_correct(splitted_rows):
            return splitted_rows

        return [
            self._maybe_add_start_and_end_dates(self._maybe_add_shorthand(split_row)) for split_row in splitted_rows
        ]

    def _maybe_add_shorthand(self, row: List[str]) -> List[str]:
        if len(row) == 4 and self._is_date_row(row[:3]):
            row.insert(1, self._generate_shorthand(row[1], row[2]))
        return row

    def _maybe_add_start_and_end_dates(self, row: List[str]) -> List[str]:
        if len(row) == 5:
            return row
        if self._is_valid_row(row[:2]):
            start_date, end_date = generate_start_and_end_from_shorthand(row[1])
            return [row[0], row[1], start_date, end_date, row[-1]]
        return row

    def _split_row(self, row: List[str], correct_items_per_row: int) -> List[List[str]]:
        return [row[i : i + correct_items_per_row] for i in range(0, len(row), correct_items_per_row)]  # noqa E203

    def _generate_shorthand(self, start_date: str, end_date: str) -> str:
        start_dt = datetime.strptime(start_date, '%d-%m-%Y')
        end_dt = datetime.strptime(end_date, '%d-%m-%Y')

        if start_dt.year == end_dt.year and start_dt.month == 1 and end_dt.month == 12 and end_dt.day == 31:
            return f"Cal-{start_dt.year % 100:02d}"
        return end_dt.strftime('%b-%y')

    def _are_all_rows_correct(self, rows: List[List[str]]) -> bool:
        return all(len(row) == 5 for row in rows)

    def _map_row_to_dict(self, row: List[str]) -> Dict[str, str]:
        keys = ['publication_date', 'shorthand', 'start', 'end', 'price']
        if len(row) != len(keys):
            logger.warning(f"Skipping row with incorrect number of fields: {row}")
            return {}
        return dict(zip(keys, row))

    def _normalize_data(self, data: List[Dict[str, str]]) -> List[Quote]:
        self.total_rows_count = len(data)
        valid_data = []
        for row in data:
            if row:
                try:
                    quote = Quote.model_validate(row)
                    valid_data.append(quote)
                    self.shorthands.add(quote.shorthand)
                except ValidationError as e:
                    logger.warning(f"Skipping row due to validation error: {row} ({e})")
        self.valid_rows_count = len(valid_data)
        logger.info(
            f"Normalized {self.valid_rows_count} rows: Valid {self.valid_rows_count}, "
            f"Skipped {self.total_rows_count - self.valid_rows_count}"
        )
        return valid_data

    def _is_date_row(self, row: List[str]) -> bool:
        try:
            for item in row:
                datetime.strptime(item, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def _is_valid_row(self, row: List[str]) -> bool:
        try:
            datetime.strptime(row[0], '%d-%m-%Y')
            validate_shorthand(row[1])
            return True
        except ValueError:
            return False
