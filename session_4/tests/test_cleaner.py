import pytest
import logging
from cleaner import Cleaner


@pytest.fixture
def cleaner() -> Cleaner:
    return Cleaner(logging.getLogger())


def test_noop(cleaner: Cleaner) -> None:
    assert [] == cleaner.clean([])
