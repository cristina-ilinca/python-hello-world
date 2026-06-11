from datetime import datetime
import json
import os

# Numele fișierului în care se vor salva datele
FISIER_PACIENTI = "pacienti.json"


def incarcă_pacienti():
    """Încarcă lista de pacienți din fișierul JSON."""
    if not os.path.exists(FISIER_PACIENTI):
        return []
    try:
        with open(FISIER_PACIENTI, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(
            "⚠️ Eroare la citirea fișierului JSON. S-a inițializat o listă goală."
        )
        return []


def salveaza_pacienti(lista_pacienti):
    """Salvează lista de pacienți în fișierul JSON."""
    try:
        with open(FISIER_PACIENTI, "w", encoding="utf-8") as f:
            json.dump(lista_pacienti, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Eroare la salvarea datelor: {e}")


def calculeaza_varsta(data_nasterii_str):
    """Calculează vârsta curentă în funcție de data nașterii (Format: AAAA-LL-ZZ)."""
    try:
        data_nasterii = datetime.strptime(data_nasterii_str, "%Y-%m-%d")
        astazi = datetime.today()
        varsta = (
            astazi.year
            - data_nasterii.year
            - (
                (astazi.month, astazi.day)
                < (data_nasterii.month, data_nasterii.day)
            )
        )
        return varsta
    except ValueError:
        return "N/A"


def genereaza_id_unic(lista_pacienti):
    """Generează un ID unic incrementat automat."""
    if not lista_pacienti:
        return 101  # Pornim de la ID-ul 101
    # Luăm cel mai mare ID existent și adăugăm 1
    return max(pacient["id"] for pacient in lista_pacienti) + 1


def valideaza_data(data_str):
    """Verifică dacă formatul datei introdus este corect (AAAA-LL-ZZ)."""
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# --- FUNCTIUNILE PRINCIPALE ---


def adauga_pacient():
    print("\n--- Adăugare Pacient Nou ---")
    lista_pacienti = incarcă_pacienti()

    nume = input("Nume: ").strip()
    prenume = input("Prenume: ").strip()

    # Validare dată naștere
    while True:
        data_nasterii = input("Data nașterii (AAAA-LL-ZZ): ").strip()
        if valideaza_data(data_nasterii):
            break
        print("❌ Format invalid! Introdu data sub forma AAAA-LL-ZZ (ex: 1990-05-14).")

    alergii_input = input(
        "Alergii (separate prin virgulă, sau lasă gol): "
    ).strip()
    alergii = (
        [a.strip() for a in alergii_input.split(",") if a.strip()]
        if alergii_input
        else []
    )

    diagnostic_initial = input("Diagnostic inițial (sau lasă gol): ").strip()
    istoric = [diagnostic_initial] if diagnostic_initial else []

    nou_pacient = {
        "id": genereaza_id_unic(lista_pacienti),
        "nume": nume,
        "prenume": prenume,
        "data_nasterii": data_nasterii,
        "alergii": alergii,
        "istoric_diagnostic": istoric,
    }

    lista_pacienti.append(nou_pacient)
    salveaza_pacienti(lista_pacienti)
    print(f"✅ Pacientul a fost adăugat cu succes! ID alocat: {nou_pacient['id']}")


def cauta_pacient():
    print("\n--- Căutare Pacient ---")
    lista_pacienti = incarcă_pacienti()

    print("1. Căutare după ID")
    print("2. Căutare după Nume/Prenume")
    optiune = input("Alege o opțiune de căutare: ").strip()

    rezultate = []

    if optiune == "1":
        try:
            cautat_id = int(input("Introdu ID-ul pacientului: "))
            rezultate = [p for p in lista_pacienti if p["id"] == cautat_id]
        except ValueError:
            print("❌ ID-ul trebuie să fie un număr.")
            return
    elif optiune == "2":
        termen = input("Introdu numele sau prenumele: ").lower().strip()
        rezultate = [
            p
            for p in lista_pacienti
            if termen in p["nume"].lower() or termen in p["prenume"].lower()
        ]
    else:
        print("❌ Opțiune invalidă.")
        return

    if not rezultate:
        print("🔍 Nu s-a găsit niciun pacient cu datele introduse.")
    else:
        print(f"\n🔍 S-au găsit {len(rezultate)} rezultate:")
        for p in rezultate:
            varsta_calculata = calculeaza_varsta(p["data_nasterii"])
            print("-" * 40)
            print(f"ID: {p['id']}")
            print(f"Nume complet: {p['nume']} {p['prenume']}")
            print(f"Data Nașterii: {p['data_nasterii']} ({varsta_calculata} ani)")
            print(f"Alergii: {', '.join(p['alergii']) if p['alergii'] else 'Niciuna'}")
            print(
                f"Istoric Medical: {', '.join(p['istoric_diagnostic']) if p['istoric_diagnostic'] else 'Niciun diagnostic înregistrat'}"
            )
        print("-" * 40)


def actualizeaza_fisa_medicala():
    print("\n--- Actualizare Fișă Medicală ---")
    lista_pacienti = incarcă_pacienti()

    try:
        cautat_id = int(input("Introdu ID-ul pacientului pentru actualizare: "))
    except ValueError:
        print("❌ ID-ul trebuie să fie un număr.")
        return

    # Găsim indexul pacientului în listă
    pacient_gasit = None
    for pacient in lista_pacienti:
        if pacient["id"] == cautat_id:
            pacient_gasit = pacient
            break

    if not pacient_gasit:
        print("❌ Pacientul cu acest ID nu a fost găsit.")
        return

    print(
        f"Modifici fișa pentru: {pacient_gasit['nume']} {pacient_gasit['prenume']}"
    )
    print("1. Adaugă un nou diagnostic în istoric")
    print("2. Adaugă o nouă alergie")
    optiune = input("Alege ce vrei să modifici: ").strip()

    if optiune == "1":
        nou_diag = input("Introdu noul diagnostic: ").strip()
        if nou_diag:
            pacient_gasit["istoric_diagnostic"].append(nou_diag)
            print("✅ Diagnosticul a fost adăugat.")
    elif optiune == "2":
        noua_alergie = input("Introdu noua alergie: ").strip()
        if noua_alergie:
            pacient_gasit["alergii"].append(noua_alergie)
            print("✅ Alergia a fost adăugată.")
    else:
        print("❌ Opțiune invalidă.")
        return

    # Salvăm lista actualizată înapoi în fișier
    salveaza_pacienti(lista_pacienti)


# --- MENIUL PRINCIPAL ---


def meniu_principal():
    while True:
        print("\n=== SPITAL HMS - MODUL PACIENȚI ===")
        print("1. Adăugare pacient nou")
        print("2. Căutare pacient / Vizualizare fișă")
        print("3. Actualizare fișă medicală (Diagnostic/Alergii)")
        print("4. Ieșire")

        optiune = input("Alege o opțiune (1-4): ").strip()

        if optiune == "1":
            adauga_pacient()
        elif optiune == "2":
            cauta_pacient()
        elif optiune == "3":
            actualizeaza_fisa_medicala()
        elif optiune == "4":
            print("Sistemul se închide. La revedere!")
            break
        else:
            print("❌ Opțiune invalidă! Te rog introdu un număr între 1 și 4.")


if __name__ == "__main__":
    meniu_principal()