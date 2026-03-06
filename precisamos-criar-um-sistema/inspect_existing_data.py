import json

# Check existing simulator data structure
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    grupos = json.load(f)

print("=== SIMULATOR DATA STRUCTURE ===")
for seg_key, seg_data in grupos.items():
    print(f"\nSegment: {seg_key}")
    print(f"  Label: {seg_data.get('label')}")
    print(f"  Groups: {len(seg_data.get('groups', {}))}")
    # Show first group details
    for gid, gdata in list(seg_data['groups'].items())[:1]:
        print(f"  Group {gid} keys: {list(gdata.keys())}")
        # Show all top-level values that aren't lists/dicts
        for k, v in gdata.items():
            if not isinstance(v, (list, dict)):
                print(f"    {k}: {v}")
            elif isinstance(v, list) and len(v) > 0:
                print(f"    {k}: list of {len(v)} items")
                if isinstance(v[0], dict):
                    print(f"      First item keys: {list(v[0].keys())}")
                    # Show all fields of first offer
                    for ok, ov in v[0].items():
                        if not isinstance(ov, (list, dict)):
                            print(f"        {ok}: {ov}")
            elif isinstance(v, dict):
                print(f"    {k}: dict with keys {list(v.keys())[:10]}")

# Check calendar for product IDs
print("\n\n=== CALENDAR DATA ===")
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json') as f:
    asm = json.load(f)

if 'calendar' in asm:
    for pid, cal_data in asm['calendar'].items():
        if isinstance(cal_data, list) and len(cal_data) > 0:
            first = cal_data[0]
            print(f"\nProduct {pid}: {len(cal_data)} assemblies")
            print(f"  First assembly keys: {list(first.keys())}")
            # Show groups in first assembly
            groups_in = first.get('groups', [])
            print(f"  Groups in first assembly: {len(groups_in)}")
            if groups_in:
                print(f"  First group: {json.dumps(groups_in[0], ensure_ascii=False)[:200]}")
