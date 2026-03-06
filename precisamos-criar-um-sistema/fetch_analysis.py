import requests, json

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

crm = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Fix the type parameter - it's "properties" not "property"
print("=== EXTRACTION ===")
for draw_date in ["2026-01-17", "2026-02-21", "2025-12-17"]:
    for tp in ["properties", "vehicles"]:
        r = requests.get(f"{crm}/wallets/lottery/extraction?drawDate={draw_date}&type={tp}", headers=headers, timeout=15)
        print(f"\nGET extraction drawDate={draw_date}&type={tp}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                print(f"  Items: {len(data)}")
                if data:
                    print(f"  First item keys: {list(data[0].keys())}")
                    print(f"  First item: {json.dumps(data[0], ensure_ascii=False)[:500]}")
            elif isinstance(data, dict):
                print(f"  Keys: {list(data.keys())}")
                print(f"  Preview: {json.dumps(data, ensure_ascii=False)[:500]}")
        else:
            print(f"  Response: {r.text[:300]}")

print("\n\n=== ANALYSIS ===")
for draw_date in ["2026-01-17", "2026-02-21"]:
    for tp in ["properties", "vehicles"]:
        r = requests.get(f"{crm}/wallets/analysis?drawDate={draw_date}&type={tp}", headers=headers, timeout=15)
        print(f"\nGET analysis drawDate={draw_date}&type={tp}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                print(f"  Items: {len(data)}")
                if data:
                    print(f"  First item keys: {list(data[0].keys())}")
                    print(f"  First item: {json.dumps(data[0], ensure_ascii=False)[:500]}")
                    if len(data) > 1:
                        print(f"  Second item: {json.dumps(data[1], ensure_ascii=False)[:500]}")
            elif isinstance(data, dict):
                print(f"  Keys: {list(data.keys())}")
                print(f"  Preview: {json.dumps(data, ensure_ascii=False)[:800]}")
        else:
            print(f"  Response: {r.text[:300]}")

# Also test with range parameters
print("\n\n=== ANALYSIS WITH RANGE ===")
r = requests.get(
    f"{crm}/wallets/analysis?drawDate=2026-01-17&type=properties&minRange=0&maxRange=100",
    headers=headers, timeout=15
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Response: {json.dumps(data, ensure_ascii=False)[:1000]}")
else:
    print(f"Response: {r.text[:300]}")

# Get ALL wallets data
print("\n\n=== ALL WALLETS ===")
r = requests.get(f"{crm}/wallets?page=1&pageSize=100", headers=headers, timeout=15)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Total items: {data.get('totalItems')}")
    items = data.get('items', [])
    # Group by segment
    by_segment = {}
    for item in items:
        seg = item.get('quotaSegment', '?')
        if seg not in by_segment:
            by_segment[seg] = []
        by_segment[seg].append(item)

    for seg, seg_items in sorted(by_segment.items()):
        print(f"\n  Segment {seg}: {len(seg_items)} cotas")
        for item in seg_items[:3]:
            print(f"    Grupo: {item.get('quotaGroup')}, Cota: {item.get('quotaNumber')}, "
                  f"Credito: R$ {item.get('quotaCredit'):,.2f}, "
                  f"Contemplada: {item.get('quotaIsContemplated')}, "
                  f"Status: {item.get('quotaStatusName')}, "
                  f"Cliente: {item.get('customerName')}")

# Get bids config for multiple groups
print("\n\n=== BIDS CONFIG ===")
groups_to_check = ["12164", "12155", "12148", "1010", "860", "870", "1672"]
for g in groups_to_check:
    r = requests.get(f"{crm}/wallets/bids/config?groups={g}", headers=headers, timeout=15)
    print(f"\nBids config for group {g}: status={r.status_code}")
    if r.status_code == 200:
        data = r.json()
        if data:
            print(f"  Data: {json.dumps(data, ensure_ascii=False)[:500]}")
        else:
            print(f"  Empty response (no bid config)")
