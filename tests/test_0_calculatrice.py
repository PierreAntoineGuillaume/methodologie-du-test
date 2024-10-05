import pytest
from src.calculatrice import Calculatrice


@pytest.fixture
def calc():
    """Fixture pour initialiser une instance de la calculatrice."""
    return Calculatrice()


def test_add(calc):
    assert 4 == calc.add(1, 3)


def test_subtract(calc):
    assert 1 == calc.subtract(10, 3)


def test_multiply(calc):
    pass


def test_divide(calc):
    pass
