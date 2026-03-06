import json

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    grupos = json.load(f)

# Get salesPlan details and productIds
print("=== SALES PLAN DETAILS ===")
products = {}
for seg_key, seg_data in grupos.items():
    for gid, gdata in seg_data['groups'].items():
        sp = gdata.get('salesPlan', {})
        pid = sp.get('productId')
        if pid:
            if pid not in products:
                products[pid] = {'segment': seg_data['label'], 'groups': [], 'names': []}
            products[pid]['groups'].append(gid)
            products[pid]['names'].append(gdata.get('name', ''))

print(f"\nUnique productIds: {len(products)}")
for pid, info in sorted(products.items()):
    print(f"  Product '{pid}': {info['segment']} - {len(info['groups'])} groups")
    print(f"    Names: {', '.join(info['names'][:5])}...")

# Show full salesPlan for a few groups
print("\n\n=== FULL SALES PLAN SAMPLES ===")
for seg_key, seg_data in grupos.items():
    for gid, gdata in list(seg_data['groups'].items())[:1]:
        print(f"\nGroup {gid} ({seg_data['label']}):")
        sp = gdata.get('salesPlan', {})
        for k, v in sp.items():
            print(f"  {k}: {v}")

# Show installment details
print("\n\n=== INSTALLMENT SAMPLES ===")
for seg_key, seg_data in grupos.items():
    for gid, gdata in list(seg_data['groups'].items())[:1]:
        print(f"\nGroup {gid} ({seg_data['label']}):")
        inst = gdata.get('installment', {})
        for k, v in inst.items():
            print(f"  {k}: {v}")
