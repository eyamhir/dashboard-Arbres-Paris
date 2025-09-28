import json
import psycopg2
from datetime import datetime

# connexion PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="paris_data",
    user="eya",
    password="eyaeya"
)
cursor = conn.cursor()

# charger le JSON
with open("/app/data/arbres.json", "r", encoding="utf-8") as f:
    records = json.load(f)

for rec in records:
    f = rec["fields"]
    genre = f.get("genre") or None
    espece = f.get("espece") or None
    adresse = f.get("adresse") or None
    arrondissement = f.get("arrondissement") or None

    # gérer la date
    date_str = f.get("dateplantation")
    if date_str:
        try:
            date_plantation = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            date_plantation = None
    else:
        date_plantation = None

    # gérer les coordonnées
    coords = f.get("geo_point_2d", [None, None])
    lat, lon = coords if coords else (None, None)

    cursor.execute("""
        INSERT INTO arbres_remarquables
        (genre, espece, adresse, arrondissement, date_plantation, geo_lat, geo_lon)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (genre, espece, adresse, arrondissement, date_plantation, lat, lon))

conn.commit()
cursor.close()
conn.close()

print("✅ Données insérées dans PostgreSQL")
