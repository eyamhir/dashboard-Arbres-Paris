import requests
import json
import os

# Paramètres
DATASET = "arbresremarquablesparis"
BASE_URL = "https://opendata.paris.fr/api/records/1.0/search/"
ROWS = 100  # maximum autorisé par requête

def fetch_data():
    all_records = []
    start = 0

    while True:
        params = {
            "dataset": DATASET,
            "rows": ROWS,
            "start": start
        }
        r = requests.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()

        records = data.get("records", [])
        all_records.extend(records)

        if len(records) < ROWS:
            break
        start += ROWS

    # sauvegarder en JSON
    os.makedirs("data", exist_ok=True)
    with open("data/arbres.json", "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"{len(all_records)} enregistrements sauvegardés dans data/arbres.json")

if __name__ == "__main__":
    fetch_data()
