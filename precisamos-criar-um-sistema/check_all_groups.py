import json

# 1. Simulator data (what we have)
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim = json.load(f)

print("=== SIMULADOR (grupos com cotas disponiveis) ===")
for seg, data in sim.items():
    groups = data.get('groups', {})
    print(f"  {data['label']}: {len(groups)} grupos")

# 2. Calendar data (all groups that have assemblies scheduled)
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json') as f:
    asm = json.load(f)

print("\n=== CALENDARIO (grupos com assembleias futuras) ===")
for pid, assemblies in asm.get('calendar', {}).items():
    all_groups = set()
    for a in assemblies:
        for g in a.get('grupos', []):
            all_groups.add(str(g))
    print(f"  Produto {pid}: {len(all_groups)} grupos unicos no calendario")
    if pid == '101':
        imoveis_calendar = all_groups

# 3. Bids config (all groups we got config for)
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json') as f:
    bids = json.load(f)

print(f"\n=== BIDS CONFIG ===")
print(f"  Total grupos com config de lances: {len(bids)}")

# 4. CRM extractions (groups by category)
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm = json.load(f)

print("\n=== CRM EXTRACTIONS (categorias) ===")
for ext_type in ['properties', 'vehicles']:
    exts = crm.get('extractions', {}).get(ext_type, {})
    if exts:
        latest_key = sorted(exts.keys())[-1]
        ext = exts[latest_key]
        first = ext.get('extractionFirstNumber', {}).get('extraction', {})
        total_groups = 0
        for cat, cat_data in sorted(first.items()):
            groups_in_cat = cat_data.get('groups', [])
            total_groups += len(groups_in_cat)
            print(f"  {ext_type} Cat {cat}: {len(groups_in_cat)} grupos, {cat_data.get('participants', '?')} participantes")
        print(f"  {ext_type} TOTAL: {total_groups} grupos")

# 5. Compare: what's in calendar but NOT in simulator
print("\n=== IMOVEIS: CALENDARIO vs SIMULADOR ===")
sim_imoveis = set(str(g) for g in sim.get('property-segment', {}).get('groups', {}).keys())
print(f"  No simulador: {len(sim_imoveis)} grupos")
print(f"  No calendario: {len(imoveis_calendar)} grupos")
missing = imoveis_calendar - sim_imoveis
print(f"  No calendario mas NAO no simulador: {len(missing)} grupos")
if missing:
    print(f"  Grupos faltantes: {sorted(missing)[:30]}...")

# 6. Assembly history - count unique groups
print("\n=== ASSEMBLEIA HISTORICO (grupos que ja apareceram) ===")
imoveis_hist_groups = set()
for month_data in asm.get('imoveis_assemblies', []):
    if isinstance(month_data, dict):
        for cat_key, cat_val in month_data.items():
            if isinstance(cat_val, dict):
                for item in cat_val.get('items', []):
                    if 'grupo' in item:
                        imoveis_hist_groups.add(str(item['grupo']))
    elif isinstance(month_data, list):
        for item in month_data:
            if isinstance(item, dict):
                for cat_key, cat_val in item.items():
                    if isinstance(cat_val, dict):
                        for sub_item in cat_val.get('items', []):
                            if 'grupo' in sub_item:
                                imoveis_hist_groups.add(str(sub_item['grupo']))

print(f"  Imoveis historico: {len(imoveis_hist_groups)} grupos unicos")

# Check the structure of assembly data
print("\n=== ESTRUTURA ASSEMBLEIA IMOVEIS ===")
imoveis_asm = asm.get('imoveis_assemblies', [])
print(f"  Total meses: {len(imoveis_asm)}")
if imoveis_asm:
    first = imoveis_asm[0]
    print(f"  Tipo primeiro item: {type(first).__name__}")
    if isinstance(first, dict):
        print(f"  Keys: {list(first.keys())[:10]}")
        # Dig into first category
        for k, v in list(first.items())[:2]:
            print(f"    {k}: tipo={type(v).__name__}")
            if isinstance(v, dict):
                print(f"      Keys: {list(v.keys())[:10]}")
                items = v.get('items', v.get('data', []))
                if isinstance(items, list) and items:
                    print(f"      First item: {json.dumps(items[0], ensure_ascii=False)[:200]}")
            elif isinstance(v, list) and v:
                print(f"      First: {json.dumps(v[0], ensure_ascii=False)[:200]}")
