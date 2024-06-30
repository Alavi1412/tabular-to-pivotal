import re
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ValidationInfo, field_validator

from tabular_to_pivotal.utils import sort_shorthands


class Quote(BaseModel):
    publication_date: datetime
    shorthand: str
    start: datetime
    end: datetime
    price: Decimal

    @field_validator('publication_date', 'start', 'end', mode="before")
    @classmethod
    def validate_date(cls, value):
        try:
            return datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Date must be in the format DD-MM-YYYY')

    @field_validator('shorthand')
    @classmethod
    def validate_shorthand(cls, value):
        if re.match(r'^Cal-\d{2}$', value):
            return value
        try:
            datetime.strptime(value, '%b-%y')
        except ValueError:
            raise ValueError('Shorthand must be in the format Mon-YY')
        return value

    @field_validator('end')
    @classmethod
    def validate_end_after_start(cls, value: str, info: ValidationInfo):
        start = info.data.get('start')
        if start and value < start:
            raise ValueError(f'End date must be after start dat; start: {start}, end: {value}')
        return value


class LoadedData(BaseModel):
    quotes: list[Quote]
    total_rows_count: int
    valid_rows_count: int
    shorthands: set[str]

    def get_sorted_shorthands(self):
        return sort_shorthands(self.shorthands)
