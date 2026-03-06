import json

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm = json.load(f)

# Check extraction structure more carefully
print("=== CRM EXTRACTIONS - DETAILED ===")
for ext_type in ['properties', 'vehicles']:
    exts = crm.get('extractions', {}).get(ext_type, {})
    if exts:
        latest_key = sorted(exts.keys())[-1]
        ext = exts[latest_key]
        print(f"\n{ext_type} - latest date: {latest_key}")
        print(f"  Keys: {list(ext.keys())}")

        first_num = ext.get('extractionFirstNumber', {})
        print(f"  extractionFirstNumber keys: {list(first_num.keys())}")

        extraction = first_num.get('extraction', {})
        all_groups = []
        for cat, cat_data in sorted(extraction.items()):
            groups = cat_data.get('groups', [])
            participants = cat_data.get('participants', '?')
            print(f"  Cat {cat}: {len(groups)} groups, {participants} participants")
            if groups:
                print(f"    First 10: {groups[:10]}")
            all_groups.extend(groups)

        print(f"  TOTAL unique groups: {len(set(all_groups))}")
        print(f"  All group numbers: {sorted(set(all_groups))[:30]}...")

# Check calendar structure
print("\n\n=== CALENDAR STRUCTURE ===")
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json') as f:
    asm = json.load(f)

for pid in ['101', '102']:
    cal = asm.get('calendar', {}).get(pid, [])
    print(f"\nProduct {pid}: {len(cal)} assemblies")
    if cal:
        first = cal[0]
        print(f"  First: {json.dumps(first, ensure_ascii=False)[:300]}")
        # Check grupos field type
        grupos = first.get('grupos', [])
        print(f"  grupos type: {type(grupos).__name__}, len: {len(grupos)}")
        if grupos:
            print(f"  First grupo: {grupos[0]} (type: {type(grupos[0]).__name__})")

# Check assembly history structure
print("\n\n=== ASSEMBLY HISTORY STRUCTURE ===")
imoveis = asm.get('imoveis_assemblies', [])
if imoveis:
    first_month = imoveis[0]
    print(f"First month type: {type(first_month).__name__}")
    print(f"First month keys: {list(first_month.keys())}")
    results = first_month.get('results', {})
    print(f"Results type: {type(results).__name__}")
    if isinstance(results, dict):
        print(f"Results keys: {list(results.keys())[:10]}")
        for k, v in list(results.items())[:2]:
            print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:300]}")
    elif isinstance(results, list):
        print(f"Results: {len(results)} items")
        if results:
            print(f"  First: {json.dumps(results[0], ensure_ascii=False)[:300]}")

# Also check: how many groups exist in bids config?
print("\n\n=== BIDS CONFIG - IMOVEIS GROUPS ===")
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json') as f:
    bids = json.load(f)

# Group numbers in bids config are zero-padded to 6 digits
# Imoveis groups are typically 4 digits like 1010, 1240 etc
# In sim data they appear as "002010", "001742" etc (name field) or 12167 (group number)
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim = json.load(f)

sim_names = set()
sim_group_nums = set()
for gid, gdata in sim.get('property-segment', {}).get('groups', {}).items():
    sim_names.add(gdata.get('name', ''))
    sim_group_nums.add(str(gdata.get('group', '')))

print(f"Sim imoveis names: {sorted(sim_names)[:10]}...")
print(f"Sim imoveis group nums: {sorted(sim_group_nums)[:10]}...")

# Check what bid config keys look like
bids_keys = sorted(bids.keys())
print(f"\nBids config: {len(bids_keys)} total keys")
print(f"Sample keys: {bids_keys[:20]}")
print(f"Key length distribution: {set(len(k) for k in bids_keys)}")
