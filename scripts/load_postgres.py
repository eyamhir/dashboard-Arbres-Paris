import json
import psycopg2

# connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="paris_data",
    user="eya",
    password="eyaeya"
)
cursor = conn.cursor()

# charger le JSON
with open("data/arbres.json", "r", encoding="utf-8") as f:
    records = json.load(f)

for rec in records:
    f = rec["fields"]
    genre = f.get("genre", "")
    espece = f.get("espece", "")
    adresse = f.get("adresse", "")
    arrondissement = f.get("arrondissement", "")
    date_plantation = f.get("dateplantation", "")
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
