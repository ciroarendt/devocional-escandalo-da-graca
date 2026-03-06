import json

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm = json.load(f)

print("=== RESUMO DOS DADOS CRM ===")
print(f"Draw dates: {len(crm['draw_dates'])}")
print(f"Lottery results: {len(crm['lottery_results'])}")
print(f"Property extractions: {len(crm['extractions']['properties'])}")
print(f"Vehicle extractions: {len(crm['extractions']['vehicles'])}")
print(f"Property analyses: {len(crm['analyses']['properties'])}")
print(f"Vehicle analyses: {len(crm['analyses']['vehicles'])}")
print(f"Wallets: {len(crm['wallets'])}")

# Analyze latest extraction to understand group categories
print("\n=== LATEST PROPERTY EXTRACTION (Feb 2026) ===")
latest_prop = crm['extractions']['properties'].get('2026-02-21', {})
if latest_prop:
    first = latest_prop.get('extractionFirstNumber', {})
    extraction = first.get('extraction', {})
    for cat, data in sorted(extraction.items()):
        groups = data.get('groups', [])
        vacancies = data.get('numberOfVacancies', 0)
        print(f"\n  Categoria {cat} ({vacancies} participantes): {len(groups)} grupos")
        print(f"    Grupos: {groups[:15]}{'...' if len(groups) > 15 else ''}")

print("\n\n=== LATEST VEHICLE EXTRACTION (Feb 2026) ===")
latest_veh = crm['extractions']['vehicles'].get('2026-02-21', {})
if latest_veh:
    first = latest_veh.get('extractionFirstNumber', {})
    extraction = first.get('extraction', {})
    for cat, data in sorted(extraction.items()):
        groups = data.get('groups', [])
        vacancies = data.get('numberOfVacancies', 0)
        print(f"\n  Categoria {cat} ({vacancies} participantes): {len(groups)} grupos")
        print(f"    Grupos: {groups[:20]}{'...' if len(groups) > 20 else ''}")

# Analyze wallets data
print("\n\n=== WALLETS SUMMARY ===")
by_segment = {}
for w in crm['wallets']:
    seg = w.get('quotaSegment', '?')
    if seg not in by_segment:
        by_segment[seg] = []
    by_segment[seg].append(w)

for seg, items in sorted(by_segment.items()):
    print(f"\nSegmento {seg}: {len(items)} cotas")
    by_group = {}
    for item in items:
        g = item.get('quotaGroup', '?')
        if g not in by_group:
            by_group[g] = []
        by_group[g].append(item)
    for g, g_items in sorted(by_group.items()):
        contempladas = sum(1 for i in g_items if i.get('quotaIsContemplated'))
        credits = [i.get('quotaCredit', 0) for i in g_items]
        statuses = set(i.get('quotaStatusName', '?') for i in g_items)
        print(f"  Grupo {g}: {len(g_items)} cotas, contempladas={contempladas}, "
              f"creditos=R$ {min(credits):,.0f}-{max(credits):,.0f}, status={statuses}")

# Analyze analysis data - lance types
print("\n\n=== LANCE TYPES (from analysis) ===")
lance_types = {}
for date, data in crm['analyses']['properties'].items():
    for item in data:
        ps = item.get('prizeStatus', {})
        lt = ps.get('lanceType')
        label = ps.get('label', '')
        status = ps.get('status', '')
        key = f"{lt}|{status}|{label}"
        if key not in lance_types:
            lance_types[key] = 0
        lance_types[key] += 1

print("Properties lance types:")
for key, count in sorted(lance_types.items(), key=lambda x: -x[1]):
    lt, status, label = key.split('|')
    print(f"  lanceType={lt}, status={status}, label='{label}' ({count}x)")

lance_types_v = {}
for date, data in crm['analyses']['vehicles'].items():
    for item in data:
        ps = item.get('prizeStatus', {})
        lt = ps.get('lanceType')
        label = ps.get('label', '')
        status = ps.get('status', '')
        key = f"{lt}|{status}|{label}"
        if key not in lance_types_v:
            lance_types_v[key] = 0
        lance_types_v[key] += 1

print("\nVehicles lance types:")
for key, count in sorted(lance_types_v.items(), key=lambda x: -x[1]):
    lt, status, label = key.split('|')
    print(f"  lanceType={lt}, status={status}, label='{label}' ({count}x)")

# Count all unique groups across all extractions
print("\n\n=== TOTAL UNIQUE GROUPS IN EXTRACTIONS ===")
all_prop_groups = set()
for date, ext in crm['extractions']['properties'].items():
    for prize_key in ['extractionFirstNumber', 'extractionSecondNumber', 'extractionThirdNumber', 'extractionFourthNumber', 'extractionFifthNumber']:
        prize = ext.get(prize_key, {})
        for cat, cat_data in prize.get('extraction', {}).items():
            for g in cat_data.get('groups', []):
                all_prop_groups.add(g)

all_veh_groups = set()
for date, ext in crm['extractions']['vehicles'].items():
    for prize_key in ['extractionFirstNumber', 'extractionSecondNumber', 'extractionThirdNumber', 'extractionFourthNumber', 'extractionFifthNumber']:
        prize = ext.get(prize_key, {})
        for cat, cat_data in prize.get('extraction', {}).items():
            for g in cat_data.get('groups', []):
                all_veh_groups.add(g)

print(f"Unique property groups: {len(all_prop_groups)}")
print(f"Unique vehicle groups: {len(all_veh_groups)}")
