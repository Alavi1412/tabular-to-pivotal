import csv
from typing import Dict

from tabular_to_pivotal.logger import get_logger
from tabular_to_pivotal.schemas import LoadedData

logger = get_logger(__name__)


def sort_and_save_pivot_data(data: LoadedData, output_file: str) -> None:
    pivot_data = _transform(data)
    try:
        with open(output_file, mode='w', newline='') as file:
            shorthands = data.get_sorted_shorthands()
            writer = csv.writer(file)
            writer.writerow([' '] + shorthands)
            for date, prices in sorted(pivot_data.items()):
                row = [date.strftime('%m/%d/%y')] + [prices.get(shorthand, '') for shorthand in shorthands]
                writer.writerow(row)
        logger.info(f"Saved pivot data to {output_file}")
    except Exception as e:
        logger.error(f"Error saving pivot data: {e}")
        raise


def _transform(data: LoadedData) -> Dict[str, Dict[str, float]]:
    pivot_data = {}
    for quote in data.quotes:
        publication_date = quote.publication_date
        shorthand = quote.shorthand
        price = quote.price
        if publication_date not in pivot_data:
            pivot_data[publication_date] = {}
        pivot_data[publication_date][shorthand] = price

    logger.debug(f"Transformed data to pivot format with {len(pivot_data)} publication dates")
    return pivot_data
