import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from folium import LayerControl
import numpy as np
from sklearn.cluster import DBSCAN

# ---------- 1. Charger les données enrichies ----------
CSV_FILE = "data/arbres_enriched.csv"
GEOJSON_FILE = "data/arbres_enriched.geojson"

df = pd.read_csv(CSV_FILE)
gdf = gpd.read_file(GEOJSON_FILE)

print(f"Nombre total d'arbres : {len(df)}")
print("Colonnes disponibles :", list(df.columns))

# ---------- 2. Statistiques descriptives ----------
stats_features = ["size_raw","nn_dist_m","conservation_score"]
print("\nStatistiques descriptives :")
print(df[stats_features].describe())

# ---------- 3. Corrélations ----------
corr_matrix = df[stats_features].corr()
print("\nMatrice de corrélations :")
print(corr_matrix)

# ---------- 4. Analyse par espèce ----------
species_stats = df.groupby("arbres_espece").agg(
    count=("arbres_espece","count"),
    mean_size=("size_raw","mean"),
    mean_score=("conservation_score","mean")
).reset_index().sort_values("count", ascending=False)

print("\nTop 5 espèces par nombre d'arbres :")
print(species_stats.head())

# ---------- 5. Analyse par adresse (approx. arrondissement) ----------
arr_stats = df.groupby("com_adresse").agg(
    count=("arbres_espece","count"),
    mean_size=("size_raw","mean"),
    mean_score=("conservation_score","mean")
).reset_index().sort_values("count", ascending=False)

print("\nAdresses avec le plus d'arbres :")
print(arr_stats.head(10))

# ---------- 6. Export CSV ----------
species_stats.to_csv("data/stats_by_species.csv", index=False)
arr_stats.to_csv("data/stats_by_address.csv", index=False)
print("\nExport terminé : stats_by_species.csv et stats_by_address.csv")

# ---------- 7. Graphiques ----------
plt.figure(figsize=(8,5))
plt.hist(df["size_raw"], bins=20, color="green", alpha=0.7)
plt.title("Distribution des tailles d'arbres")
plt.xlabel("Taille (m)")
plt.ylabel("Nombre d'arbres")
plt.savefig("data/hist_taille_arbres.png")
plt.close()

plt.figure(figsize=(8,5))
plt.scatter(df["size_raw"], df["conservation_score"], alpha=0.6, c=df["nn_dist_m"], cmap="Reds")
plt.colorbar(label="Distance au voisin le plus proche (m)")
plt.title("Taille vs Conservation Score (coloré par isolement)")
plt.xlabel("Taille (m)")
plt.ylabel("Conservation Score")
plt.savefig("data/scatter_size_score.png")
plt.close()
print("Graphiques exportés : hist_taille_arbres.png, scatter_size_score.png")

# ---------- 8. Clustering DBSCAN pour détecter îlots et arbres isolés ----------
coords = np.vstack([ (geom.x, geom.y) for geom in gdf.geometry ])
db = DBSCAN(eps=50, min_samples=3).fit(coords)
gdf["cluster"] = db.labels_
df["cluster"] = gdf["cluster"]

# ---------- 9. Carte interactive Folium ----------
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Cluster global
marker_cluster = MarkerCluster(name="Tous les arbres").add_to(m)

# Définir couleur selon conservation et isolement
def marker_color(row):
    score = row['conservation_score']
    iso = row['nn_dist_m']
    if score > 0.7: return "darkgreen"
    elif score > 0.4: return "green"
    elif score > 0.2: return "orange"
    else: return "red"

gdf["marker_color"] = gdf.apply(marker_color, axis=1)

# Créer des sous-groupes par adresse
addresses = gdf['com_adresse'].unique()
addr_layers = {}
for addr in addresses:
    addr_layers[addr] = FeatureGroupSubGroup(marker_cluster, name=f"Adresse {addr}")
    m.add_child(addr_layers[addr])

# Ajouter arbres avec popup enrichi
for _, row in gdf.iterrows():
    popup_text = f"""
    <b>Nom : </b>{row.get('arbres_espece','')}<br>
    <b>Adresse : </b>{row.get('com_adresse','')}<br>
    <b>Taille : </b>{row.get('size_raw',0)} m<br>
    <b>Score conservation : </b>{row.get('conservation_score',0):.2f}<br>
    <b>Isolement : </b>{row.get('nn_dist_m',0):.1f} m<br>
    <b>Cluster ID : </b>{row.get('cluster',-1)}
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=row["marker_color"],
        fill=True,
        fill_color=row["marker_color"],
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(addr_layers[row['com_adresse']])

LayerControl(collapsed=False).add_to(m)
m.save("data/carte_arbres.html")
print("Carte interactive exportée : carte_arbres.html")
