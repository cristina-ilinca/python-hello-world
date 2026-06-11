from helpers import incarca_date, salveaza_date

FISIER_SALOANE = "saloane.json"

def initializeaza_date_test():
    """Generează câteva saloane de test dacă fișierul JSON nu există."""
    saloane_initiale = [
        {"salon": 101, "sectie": "Cardiologie", "paturi_totale": 3, "paturi_ocupate": 2, "pacienti_internati": [101, 102]},
        {"salon": 102, "sectie": "Chirurgie", "paturi_totale": 2, "paturi_ocupate": 2, "pacienti_internati": [103, 104]},
        {"salon": 103, "sectie": "Pediatrie", "paturi_totale": 4, "paturi_ocupate": 0, "pacienti_internati": []}
    ]
    if not incarca_date(FISIER_SALOANE):
        salveaza_date(FISIER_SALOANE, saloane_initiale)

def afiseaza_saloane():
    """Afișează situația curentă a saloanelor și disponibilitatea."""
    saloane = incarca_date(FISIER_SALOANE)
    print("\n=== STARE SALOANE ȘI DISPONIBILITATE ===")
    for s in saloane:
        locuri_libere = s["paturi_totale"] - s["paturi_ocupate"]
        print(f"Salon {s['salon']} [{s['sectie']}] -> Paturi: {s['paturi_ocupate']}/{s['paturi_totale']} ocupate (Libere: {locuri_libere})")
        if s["pacienti_internati"]:
            print(f"   > ID Pacienți internați: {s['pacienti_internati']}")
    print("=========================================\n")

def interneaza_pacient(id_pacient, sectie_dorita):
    """Logica de business: caută un pat liber pe secția cerută și ocupă-l."""
    saloane = incarca_date(FISIER_SALOANE)
    
    # Verificăm mai întâi dacă pacientul nu este deja internat undeva
    for s in saloane:
        if id_pacient in s["pacienti_internati"]:
            print(f"⚠️ Eroare: Pacientul cu ID {id_pacient} este deja internat în Salonul {s['salon']}!")
            return

    # Căutăm un salon cu locuri libere pe secția respectivă
    for s in saloane:
        if s["sectie"].lower() == sectie_dorita.lower():
            if s["paturi_ocupate"] < s["paturi_totale"]:
                # Modificăm datele în memorie
                s["paturi_ocupate"] += 1
                s["pacienti_internati"].append(id_pacient)
                
                # Salvăm în fișierul JSON
                salveaza_date(FISIER_SALOANE, saloane)
                print(f"✅ Succes! Pacientul {id_pacient} a fost internat în Salonul {s['salon']} ({s['sectie']}).")
                return
            
    print(f"❌ Ne pare rău! Nu mai există paturi libere pe secția {sectie_dorita}.")

def externeaza_pacient(id_pacient):
    """Eliberează un pat prin externarea pacientului după ID."""
    saloane = incarca_date(FISIER_SALOANE)
    
    for s in saloane:
        if id_pacient in s["pacienti_internati"]:
            s["pacienti_internati"].remove(id_pacient)
            s["paturi_ocupate"] -= 1
            
            salveaza_date(FISIER_SALOANE, saloane)
            print(f"✅ Succes! Pacientul {id_pacient} a fost externat din Salonul {s['salon']}.")
            return
            
    print(f"⚠️ Modul: Pacientul cu ID {id_pacient} nu a fost găsit ca fiind internat în niciun salon.")

# --- MENIUL INTERACTIV (Pentru rulare în VS Code) ---
def meniu():
    initializeaza_date_test()
    while True:
        print("\n--- SISTEM MANAGEMENT INTERNĂRI ---")
        print("1. Afișează starea saloanelor")
        print("2. Internează pacient")
        print("3. Externează pacient")
        print("4. Ieșire")
        
        optiune = input("Alegeți opțiunea: ")
        
        if optiune == "1":
            afiseaza_saloane()
        elif optiune == "2":
            try:
                id_p = int(input("Introduceți ID Pacient (ex: 105): "))
                sectie = input("Introduceți secția (Cardiologie/Chirurgie/Pediatrie): ")
                interneaza_pacient(id_p, sectie)
            except ValueError:
                print("❌ ID-ul trebuie să fie un număr valid!")
        elif optiune == "3":
            try:
                id_p = int(input("Introduceți ID Pacient pentru externare: "))
                externeaza_pacient(id_p)
            except ValueError:
                print("❌ ID-ul trebuie să fie un număr valid!")
        elif optiune == "4":
            print("Ieșire din modulul de internări...")
            break
        else:
            print("Opțiune invalidă!")

if __name__ == "__main__":
    meniu()