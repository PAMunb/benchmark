"""
this module contains useful methods used in other parts of the project
"""
from benchmark.shared.constants import DURATION_60M, DURATION_10M, DURATION_15M, DURATION_30M, DURATION_5M, DURATION_1M, FUZZING_TYPE_BLACKBOX_FUZZING, FUZZING_TYPE_DIRECTED_GREYBOX_FUZZING, FUZZING_TYPE_OTHER_DIRECTED_GREYBOX_FUZZING, FUZZING_TYPE_GENETIC_ALGORITHM_FUZZING, FUZZING_TYPE_GREYBOX_FUZZING, FUZZING_TYPE_MULTI_OBJECTIVE_GREYBOX_FUZZING, FUZZING_TYPE_DIRECTED_GREYBOX2_FUZZING, FUZZING_TYPE_ALT_GREYBOX_FUZZING, FUZZING_TYPE_ALT_DIRECTED_GREYBOX_FUZZING
from benchmark.shared.exceptions import InvalidDuration, InvalidFuzzingType


def validate_fuzzing_types(fuzzing_types: list) -> None:
    """validates the fuzzing type string
    """
    valid_values = [
        FUZZING_TYPE_BLACKBOX_FUZZING,
        FUZZING_TYPE_GREYBOX_FUZZING,
        FUZZING_TYPE_DIRECTED_GREYBOX_FUZZING,
        FUZZING_TYPE_OTHER_DIRECTED_GREYBOX_FUZZING,
        FUZZING_TYPE_DIRECTED_GREYBOX2_FUZZING,
        FUZZING_TYPE_ALT_GREYBOX_FUZZING,
        FUZZING_TYPE_ALT_DIRECTED_GREYBOX_FUZZING,
        FUZZING_TYPE_GENETIC_ALGORITHM_FUZZING,
        FUZZING_TYPE_MULTI_OBJECTIVE_GREYBOX_FUZZING
    ]
    for t in fuzzing_types:
        if t not in valid_values:
            raise InvalidFuzzingType("an invalid fuzzing type was provided")


def validate_duration(duration: str) -> None:
    """validates the duration string
    """
    valid_values = [
        DURATION_1M,
        DURATION_5M,
        DURATION_10M,
        DURATION_15M,
        DURATION_30M,
        DURATION_60M,
    ]
    if duration not in valid_values:
        raise InvalidDuration("an invalid duration was provided")
