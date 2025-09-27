# scripts/enrich_and_score.py
import json
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine

# ---------- paramètres ----------
ARBRE_JSON = "data/arbres.json"
OUT_CSV = "data/arbres_enriched.csv"
OUT_GEOJSON = "data/arbres_enriched.geojson"
DB_ENGINE_URL = "postgresql+psycopg2://eya:eyaeya@localhost:5432/paris_data"
EPSG_PROJECT = "EPSG:3857"  # projection métrique pour distances

# ---------- 1. charger arbres ----------
with open(ARBRE_JSON, "r", encoding="utf-8") as f:
    records = json.load(f)

rows = []
for r in records:
    fields = r.get("fields", {})
    # Priorité à geom_x_y
    coords = fields.get("geom_x_y")
    if coords:
        lat = coords[0]
        lon = coords[1]
    else:
        # fallback sur geometry.coordinates
        geom = r.get("geometry", {})
        c = geom.get("coordinates")
        if c:
            lon, lat = c[0], c[1]
        else:
            lat = lon = None
    fields["lat"] = lat
    fields["lon"] = lon
    rows.append(fields)

df = pd.DataFrame(rows)
df = df.dropna(subset=["lat", "lon"])

# ---------- 2. GeoDataFrame ----------
gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])], crs="EPSG:4326")
gdf = gdf.to_crs(EPSG_PROJECT)

# ---------- 3. rareté ----------
gdf["species_count"] = gdf.groupby("arbres_espece")["arbres_espece"].transform("count")
gdf["species_rarity"] = 1.0 / gdf["species_count"]

# ---------- 4. taille ----------
size_col = "arbres_hauteurenm"
gdf["size_raw"] = pd.to_numeric(gdf.get(size_col, 0), errors="coerce").fillna(0)

# ---------- 5. isolement ----------
coords_mat = np.vstack([ (geom.x, geom.y) for geom in gdf.geometry ])
nbrs = NearestNeighbors(n_neighbors=2, algorithm="ball_tree").fit(coords_mat)
distances, indices = nbrs.kneighbors(coords_mat)
gdf["nn_dist_m"] = distances[:,1]

# ---------- 6. features normalisées ----------
scaler = MinMaxScaler()
gdf["rarity_norm"] = scaler.fit_transform(gdf[["species_rarity"]])
gdf["size_norm"] = scaler.fit_transform(gdf[["size_raw"]])
gdf["isolation_norm"] = scaler.fit_transform(gdf[["nn_dist_m"]])

# ---------- 7. conservation_score ----------
w_rarity = 0.4
w_size = 0.3
w_isolation = 0.3

gdf["conservation_score"] = (
    w_rarity * gdf["rarity_norm"] +
    w_size * gdf["size_norm"] +
    w_isolation * gdf["isolation_norm"]
)
gdf["conservation_score"] = scaler.fit_transform(gdf[["conservation_score"]])

# ---------- 8. clustering ----------
coords = np.vstack([ (geom.x, geom.y) for geom in gdf.geometry ])
db = DBSCAN(eps=50, min_samples=3).fit(coords)
gdf["cluster"] = db.labels_

# ---------- 9. export ----------
out_cols = ["arbres_espece","arbres_genre","com_adresse","lat","lon",
            "species_count","rarity_norm","size_raw","size_norm",
            "nn_dist_m","isolation_norm","conservation_score","cluster"]
gdf[out_cols].to_csv(OUT_CSV, index=False)
gdf.to_file(OUT_GEOJSON, driver="GeoJSON")

# ---------- 10. optionnel : Postgres ----------
try:
    engine = create_engine(DB_ENGINE_URL)
    gdf[out_cols].to_sql("arbres_enriched", engine, if_exists="replace", index=False)
    print("Table 'arbres_enriched' écrite dans Postgres ✅")
except Exception as e:
    print("Écriture Postgres échouée :", e)

print("Export terminé :", OUT_CSV, OUT_GEOJSON)
