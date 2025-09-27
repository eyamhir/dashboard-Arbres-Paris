import json

with open("data/arbres.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Nombre d'enregistrements : {len(data)}")
print("Exemple du premier enregistrement :")
print(json.dumps(data[0], indent=4, ensure_ascii=False))
