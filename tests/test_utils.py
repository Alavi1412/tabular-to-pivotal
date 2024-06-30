from tabular_to_pivotal.utils import generate_start_and_end_from_shorthand


def test_generate_start_and_end_from_shorthand():
    shorthand = "Cal-23"
    start, end = generate_start_and_end_from_shorthand(shorthand)
    assert start == "01-01-2023"
    assert end == "31-12-2023"

    shorthand = "Feb-23"
    start, end = generate_start_and_end_from_shorthand(shorthand)
    assert start == "01-02-2023"
    assert end == "28-02-2023"
