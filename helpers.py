import json
import os

def incarca_date(nume_fisier):
    """Încarcă datele dintr-un fișier JSON. Dacă nu există, returnează o listă goală."""
    if not os.path.exists(nume_fisier):
        return []
    with open(nume_fisier, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salveaza_date(nume_fisier, date):
    """Salvează datele în format JSON, frumos structurate (indented)."""
    with open(nume_fisier, "w", encoding="utf-8") as f:
        json.dump(date, f, indent=4, ensure_ascii=False)