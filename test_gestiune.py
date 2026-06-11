import os
import json
import pytest
from unittest.mock import patch
import gestiune_pacienti

# Fișier temporar folosit exclusiv pentru teste
TEST_FILE = "pacienti_test.json"

@pytest.fixture(autouse=True)
def configurare_si_curatare_teste():
    """
    Fixture care rulează înainte și după fiecare test.
    Redirecționează fișierul de producție către cel de test și îl șterge la final.
    """
    # Redirecționăm constanta din scriptul original către fișierul de test
    gestiune_pacienti.FISIER_PACIENTI = TEST_FILE
    
    # Ne asigurăm că pornim de la zero
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
        
    yield  # Aici se execută testul propriu-zis
    
    # Curățenie după rularea testului
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_valideaza_data():
    """Testează validarea formatului de dată."""
    assert gestiune_pacienti.valideaza_data("2026-06-10") is True
    assert gestiune_pacienti.valideaza_data("10-06-2026") is False
    assert gestiune_pacienti.valideaza_data("invalid-date") is False


def test_calculeaza_varsta():
    """Testează calculul vârstei."""
    # Testăm un caz stabil (pentru format greșit)
    assert gestiune_pacienti.calculeaza_varsta("format-gresit") == "N/A"
    
    # Test pentru o dată validă (ajustează logic dacă vrei test exact pe an curent)
    # Ex: Cineva născut în 2000 va avea în jur de 26 de ani în 2026
    varsta = gestiune_pacienti.calculeaza_varsta("2000-01-01")
    assert isinstance(varsta, int)
    assert varsta >= 0


def test_genereaza_id_unic():
    """Testează incrementarea automată a ID-urilor."""
    lista_goala = []
    assert gestiune_pacienti.genereaza_id_unic(lista_goala) == 101
    
    lista_existenta = [{"id": 101}, {"id": 105}]
    assert gestiune_pacienti.genereaza_id_unic(lista_existenta) == 106


@patch('builtins.input')
def test_adauga_pacient(mock_input):
    """
    Testează adăugarea unui pacient simulând introducerea datelor de la tastatură.
    Mock-ul va oferi răspunsurile în ordine.
    """
    # Intrări simulate: Nume, Prenume, Data nașterii, Alergii, Diagnostic
    mock_input.side_effect = ["Popescu", "Ion", "1990-05-14", "Polen, Aspirină", "Hipertensiune"]
    
    gestiune_pacienti.adauga_pacient()
    
    # Citim fișierul generat să vedem dacă s-a salvat corect
    pacienti = gestiune_pacienti.incarcă_pacienti()
    assert len(pacienti) == 1
    assert pacienti[0]["nume"] == "Popescu"
    assert pacienti[0]["prenume"] == "Ion"
    assert "Polen" in pacienti[0]["alergii"]
    assert "Hipertensiune" in pacienti[0]["istoric_diagnostic"]


@patch('builtins.input')
def test_actualizeaza_fisa_medicala(mock_input):
    """Testează adăugarea unui diagnostic nou la un pacient existent."""
    # Creăm un pacient de test direct în fișier
    pacient_initial = [{
        "id": 101,
        "nume": "Ionescu",
        "prenume": "Ana",
        "data_nasterii": "1985-08-20",
        "alergii": [],
        "istoric_diagnostic": ["Gripă"]
    }]
    gestiune_pacienti.salveaza_pacienti(pacient_initial)
    
    # Intrări simulate: ID pacient (101), Opțiune (1 - Diagnostic), Noul Diagnostic
    mock_input.side_effect = ["101", "1", "Diabet Tip 2"]
    
    gestiune_pacienti.actualizeaza_fisa_medicala()
    
    # Verificăm actualizarea
    pacienti_updatat = gestiune_pacienti.incarcă_pacienti()
    assert "Diabet Tip 2" in pacienti_updatat[0]["istoric_diagnostic"]