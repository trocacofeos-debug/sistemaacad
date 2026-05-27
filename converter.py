import json

with open("serviceAccountKey.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data))