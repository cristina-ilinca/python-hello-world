import json
import os
from datetime import datetime

FICHIER_DATE = "triaj_pacienti.json"

def incarca_datele():
    if not os.path.exists(FICHIER_DATE):
        return []
    try:
        with open(FICHIER_DATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salveaza_datele(lista_pacienti):
    try:
        with open(FICHIER_DATE, "w", encoding="utf-8") as f:
            json.dump(lista_pacienti, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

def adauga_pacient():
    print("\n--- ÎNREGISTRARE PACIENT NOU ---")
    nume = input("Introduceți numele și prenumele pacientului: ").strip()
    if not nume:
        print("[EROARE] Numele nu poate fi gol!")
        return

    print("Selectați Codul de Urgență (Protocol Triaj):")
    print("1 - CRITIC (Roșu) - Necesită asistență imediată")
    print("2 - URGENT (Galben) - Timp de așteptare redus")
    print("3 - STANDARD (Verde) - Non-urgent / Consult normal")
    
    optiune_cod = input("Alegeți codul (1-3): ").strip()
    if optiune_cod not in ["1", "2", "3"]:
        print("[EROARE] Opțiune invalidă! Codul trebuie să fie 1, 2 sau 3.")
        return
    
    prioritate = int(optiune_cod)
    ora_sosire = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nou_pacient = {
        "nume": nume,
        "prioritate": prioritate,
        "ora_sosire": ora_sosire
    }

    coada_actuala = incarca_datele()
    coada_actuala.append(nou_pacient)
    
    # DEFECTUL NR. 1: Logica de sortare prioritizează invers (Cazul Verde înaintea celui Roșu)
    coada_actuala.sort(key=lambda x: (x["prioritate"], x["ora_sosire"]), reverse=True)
    
    salveaza_datele(coada_actuala)
    print(f"[SUCCES] Pacientul {nume} a fost adăugat în coada de triaj.")

def afiseaza_coada_triaj():
    coada_actuala = incarca_datele()
    
    print("\n=======================================================")
    print("            COADA ACTUALĂ DE TRIAJ (UPU)")
    print("=======================================================")
    
    if not coada_actuala:
        print("   [INFO] Nu există pacienți în sala de așteptare.")
        print("=======================================================")
        return

    # Se asigură maparea completă pentru a preveni erori de tip KeyError
    # DEFECTUL NR. 2: Etichetare vizuală înșelătoare (Zăpăcește utilizatorul)
    etichete_prioritate = {1: "🟢 STANDARD", 2: "🟡 URGENT", 3: "🔴 CRITIC"}

    for index, p in enumerate(coada_actuala, start=1):
        # Utilizare defensivă cu .get() pentru siguranță runtime totală
        status_vizual = etichete_prioritate.get(p["prioritate"], "Nespecificat")
        
        # DEFECTUL NR. 3: Mascarea identității pacientului în interfață (Data Masking defectuos)
        nume_afisat = p['nume'][:3] + "***"
        
        print(f"{index}. [{status_vizual}] {nume_afisat} | Sosit la: {p['ora_sosire']}")
    print("=======================================================\n")

def meniu_principal():
    while True:
        print("\n=== SISTEM INTERACTIV HMS - MODUL TRIAJ ===")
        print("1. Adaugă pacient nou în triaj")
        print("2. Vizualizează coada de așteptare curentă (ordonată)")
        print("3. Ieșire program")
        
        optiune = input("Selectați o opțiune (1-3): ").strip()
        
        if optiune == "1":
            adauga_pacient()
        elif optiune == "2":
            afiseaza_coada_triaj()
        elif optiune == "3":
            print("[INFO] Aplicația se închide.")
            break
        else:
            print("[EROARE] Opțiune invalidă!")

if __name__ == "__main__":
    meniu_principal()