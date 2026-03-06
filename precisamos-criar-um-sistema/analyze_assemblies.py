#!/usr/bin/env python3
import json

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos_completo.json') as f:
    data = json.load(f)

assembly = data.get('assembly_results', {})

# Imoveis
newcon = assembly.get('assembleias_newcon', {})
results = newcon.get('results', {})

print("=== RESULTADOS ASSEMBLEIAS IMOVEIS ===\n")
for month, month_data in sorted(results.items()):
    res = month_data.get('results', [])
    lot = month_data.get('lotteries', {})
    if not res:
        continue
    print(f"--- {month} ---")
    if isinstance(lot, dict) and lot:
        dt = lot.get('data', 'N/A')
        print(f"  Data: {dt}")
        for k, v in lot.items():
            if '_loteria' in k:
                print(f"    {k}: {v}")
    for r in res:
        cat_code = r.get('categoria', '?')
        part = r.get('participantes', '?')
        nums = [str(r.get(f'{i}_num', '')) for i in range(1, 6) if r.get(f'{i}_num')]
        print(f"  Cat {cat_code} ({part} part.): sorteados = {', '.join(nums)}")
    print()

# Veiculos
veiculos = assembly.get('assembleias_veiculos', {})
vresults = veiculos.get('results', {})
print("\n=== RESULTADOS ASSEMBLEIAS VEICULOS ===\n")
for month, month_data in sorted(vresults.items()):
    res = month_data.get('results', [])
    if not res:
        continue
    print(f"--- {month} ---")
    for r in res:
        cat_code = r.get('categoria', '?')
        part = r.get('participantes', '?')
        nums = [str(r.get(f'{i}_num', '')) for i in range(1, 6) if r.get(f'{i}_num')]
        print(f"  Cat {cat_code} ({part} part.): sorteados = {', '.join(nums)}")
    print()
