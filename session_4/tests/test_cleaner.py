import pytest
import logging
from cleaner import ActualCleaner, Cleaner


@pytest.fixture
def cleaner() -> Cleaner:
    return ActualCleaner(logging.getLogger())


def test_noop(cleaner: ActualCleaner) -> None:
    assert [] == cleaner.clean([])
