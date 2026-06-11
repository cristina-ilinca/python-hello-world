import json
import os
from datetime import datetime, timedelta

FISIER_MEDICAMENTE = "medicamente.json"
LIMITA_STOC_CRITIC = 10
ZILE_PANA_LA_EXPIRARE = 30


def incarca_medicamente():
    if not os.path.exists(FISIER_MEDICAMENTE):
        return []
    try:
        with open(FISIER_MEDICAMENTE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def salveaza_medicamente(lista_medicamente):
    try:
        with open(FISIER_MEDICAMENTE, "w", encoding="utf-8") as f:
            json.dump(lista_medicamente, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Eroare la salvarea stocului: {e}")


def verifica_alerte_stoc(lista_medicamente):
    print("\n=== 🔔 SISTEM AUTOMAT DE ALERTE FARMACIE ===")
    astazi = datetime.today()
    limita_expirare = astazi + timedelta(days=ZILE_PANA_LA_EXPIRARE)
    are_alerte = False

    for med in lista_medicamente:
        alerta_text = []
        if med["cantitate"] <= LIMITA_STOC_CRITIC:
            alerta_text.append(
                f"STOC CRITIC ({med['cantitate']} {med['forma']} rămase)"
            )

        try:
            data_exp = datetime.strptime(med["data_expirare"], "%Y-%m-%d")
            if data_exp <= astazi:
                alerta_text.append("❌ EXPIRAT!")
            elif data_exp <= limita_expirare:
                alerta_text.append(f"Expiră curând ({med['data_expirare']})")
        except ValueError:
            alerta_text.append("Dată expirare invalidă")

        if alerta_text:
            are_alerte = True
            print(
                f"⚠️ [ {med['denumire']} {med['concentratie']} ({med['forma']}) ] -> {' | '.join(alerta_text)}"
            )

    if not are_alerte:
        print("✅ Toate stocurile și termenele de valabilitate sunt optime.")
    print("=" * 43)


def adauga_sau_suplimenteaza_medicament():
    print("\n--- Adăugare / Suplimentare Medicament ---")
    lista_medicamente = incarca_medicamente()

    denumire = input("Denumire comercială (ex: Augmentin): ").strip()
    concentratie = input("Concentrație (ex: 100mg): ").strip()

    print(
        "Forma de prezentare (Alege cifră: 1-Fiolă, 2-Tabletă, 3-Capsulă, 4-Sirop): "
    )
    opt_forma = input("> ").strip()
    forme_dict = {"1": "Fiolă", "2": "Tabletă", "3": "Capsulă", "4": "Sirop"}
    forma = forme_dict.get(opt_forma, "Altceva")

    medicament_existent = None
    for med in lista_medicamente:
        if (
            med["denumire"].lower() == denumire.lower()
            and med["concentratie"].lower() == concentratie.lower()
            and med["forma"].lower() == forma.lower()
        ):
            medicament_existent = med
            break

    try:
        cantitate = int(input(f"Cantitate de adăugat în stoc ({forma}e): "))
        if cantitate <= 0:
            print("❌ Cantitatea trebuie să fie pozitivă.")
            return
    except ValueError:
        print("❌ Introdu un număr valid.")
        return

    if medicament_existent:
        # ⚠️ DEFECTUL 2: În loc de adunare (+=), am pus atribuire (=).
        # În loc să adauge lotul nou la cel vechi, sistemul va suprascrie stocul total cu valoarea introdusă acum.
        medicament_existent["cantitate"] = cantitate
        print(
            f"⚠️ [BUG ACTIVAT] Stocul pentru {medicament_existent['denumire']} a fost suprascris la doar {medicament_existent['cantitate']} buc. (stocul vechi s-a pierdut)!"
        )
    else:
        print("\n--- Atribute medicale noi sesizate ---")
        substanta = input("Substanța activă: ").strip()

        regim_input = (
            input("Este medicament cu regim special/narcotic? (da/nu): ")
            .strip()
            .lower()
        )
        regim_special = True if regim_input == "da" else False

        while True:
            data_exp = input("Data expirării (AAAA-LL-ZZ): ").strip()
            try:
                datetime.strptime(data_exp, "%Y-%m-%d")
                break
            except ValueError:
                print("❌ Format incorect! Folosește AAAA-LL-ZZ.")

        nou_medicament = {
            "denumire": denumire,
            "substanta_activa": substanta,
            "concentratie": concentratie,
            "forma": forma,
            "cantitate": cantitate,
            "data_expirare": data_exp,
            "regim_special": regim_special,
        }
        lista_medicamente.append(nou_medicament)
        print(f"✅ Medicamentul nou a fost înregistrat cu succes.")

    salveaza_medicamente(lista_medicamente)


def consuma_medicament():
    print("\n--- Consum / Eliberare Medicament (Prescripție) ---")
    lista_medicamente = incarca_medicamente()

    denumire = input("Denumire medicament: ").strip()
    concentratie = input("Concentrație (ex: 100mg): ").strip()

    med_gasit = None
    for med in lista_medicamente:
        if (
            med["denumire"].lower() == denumire.lower()
            and med["concentratie"].lower() == concentratie.lower()
        ):
            med_gasit = med
            break

    if not med_gasit:
        print(
            "❌ Medicamentul cu această concentrație nu a fost găsit în inventar."
        )
        return

    if med_gasit.get("regim_special", False):
        print(
            "⚠️ ATENȚIE: Acesta este un medicament cu REGIM SPECIAL (Narcotic/Psihotrop)!"
        )
        parola = input("Introdu codul de autorizare medic/farmacist: ")
        if parola != "HMS123":
            print("❌ Autorizare eșuată! Eliberarea a fost blocată.")
            return

    print(
        f"Disponibil: {med_gasit['cantitate']} x {med_gasit['forma']} ({med_gasit['substanta_activa']})"
    )
    try:
        cant_necesara = int(input("Cantitate necesară pentru eliberare: "))

        # ⚠️ DEFECTUL 1: Am eliminat complet validarea cantității!
        # Blocul de control care verifica dacă stocul e suficient (cant_necesara > cantitate) NU mai există.

        med_gasit["cantitate"] -= cant_necesara
        print(
            f"⚠️ [BUG ACTIVAT] Eliberat cu succes! Stoc rămas în JSON: {med_gasit['cantitate']} {med_gasit['forma']}e."
        )

        salveaza_medicamente(lista_medicamente)
    except ValueError:
        print("❌ Introdu un număr valid.")


def afiseaza_inventar():
    print("\n--- Inventar Detaliat Spital ---")
    lista_medicamente = incarca_medicamente()

    if not lista_medicamente:
        print("Inventarul este gol.")
        return

    print(
        f"{'Denumire':<15} | {'Subst. Activă':<15} | {'Conc.':<7} | {'Formă':<9} | {'Stoc':<6} | {'Regim Sp.':<10}"
    )
    print("-" * 75)
    for med in lista_medicamente:
        regim = "DA" if med.get("regim_special", False) else "NU"
        print(
            f"{med['denumire']:<15} | {med['substanta_activa']:<15} | {med['concentratie']:<7} | {med['forma']:<9} | {med['cantitate']:<6} | {regim:<10}"
        )
    print("-" * 75)


def meniu_stocuri():
    stoc_curent = incarca_medicamente()
    verifica_alerte_stoc(stoc_curent)

    while True:
        print("\n=== HMS - MANAGEMENT FARMACIE (VERSIUNE CU BUG-URI) ===")
        print("1. Afișare Inventar Detaliat")
        print("2. Adăugare / Suplimentare Stoc")
        print("3. Eliberare Medicament")
        print("4. Ieșire")

        optiune = input("Alege o opțiune: ").strip()
        if optiune == "1":
            afiseaza_inventar()
        elif optiune == "2":
            adauga_sau_suplimenteaza_medicament()
        elif optiune == "3":
            consuma_medicament()
        elif optiune == "4":
            break
        else:
            print("❌ Opțiune invalidă.")


if __name__ == "__main__":
    meniu_stocuri()