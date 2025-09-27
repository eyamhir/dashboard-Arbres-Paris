import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ---------- 1. Définir le chemin sécurisé du CSV ----------
CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "arbres_enriched.csv")

# Vérifier que le fichier existe
if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"Le fichier {CSV_FILE} est introuvable !")

# ---------- 2. Charger les données ----------
df = pd.read_csv(CSV_FILE)
print("Colonnes disponibles :", list(df.columns))

# Remplacer les NaN dans 'com_adresse' et 'arbres_espece' par une valeur vide
df["com_adresse"] = df["com_adresse"].fillna("Inconnu")
df["arbres_espece"] = df["arbres_espece"].fillna("Inconnu")

# ---------- 3. Initialiser l'app Dash ----------
app = dash.Dash(__name__)

# Dropdown options
species_options = [{"label": s, "value": s} for s in sorted(df["arbres_espece"].unique())]
address_options = [{"label": a, "value": a} for a in sorted(df["com_adresse"].unique())]

# ---------- 4. Layout ----------
app.layout = html.Div([
    html.H1("Dashboard Arbres Paris"),

    html.Div([
        html.Label("Filtrer par espèce"),
        dcc.Dropdown(id="species-dropdown", options=species_options, multi=True),
        html.Label("Filtrer par adresse"),
        dcc.Dropdown(id="address-dropdown", options=address_options, multi=True),
    ], style={"width": "40%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        dcc.Graph(id="scatter-size-score"),
        dcc.Graph(id="hist-size"),
    ], style={"width": "55%", "display": "inline-block"}),

    html.H2("Top 10 espèces"),
    html.Div(id="top-species-table"),

    html.H2("Top 10 adresses"),
    html.Div(id="top-address-table")
])

# ---------- 5. Callback ----------
@app.callback(
    Output("scatter-size-score", "figure"),
    Output("hist-size", "figure"),
    Output("top-species-table", "children"),
    Output("top-address-table", "children"),
    Input("species-dropdown", "value"),
    Input("address-dropdown", "value"),
)
def update_dashboard(selected_species, selected_address):
    dff = df.copy()
    if selected_species:
        dff = dff[dff["arbres_espece"].isin(selected_species)]
    if selected_address:
        dff = dff[dff["com_adresse"].isin(selected_address)]

    # Scatter taille vs score
    scatter_fig = px.scatter(
        dff,
        x="size_raw",
        y="conservation_score",
        color="rarity_norm",
        hover_data=["arbres_espece", "com_adresse"],
        color_continuous_scale="Viridis",
        title="Taille vs Conservation Score (coloré par rareté)"
    )

    # Histogramme des tailles
    hist_fig = px.histogram(dff, x="size_raw", nbins=20, title="Distribution des tailles d'arbres")

    # Top espèces
    top_species = dff.groupby("arbres_espece").size().sort_values(ascending=False).head(10).reset_index()
    top_species.columns = ["Espèce", "Nombre"]
    species_table = html.Table([
        html.Tr([html.Th(col) for col in top_species.columns])] +
        [html.Tr([html.Td(top_species.iloc[i][col]) for col in top_species.columns]) for i in range(len(top_species))]
    )

    # Top adresses
    top_address = dff.groupby("com_adresse").size().sort_values(ascending=False).head(10).reset_index()
    top_address.columns = ["Adresse", "Nombre"]
    address_table = html.Table([
        html.Tr([html.Th(col) for col in top_address.columns])] +
        [html.Tr([html.Td(top_address.iloc[i][col]) for col in top_address.columns]) for i in range(len(top_address))]
    )

    return scatter_fig, hist_fig, species_table, address_table

# ---------- 6. Lancer l'app ----------
if __name__ == "__main__":
    app.run(debug=True)
