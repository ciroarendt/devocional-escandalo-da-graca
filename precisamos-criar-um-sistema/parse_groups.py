#!/usr/bin/env python3
"""Parse real group numbers from assembly data."""
import json
import re
import urllib.request
import ssl

ssl_ctx = ssl.create_default_context()

# Load assembly history
with open('/tmp/assembleias_historico_imoveis.json') as f:
    data = json.load(f)

# Get most recent entry (Jan 2026)
latest = data[-1]
print(f"=== IMOVEIS - {latest['month_name']} ===\n")

all_real_groups = {}
for result in latest.get('results', []):
    cat_str = result.get('categoria', '')
    participants = result.get('participantes', '?')

    groups_in_cat = []
    parts = re.split(r'[|,]', cat_str)
    for part in parts:
        part = part.strip()
        num = re.match(r'^(\d+)$', part)
        if num:
            groups_in_cat.append(num.group(1))

    print(f"Categoria ({participants} part.): {len(groups_in_cat)} grupos")
    for g in groups_in_cat:
        all_real_groups[g] = {"participants": participants, "segment": "imoveis"}

print(f"\nTotal grupos REAIS imoveis em Jan/2026: {len(all_real_groups)}")

# Veiculos
print("\n=== VEICULOS ===")
url = "https://api.mktademicon.com.br/api/assembleias/?act=options_motors"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
    opts = json.loads(resp.read())

veh_months = opts.get('select', [])
print(f"Total meses disponiveis: {len(veh_months)}")
print(f"Ultimos: {veh_months[-3:]}")

# Get latest month
last_m = veh_months[-1]
param = f"{last_m[0]}/{last_m[1]}"
url = f"https://api.mktademicon.com.br/api/assembleias/?act=assembleias_veiculos&param={param}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
    veh_data = json.loads(resp.read())

veh_results = veh_data.get('results', [])
print(f"\n{last_m[2]} {last_m[1]}: {len(veh_results)} categorias")

veh_groups = {}
for result in veh_results:
    cat_str = result.get('categoria', '')
    participants = result.get('participantes', '?')
    parts = re.split(r'[|,]', cat_str)
    groups_in_cat = []
    for part in parts:
        part = part.strip()
        num = re.match(r'^(\d+)$', part)
        if num:
            groups_in_cat.append(num.group(1))
    print(f"  Cat ({participants} part.): {len(groups_in_cat)} grupos - {groups_in_cat[:10]}...")
    for g in groups_in_cat:
        veh_groups[g] = {"participants": participants, "segment": "veiculos"}

print(f"\nTotal grupos REAIS veiculos: {len(veh_groups)}")

# Summary
print(f"\n{'='*60}")
print(f"RESUMO:")
print(f"  Imoveis: {len(all_real_groups)} grupos")
print(f"  Veiculos: {len(veh_groups)} grupos")
print(f"  TOTAL: {len(all_real_groups) + len(veh_groups)}")
