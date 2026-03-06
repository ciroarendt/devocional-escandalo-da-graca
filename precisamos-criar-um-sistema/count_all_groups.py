#!/usr/bin/env python3
"""Count ALL unique groups across assembly results and simulator data."""
import json
import re

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos_completo.json') as f:
    data = json.load(f)

assembly = data.get('assembly_results', {})

def extract_group_ids(cat_string):
    """Extract individual group IDs from category strings like '651 | 660 ao 700 | 720'."""
    groups = set()
    cat_string = str(cat_string)

    # Remove pipe separators and extra spaces
    parts = re.split(r'\s*\|\s*', cat_string)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Check for range patterns: "660 ao 700", "660 a 700", "4101 a 4110"
        range_match = re.match(r'(\d+)\s+(?:ao?|a)\s+(\d+)', part)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            for i in range(start, end + 1):
                groups.add(str(i))
        else:
            # Single group ID
            num_match = re.match(r'^(\d+)$', part)
            if num_match:
                groups.add(num_match.group(1))

    return groups

# Collect ALL groups from assembly results
all_assembly_groups = {"imoveis": set(), "veiculos": set()}

# Imoveis
newcon = assembly.get('assembleias_newcon', {}).get('results', {})
for month, mdata in newcon.items():
    for r in mdata.get('results', []):
        cat = str(r.get('categoria', ''))
        groups = extract_group_ids(cat)
        all_assembly_groups["imoveis"].update(groups)

# Veiculos
veic = assembly.get('assembleias_veiculos', {}).get('results', {})
for month, mdata in veic.items():
    for r in mdata.get('results', []):
        cat = str(r.get('categoria', ''))
        groups = extract_group_ids(cat)
        all_assembly_groups["veiculos"].update(groups)

# Simulator groups
sim_groups = {}
for seg_key in ["property-segment", "vehicle-segment", "motorcycle-segment", "service-segment", "movable-assets-segment"]:
    seg_data = data.get(seg_key, {})
    sim_groups[seg_key] = set(seg_data.get('groups', {}).keys())

# Calendar groups
cal_groups = {}
for seg_key in ["property-segment", "vehicle-segment", "motorcycle-segment", "service-segment", "movable-assets-segment"]:
    seg_data = data.get(seg_key, {})
    cal_groups[seg_key] = set(seg_data.get('calendar_group_ids', []))

print("=" * 70)
print("CONTAGEM COMPLETA DE GRUPOS ADEMICON")
print("=" * 70)

print("\n--- IMOVEIS ---")
print(f"  Grupos no simulador (com cotas disponiveis): {len(sim_groups.get('property-segment', set()))}")
print(f"  Grupos no calendario de assembleias:         {len(cal_groups.get('property-segment', set()))}")
print(f"  Grupos nos resultados de assembleias:        {len(all_assembly_groups['imoveis'])}")
all_imoveis = sim_groups.get('property-segment', set()) | cal_groups.get('property-segment', set()) | all_assembly_groups['imoveis']
print(f"  TOTAL UNICO de grupos de imoveis:            {len(all_imoveis)}")

print("\n--- VEICULOS ---")
print(f"  Grupos no simulador:                         {len(sim_groups.get('vehicle-segment', set()))}")
print(f"  Grupos no calendario:                        {len(cal_groups.get('vehicle-segment', set()))}")
print(f"  Grupos nos resultados de assembleias:        {len(all_assembly_groups['veiculos'])}")
all_veiculos = sim_groups.get('vehicle-segment', set()) | cal_groups.get('vehicle-segment', set()) | all_assembly_groups['veiculos']
print(f"  TOTAL UNICO de grupos de veiculos:           {len(all_veiculos)}")

print("\n--- MOTOS ---")
print(f"  Grupos no simulador:                         {len(sim_groups.get('motorcycle-segment', set()))}")
print(f"  Grupos no calendario:                        {len(cal_groups.get('motorcycle-segment', set()))}")

print("\n--- SERVICOS ---")
print(f"  Grupos no simulador:                         {len(sim_groups.get('service-segment', set()))}")
print(f"  Grupos no calendario:                        {len(cal_groups.get('service-segment', set()))}")

print("\n--- OUTROS BENS MOVEIS ---")
print(f"  Grupos no simulador:                         {len(sim_groups.get('movable-assets-segment', set()))}")
print(f"  Grupos no calendario:                        {len(cal_groups.get('movable-assets-segment', set()))}")

total_sim = sum(len(v) for v in sim_groups.values())
total_all = len(all_imoveis) + len(all_veiculos) + len(sim_groups.get('motorcycle-segment', set())) + len(sim_groups.get('service-segment', set())) + len(sim_groups.get('movable-assets-segment', set()))

print(f"\n{'='*70}")
print(f"TOTAL grupos com dados detalhados (simulador): {total_sim}")
print(f"TOTAL grupos identificados (todas as fontes):  ~{total_all}+")

# List groups only in assembly but not in simulator (no detailed data)
missing_imoveis = all_imoveis - sim_groups.get('property-segment', set())
missing_veiculos = all_veiculos - sim_groups.get('vehicle-segment', set())
print(f"\nGrupos de imoveis SEM dados detalhados: {len(missing_imoveis)}")
print(f"Grupos de veiculos SEM dados detalhados: {len(missing_veiculos)}")
print(f"\n(Esses grupos provavelmente ja estao com cotas esgotadas)")
