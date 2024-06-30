from tempfile import TemporaryDirectory

from tabular_to_pivotal import transformer
from tabular_to_pivotal.schemas import LoadedData, Quote


def test_transform():
    quotes = [
        Quote(publication_date='3-1-2023', shorthand='Feb-23', start='1-2-2023', end='28-2-2023', price=181),
        Quote(publication_date='3-1-2023', shorthand='Mar-23', start='1-3-2023', end='31-3-2023', price=179.5),
        Quote(publication_date='3-2-2023', shorthand='Mar-23', start='1-3-2023', end='31-3-2023', price=220.5),
    ]
    data = LoadedData(quotes=quotes, total_rows_count=2, valid_rows_count=2, shorthands={'Feb-23', 'Mar-23'})
    with TemporaryDirectory() as temp_dir:
        output_file = f'{temp_dir}/output.csv'
        transformer.sort_and_save_pivot_data(data, output_file)
        with open(output_file) as file:
            lines = file.readlines()
            assert len(lines) == 3
            assert lines[0].strip() == ',Feb-23,Mar-23'
            assert lines[1].strip() == '01/03/23,181,179.5'
            assert lines[2].strip() == '02/03/23,,220.5'
