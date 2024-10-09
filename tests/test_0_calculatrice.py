import pytest
from src.tp_0_calculatrice import Calculatrice


@pytest.fixture
def calc():
    """Fixture pour initialiser une instance de la calculatrice."""
    return Calculatrice()


def test_add(calc):
    pass

def test_subtract(calc):
    pass

def test_multiply(calc):
    pass

def test_divide(calc):
    pass
