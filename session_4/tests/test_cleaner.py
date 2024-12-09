import logging

import pytest

from cleaner import Cleaner
from data import TuplePropre, BienType


@pytest.fixture
def cleaner() -> Cleaner:
    return Cleaner(logging.getLogger())


def test_noop(cleaner: Cleaner) -> None:
    assert [] == cleaner.clean([])


def test_eq() -> None:
    assert TuplePropre(
        type_bien=BienType.Maison, prix=100, surface=200, pieces=6
    ) == TuplePropre(type_bien=BienType.Maison, prix=100, surface=200, pieces=6)
