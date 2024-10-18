import pytest

def premier_paragraphe():
    return "1 kilomètre à pied, ça use, ça use,\n1 kilomètre à pied, ça use les souliers."

def generer_paragraphe(kilometres):
    return f"{kilometres} kilomètres à pied, ça use, ça use,\n{kilometres} kilomètres à pied, ça use les souliers."

def test_premier_paragraphe():
    assert "1 kilomètre à pied, ça use, ça use,\n1 kilomètre à pied, ça use les souliers." == premier_paragraphe()

def test_generer_chanson():
    assert "5 kilomètres à pied, ça use, ça use,\n5 kilomètres à pied, ça use les souliers." == generer_paragraphe(5)