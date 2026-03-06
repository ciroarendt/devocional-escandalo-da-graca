import json

# Load all data sources
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_bids_config.json') as f:
    bids = json.load(f)

# Groups from SIMULATOR (full details)
sim_groups = {}
for seg_key, seg_data in sim.items():
    for gid, gdata in seg_data['groups'].items():
        sim_groups[gid] = {"segment": seg_data['label'], "data": gdata}

# Groups from CRM EXTRACTIONS (latest Feb 2026)
ext_groups = {}
for tp, tp_label in [('properties', 'Imoveis'), ('vehicles', 'Veiculos')]:
    latest_key = sorted(crm['extractions'][tp].keys())[-1] if crm['extractions'][tp] else None
    if not latest_key:
        continue
    ext = crm['extractions'][tp][latest_key]
    first = ext.get('extractionFirstNumber', {}).get('extraction', {})
    for cat_letter, cat_data in first.items():
        for g in cat_data.get('groups', []):
            ext_groups[g] = {
                "segment": tp_label,
                "category": cat_letter,
                "participants": cat_data.get('numberOfVacancies', 0)
            }

# Groups from BIDS CONFIG
bids_by_group = {}
for gname, configs in bids.items():
    gid = str(int(gname))  # Remove leading zeros
    enabled = [c['st_modalidade'] for c in configs if c.get('sn_habilitada') == 'S']
    all_mods = [c['st_modalidade'] for c in configs]
    bids_by_group[gid] = {"enabled": enabled, "all": all_mods, "configs": configs}

# Merge all
all_group_ids = sorted(
    set(list(sim_groups.keys()) + list(ext_groups.keys()) + list(bids_by_group.keys())),
    key=lambda x: int(x) if x.isdigit() else 0
)

print("=" * 80)
print("COBERTURA DE DADOS POR GRUPO")
print("=" * 80)

counts = {"full": 0, "no_sim": 0, "no_bids": 0, "no_ext": 0}
segments = {"Imoveis": {"full": 0, "partial": 0}, "Veiculos": {"full": 0, "partial": 0}, "Outros": {"full": 0, "partial": 0}}

for gid in all_group_ids:
    has_sim = gid in sim_groups
    has_ext = gid in ext_groups
    has_bids = gid in bids_by_group

    if has_sim:
        counts["full"] += 1
    else:
        counts["no_sim"] += 1

    seg = "Outros"
    if has_sim:
        seg = sim_groups[gid]["segment"]
    elif has_ext:
        seg = ext_groups[gid]["segment"]

    if has_sim:
        segments.setdefault(seg, {"full": 0, "partial": 0})["full"] += 1
    else:
        segments.setdefault(seg, {"full": 0, "partial": 0})["partial"] += 1

print(f"\nTotal grupos identificados: {len(all_group_ids)}")
print(f"\nCom dados COMPLETOS (simulador + bids + extracao): {counts['full']}")
print(f"Sem dados do simulador (credito/parcela): {counts['no_sim']}")

print(f"\nPor segmento:")
for seg, data in sorted(segments.items()):
    total = data['full'] + data['partial']
    print(f"  {seg}: {total} total ({data['full']} completos, {data['partial']} parciais)")

# Show what's missing for partial groups
print(f"\n{'=' * 80}")
print("GRUPOS SEM DADOS DO SIMULADOR (sem credito/parcela)")
print("=" * 80)
print(f"{'Grupo':<10} {'Segmento':<12} {'Cat.':<6} {'Partic.':<10} {'Bids':<20}")
print("-" * 60)

missing_sim = []
for gid in all_group_ids:
    if gid not in sim_groups:
        seg = ext_groups.get(gid, {}).get('segment', '?')
        cat = ext_groups.get(gid, {}).get('category', '?')
        part = ext_groups.get(gid, {}).get('participants', '?')
        bid_info = ",".join(bids_by_group.get(gid, {}).get('enabled', []))
        missing_sim.append((gid, seg, cat, part, bid_info))

# Show imoveis missing
imoveis_missing = [m for m in missing_sim if m[1] == 'Imoveis']
veiculos_missing = [m for m in missing_sim if m[1] == 'Veiculos']
print(f"\nImoveis sem simulador ({len(imoveis_missing)}):")
for gid, seg, cat, part, bid_info in imoveis_missing:
    print(f"  {gid:<10} Cat {cat:<4} {part:<10} Bids: {bid_info}")

print(f"\nVeiculos sem simulador ({len(veiculos_missing)}):")
for gid, seg, cat, part, bid_info in veiculos_missing[:30]:
    print(f"  {gid:<10} Cat {cat:<4} {part:<10} Bids: {bid_info}")
if len(veiculos_missing) > 30:
    print(f"  ... e mais {len(veiculos_missing) - 30}")

print(f"\n{'=' * 80}")
print("RESUMO FINAL")
print("=" * 80)
print(f"Dados DISPONÍVEIS para o sistema:")
print(f"  - Crédito, parcela, taxa, participantes, tipo parcela -> {counts['full']} grupos (simulador)")
print(f"  - Config de lances (LF/LL/LI/LM/LS) -> {len(bids_by_group)} grupos (CRM)")
print(f"  - Categoria (A-F) e participantes -> {len(ext_groups)} grupos (CRM extrações)")
print(f"\nDados FALTANDO:")
print(f"  - {counts['no_sim']} grupos SEM valor de crédito/parcela (cotas esgotadas no simulador)")
print(f"  - Estes grupos TÊM: categoria, participantes, config de lances")
print(f"  - Falta: crédito exato, parcela, taxa admin, meses restantes")
