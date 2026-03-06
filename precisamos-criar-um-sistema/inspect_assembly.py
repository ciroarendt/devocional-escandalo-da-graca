import requests, json

# Re-fetch a recent assembly with full detail to inspect all fields
r = requests.get(
    "https://api.mktademicon.com.br/api/assembleias/?act=assembleias_newcon&param=01/2026",
    timeout=15
)
data = r.json()
print(f"Top-level keys: {list(data.keys())}")

for key in data.keys():
    val = data[key]
    if isinstance(val, list):
        print(f"\n--- {key}: list of {len(val)} items ---")
        if val:
            if isinstance(val[0], dict):
                print(f"  Item keys: {list(val[0].keys())}")
                for i, item in enumerate(val[:2]):
                    print(f"  Item {i}: {json.dumps(item, ensure_ascii=False)[:500]}")
            else:
                print(f"  First items: {val[:5]}")
    elif isinstance(val, dict):
        print(f"\n--- {key}: dict ---")
        print(f"  Keys: {list(val.keys())}")
        print(f"  Content: {json.dumps(val, ensure_ascii=False)[:500]}")
    else:
        print(f"\n--- {key}: {type(val).__name__} = {str(val)[:200]} ---")

# Also check if there's a different endpoint for veiculos with more data
print("\n\n=== VEICULOS 01/2026 ===")
r2 = requests.get(
    "https://api.mktademicon.com.br/api/assembleias/?act=assembleias_veiculos&param=01/2026",
    timeout=15
)
data2 = r2.json()
print(f"Top-level keys: {list(data2.keys())}")
for key in data2.keys():
    val = data2[key]
    if isinstance(val, list):
        print(f"\n--- {key}: list of {len(val)} items ---")
        if val:
            if isinstance(val[0], dict):
                print(f"  Item keys: {list(val[0].keys())}")
                for i, item in enumerate(val[:2]):
                    print(f"  Item {i}: {json.dumps(item, ensure_ascii=False)[:500]}")
    elif isinstance(val, dict):
        print(f"\n--- {key}: dict ---")
        print(f"  Content: {json.dumps(val, ensure_ascii=False)[:500]}")
