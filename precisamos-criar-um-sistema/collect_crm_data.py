import requests, json, time

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

crm = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Step 1: Get all draw dates
print("=== Collecting all draw dates ===")
r = requests.get(f"{crm}/wallets/lottery/draw-dates", headers=headers, timeout=15)
draw_dates = r.json()
print(f"Total draw dates: {len(draw_dates)}")

# Organize by type
prop_dates = sorted(set(d['drawDate'][:10] for d in draw_dates if d['type'] == 'properties'))
veh_dates = sorted(set(d['drawDate'][:10] for d in draw_dates if d['type'] == 'vehicles'))
print(f"Properties draw dates: {len(prop_dates)}")
print(f"Vehicles draw dates: {len(veh_dates)}")

# Step 2: Get lottery results for all dates
print("\n=== Collecting lottery results ===")
lottery_results = {}
all_dates = sorted(set(d['drawDate'][:10] for d in draw_dates))
for date in all_dates:
    r = requests.get(f"{crm}/wallets/lottery/results-by-draw-date?drawDate={date}", headers=headers, timeout=15)
    if r.status_code == 200:
        lottery_results[date] = r.json()
        prizes = r.json()
        print(f"  {date}: Prizes = {prizes.get('NO_Premio_1','?')}, {prizes.get('NO_Premio_2','?')}, {prizes.get('NO_Premio_3','?')}, {prizes.get('NO_Premio_4','?')}, {prizes.get('NO_Premio_5','?')}")
    time.sleep(0.3)

# Step 3: Get extraction data for all dates
print("\n=== Collecting extraction data ===")
extractions = {"properties": {}, "vehicles": {}}
for date in prop_dates:
    r = requests.get(f"{crm}/wallets/lottery/extraction?drawDate={date}&type=properties", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        # Count groups per category
        first_ext = data.get('extractionFirstNumber', {}).get('extraction', {})
        cats = {k: len(v.get('groups', [])) for k, v in first_ext.items()}
        print(f"  Properties {date}: categories={cats}")
        extractions['properties'][date] = data
    time.sleep(0.3)

for date in veh_dates:
    r = requests.get(f"{crm}/wallets/lottery/extraction?drawDate={date}&type=vehicles", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        first_ext = data.get('extractionFirstNumber', {}).get('extraction', {})
        cats = {k: len(v.get('groups', [])) for k, v in first_ext.items()}
        print(f"  Vehicles {date}: categories={cats}")
        extractions['vehicles'][date] = data
    time.sleep(0.3)

# Step 4: Get analysis for all dates
print("\n=== Collecting analysis data ===")
analyses = {"properties": {}, "vehicles": {}}
for date in prop_dates:
    r = requests.get(f"{crm}/wallets/analysis?drawDate={date}&type=properties", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"  Properties analysis {date}: {len(data)} cotas")
        analyses['properties'][date] = data
    time.sleep(0.3)

for date in veh_dates:
    r = requests.get(f"{crm}/wallets/analysis?drawDate={date}&type=vehicles", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"  Vehicles analysis {date}: {len(data)} cotas")
        analyses['vehicles'][date] = data
    time.sleep(0.3)

# Step 5: Get all wallets
print("\n=== Collecting all wallets ===")
all_wallets = []
page = 1
while True:
    r = requests.get(f"{crm}/wallets?page={page}&pageSize=100", headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        items = data.get('items', [])
        all_wallets.extend(items)
        total = data.get('totalItems', 0)
        print(f"  Page {page}: {len(items)} items (total: {total})")
        if len(all_wallets) >= total:
            break
        page += 1
    else:
        break
    time.sleep(0.3)

# Save everything
output = {
    "draw_dates": draw_dates,
    "lottery_results": lottery_results,
    "extractions": extractions,
    "analyses": analyses,
    "wallets": all_wallets,
}

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Draw dates: {len(draw_dates)}")
print(f"Lottery results: {len(lottery_results)}")
print(f"Property extractions: {len(extractions['properties'])}")
print(f"Vehicle extractions: {len(extractions['vehicles'])}")
print(f"Property analyses: {len(analyses['properties'])}")
print(f"Vehicle analyses: {len(analyses['vehicles'])}")
print(f"Wallets: {len(all_wallets)}")
print(f"\nSaved to dados_crm.json")
