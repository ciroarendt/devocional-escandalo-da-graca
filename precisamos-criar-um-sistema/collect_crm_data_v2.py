import requests, json, time

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

crm = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Check if token is still valid
r = requests.get(f"{crm}/wallets?page=1&pageSize=1", headers=headers, timeout=15)
if r.status_code != 200:
    print(f"Token may be expired! Status: {r.status_code}")
    print("Attempting re-login...")
    # Re-login
    import subprocess
    subprocess.run(["python3", "/home/dev/workspace/precisamos-criar-um-sistema/login_get_token.py"], timeout=300)
    with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
        token = f.read().strip()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.get(f"{crm}/wallets?page=1&pageSize=1", headers=headers, timeout=15)
    print(f"After re-login: {r.status_code}")

print(f"Token valid: {r.status_code == 200}")

# Step 1: Get all draw dates
print("\n=== Collecting draw dates ===")
r = requests.get(f"{crm}/wallets/lottery/draw-dates", headers=headers, timeout=15)
draw_dates = r.json()
print(f"Total draw dates: {len(draw_dates)}")

prop_dates = sorted(set(d['drawDate'][:10] for d in draw_dates if d['type'] == 'properties'))
veh_dates = sorted(set(d['drawDate'][:10] for d in draw_dates if d['type'] == 'vehicles'))
print(f"Properties dates: {len(prop_dates)}")
print(f"Vehicles dates: {len(veh_dates)}")

# Step 2: Get lottery results - quick batch
print("\n=== Collecting lottery results ===")
lottery_results = {}
all_dates = sorted(set(d['drawDate'][:10] for d in draw_dates))
for i, date in enumerate(all_dates):
    try:
        r = requests.get(f"{crm}/wallets/lottery/results-by-draw-date?drawDate={date}", headers=headers, timeout=15)
        if r.status_code == 200 and r.text.strip():
            lottery_results[date] = r.json()
    except:
        pass
    if i % 50 == 0:
        print(f"  Progress: {i}/{len(all_dates)}")
    time.sleep(0.2)
print(f"  Collected {len(lottery_results)} lottery results")

# Step 3: Get extraction data - only recent (last 2 years)
print("\n=== Collecting extractions (recent) ===")
extractions = {"properties": {}, "vehicles": {}}

# Focus on last 2 years of data
recent_prop = [d for d in prop_dates if d >= "2024-01-01"]
recent_veh = [d for d in veh_dates if d >= "2024-01-01"]
print(f"Recent property dates: {len(recent_prop)}")
print(f"Recent vehicle dates: {len(recent_veh)}")

for date in recent_prop:
    try:
        r = requests.get(f"{crm}/wallets/lottery/extraction?drawDate={date}&type=properties", headers=headers, timeout=15)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
            first_ext = data.get('extractionFirstNumber', {}).get('extraction', {})
            total_groups = sum(len(v.get('groups', [])) for v in first_ext.values())
            print(f"  Properties {date}: {len(first_ext)} categories, {total_groups} groups")
            extractions['properties'][date] = data
        else:
            print(f"  Properties {date}: status={r.status_code}, empty={not r.text.strip()}")
    except Exception as e:
        print(f"  Properties {date}: error={e}")
    time.sleep(0.3)

for date in recent_veh:
    try:
        r = requests.get(f"{crm}/wallets/lottery/extraction?drawDate={date}&type=vehicles", headers=headers, timeout=15)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
            first_ext = data.get('extractionFirstNumber', {}).get('extraction', {})
            total_groups = sum(len(v.get('groups', [])) for v in first_ext.values())
            print(f"  Vehicles {date}: {len(first_ext)} categories, {total_groups} groups")
            extractions['vehicles'][date] = data
        else:
            print(f"  Vehicles {date}: status={r.status_code}, empty={not r.text.strip()}")
    except Exception as e:
        print(f"  Vehicles {date}: error={e}")
    time.sleep(0.3)

# Step 4: Get analysis for recent dates
print("\n=== Collecting analyses (recent) ===")
analyses = {"properties": {}, "vehicles": {}}
for date in recent_prop:
    try:
        r = requests.get(f"{crm}/wallets/analysis?drawDate={date}&type=properties", headers=headers, timeout=15)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
            print(f"  Properties analysis {date}: {len(data)} quotas")
            analyses['properties'][date] = data
    except Exception as e:
        print(f"  Properties analysis {date}: error={e}")
    time.sleep(0.3)

for date in recent_veh:
    try:
        r = requests.get(f"{crm}/wallets/analysis?drawDate={date}&type=vehicles", headers=headers, timeout=15)
        if r.status_code == 200 and r.text.strip():
            data = r.json()
            print(f"  Vehicles analysis {date}: {len(data)} quotas")
            analyses['vehicles'][date] = data
    except Exception as e:
        print(f"  Vehicles analysis {date}: error={e}")
    time.sleep(0.3)

# Step 5: Get all wallets
print("\n=== Collecting wallets ===")
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

print(f"\n{'='*60}")
print(f"RESUMO FINAL:")
print(f"  Draw dates: {len(draw_dates)}")
print(f"  Lottery results: {len(lottery_results)}")
print(f"  Property extractions: {len(extractions['properties'])}")
print(f"  Vehicle extractions: {len(extractions['vehicles'])}")
print(f"  Property analyses: {len(analyses['properties'])}")
print(f"  Vehicle analyses: {len(analyses['vehicles'])}")
print(f"  Wallets: {len(all_wallets)}")
print(f"\nSalvo em dados_crm.json")
