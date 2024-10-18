import pytest

def premier_paragraphe():
    return "1 kilomètre à pied, ça use, ça use,\n1 kilomètre à pied, ça use les souliers."


def test_premier_paragraphe():
    assert "1 kilomètre à pied, ça use, ça use,\n1 kilomètre à pied, ça use les souliers." == premier_paragraphe()