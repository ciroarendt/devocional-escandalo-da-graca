import requests, json, time

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

crm = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Load extraction data to get all group IDs
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm_data = json.load(f)

# Get all unique groups from latest extraction
all_groups = set()
for tp in ['properties', 'vehicles']:
    for date, ext in crm_data['extractions'][tp].items():
        for prize_key in ['extractionFirstNumber']:
            prize = ext.get(prize_key, {})
            for cat, cat_data in prize.get('extraction', {}).items():
                for g in cat_data.get('groups', []):
                    all_groups.add(g)

print(f"Total unique groups to query: {len(all_groups)}")

# Format groups with leading zeros (6 digits)
formatted_groups = []
for g in sorted(all_groups):
    formatted = g.zfill(6)
    formatted_groups.append(formatted)

print(f"Formatted groups (sample): {formatted_groups[:5]}")

# Query bids config in batches (comma-separated groups)
# API accepts comma-separated groups parameter
all_bids_config = {}
batch_size = 10
batches = [formatted_groups[i:i+batch_size] for i in range(0, len(formatted_groups), batch_size)]

print(f"Querying in {len(batches)} batches of {batch_size}...")

for i, batch in enumerate(batches):
    groups_param = ",".join(batch)
    r = requests.get(
        f"{crm}/wallets/bids/config?groups={groups_param}",
        headers=headers, timeout=15
    )
    if r.status_code == 200:
        data = r.json()
        if data:
            for item in data:
                gname = item.get('groupname', '')
                if gname not in all_bids_config:
                    all_bids_config[gname] = []
                all_bids_config[gname].append(item)
            print(f"  Batch {i+1}: {len(data)} configs for groups {batch[:3]}...")
    time.sleep(0.3)

print(f"\n=== BIDS CONFIG SUMMARY ===")
print(f"Groups with bid config: {len(all_bids_config)}")

# Show all unique bid modalities
modalities = {}
for gname, configs in all_bids_config.items():
    for cfg in configs:
        mod = cfg.get('nm_modalidade', '?')
        st_mod = cfg.get('st_modalidade', '?')
        enabled = cfg.get('sn_habilitada', '?')
        key = f"{mod} ({st_mod}) enabled={enabled}"
        if key not in modalities:
            modalities[key] = 0
        modalities[key] += 1

print("\nBid modalities found:")
for key, count in sorted(modalities.items(), key=lambda x: -x[1]):
    print(f"  {key}: {count} groups")

# Show detailed config for first few groups
print("\n=== DETAILED BID CONFIG (sample) ===")
for gname in sorted(all_bids_config.keys())[:5]:
    configs = all_bids_config[gname]
    print(f"\nGrupo {gname}:")
    for cfg in configs:
        print(f"  Modalidade: {cfg.get('nm_modalidade')} ({cfg.get('st_modalidade')})")
        print(f"    Habilitada: {cfg.get('sn_habilitada')}")
        print(f"    Oferta: {cfg.get('st_oferta')}")
        print(f"    Lance embutido max: {cfg.get('pe_lance_embutido_max')}%")
        print(f"    Parcelas lance embutido max: {cfg.get('qt_pc_lance_embutido_max')}")
        print(f"    Regra lance: {cfg.get('regra_lance')}")
        # Print any other fields
        known_keys = {'id_grupo', 'groupname', 'nm_modalidade', 'st_modalidade', 'sn_habilitada',
                       'st_oferta', 'pe_lance_embutido_max', 'qt_pc_lance_embutido_max', 'regra_lance'}
        extra = {k: v for k, v in cfg.items() if k not in known_keys}
        if extra:
            print(f"    Extra fields: {json.dumps(extra, ensure_ascii=False)}")

# Save bids config
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json', 'w') as f:
    json.dump(all_bids_config, f, ensure_ascii=False, indent=2)

print(f"\nSalvo em dados_bids_config.json")
