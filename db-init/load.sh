#!/bin/bash

echo "🔹 Step 1: Data retrieval"
python /app/scripts/data_retrieval.py

echo "🔹 Step 2: Load into PostgreSQL"
python /app/scripts/load_postgres.py

echo "🔹 Step 3: Enrich and score"
python /app/scripts/enrich_and_score.py

echo "🔹 Step 4: Inspect JSON"
python /app/scripts/inspect_json.py

echo "🔹 Step 5: Analyse arbres"
python /app/scripts/analyse_arbres.py

echo "✅ All scripts executed successfully!"
