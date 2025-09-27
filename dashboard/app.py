# ---------- imports ----------
import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# ---------- 1. Charger le CSV (via variable d'environnement) ----------
DATA_FILE = os.getenv("DATA_FILE", "/app/data/arbres_enriched.csv")

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Le fichier {DATA_FILE} est introuvable !")

df = pd.read_csv(DATA_FILE)
df["com_adresse"] = df["com_adresse"].fillna("Inconnu")
df["arbres_espece"] = df["arbres_espece"].fillna("Inconnu")

# ---------- 2. Préparer les options dropdown ----------
species_options = [{"label": s, "value": s} for s in sorted(df["arbres_espece"].unique())]
address_options = [{"label": a, "value": a} for a in sorted(df["com_adresse"].unique())]

# ---------- 3. Initialiser l'app ----------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server  # <-- indispensable pour Gunicorn
app.title = "🌳 Dashboard Arbres Paris"

# ---------- 4. Layout ----------
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("🌳 Dashboard Arbres Paris", className="text-center mb-4"), width=12)),

    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total Arbres", className="text-secondary"), html.H3(id="total-trees")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Espèces uniques", className="text-secondary"), html.H3(id="unique-species")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Taille moyenne", className="text-secondary"), html.H3(id="avg-size")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Espèce la plus rare", className="text-secondary"), html.H3(id="rare-species")])), width=3),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Filtres"),
                dbc.CardBody([
                    html.Label("Filtrer par espèce"),
                    dcc.Dropdown(id="species-dropdown", options=species_options, multi=True, placeholder="Toutes les espèces"),
                    html.Br(),
                    html.Label("Filtrer par adresse"),
                    dcc.Dropdown(id="address-dropdown", options=address_options, multi=True, placeholder="Toutes les adresses"),
                ])
            ], className="mb-4 shadow"),
            width=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Visualisations"),
                dbc.CardBody([
                    dcc.Graph(id="scatter-size-score"),
                    dcc.Graph(id="hist-size"),
                    dcc.Graph(id="rarity-pie")
                ])
            ], className="mb-4 shadow"),
            width=8
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top 10 Espèces"),
                dbc.CardBody(dcc.Graph(id="top-species-bar"))
            ], className="mb-4 shadow"),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top 10 Adresses"),
                dbc.CardBody(dcc.Graph(id="top-address-bar"))
            ], className="mb-4 shadow"),
            width=6
        )
    ]),

    dbc.Row(
        dbc.Col(
            dbc.Button("📥 Télécharger CSV filtré", id="download-btn", color="success", className="mb-4"),
            width=3
        )
    )
], fluid=True)

# ---------- 5. Callback ----------
@app.callback(
    Output("scatter-size-score", "figure"),
    Output("hist-size", "figure"),
    Output("rarity-pie", "figure"),
    Output("top-species-bar", "figure"),
    Output("top-address-bar", "figure"),
    Output("total-trees", "children"),
    Output("unique-species", "children"),
    Output("avg-size", "children"),
    Output("rare-species", "children"),
    Input("species-dropdown", "value"),
    Input("address-dropdown", "value"),
)
def update_dashboard(selected_species, selected_address):
    dff = df.copy()

    # Filtrage
    if selected_species:
        dff = dff[dff["arbres_espece"].isin(selected_species)]
    if selected_address:
        dff = dff[dff["com_adresse"].isin(selected_address)]

    # Vérifier DataFrame vide
    if dff.empty:
        dff = df.copy()

    # Forcer colonnes numériques
    for col in ["size_raw", "conservation_score", "rarity_norm"]:
        if col in dff.columns:
            dff[col] = pd.to_numeric(dff[col], errors="coerce").fillna(0)
        else:
            dff[col] = 0

    # Scatter
    scatter_fig = px.scatter(
        dff, x="size_raw", y="conservation_score", color="rarity_norm",
        hover_data=["arbres_espece", "com_adresse"], color_continuous_scale="Viridis",
        title="Taille vs Conservation Score (coloré par rareté)"
    )
    scatter_fig.update_layout(hovermode="closest", template="plotly_dark")

    # Histogramme
    hist_fig = px.histogram(dff, x="size_raw", nbins=20, title="Distribution des tailles d'arbres", color_discrete_sequence=["#17BECF"])
    hist_fig.update_layout(template="plotly_dark")

    # Pie chart
    if "rarity_norm" in dff.columns and dff["rarity_norm"].notna().any():
        rarity_fig = px.pie(dff, names="rarity_norm", title="Répartition de la rareté", color_discrete_sequence=px.colors.sequential.Viridis)
        rarity_fig.update_traces(textposition='inside', textinfo='percent+label')
    else:
        rarity_fig = px.pie(names=["Aucune donnée"], values=[1], title="Répartition de la rareté")
    rarity_fig.update_layout(template="plotly_dark")

    # Top espèces
    top_species = dff.groupby("arbres_espece").size().sort_values(ascending=False).head(10).reset_index()
    top_species.columns = ["Espèce", "Nombre"]
    top_species_fig = px.bar(top_species, x="Espèce", y="Nombre", text="Nombre", color="Nombre",
                             title="Top 10 espèces", color_continuous_scale=px.colors.sequential.Viridis)
    top_species_fig.update_traces(textposition='outside')
    top_species_fig.update_layout(template="plotly_dark")

    # Top adresses
    top_address = dff.groupby("com_adresse").size().sort_values(ascending=False).head(10).reset_index()
    top_address.columns = ["Adresse", "Nombre"]
    top_address_fig = px.bar(top_address, x="Adresse", y="Nombre", text="Nombre", color="Nombre",
                             title="Top 10 adresses", color_continuous_scale=px.colors.sequential.Viridis)
    top_address_fig.update_traces(textposition='outside')
    top_address_fig.update_layout(template="plotly_dark")

    # KPIs
    total_trees = len(dff)
    unique_species = dff["arbres_espece"].nunique()
    avg_size = round(dff["size_raw"].mean(), 2)

    if not dff.empty and "rarity_norm" in dff.columns and dff["rarity_norm"].notna().any():
        rare_species = dff.loc[dff["rarity_norm"].idxmax(), "arbres_espece"]
    else:
        rare_species = "Inconnu"

    return scatter_fig, hist_fig, rarity_fig, top_species_fig, top_address_fig, total_trees, unique_species, avg_size, rare_species

# ---------- 6. Lancer l'app pour tests locaux ----------
if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=8050, debug=debug_mode)
