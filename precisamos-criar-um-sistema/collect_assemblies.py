#!/usr/bin/env python3
"""Collect assembly history and vehicle data from MKT API."""
import json
import urllib.request
import ssl

ssl_ctx = ssl.create_default_context()

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
        return json.loads(resp.read())

# ============================================================
# IMOVEIS ASSEMBLY HISTORY
# ============================================================
print("=== Collecting assembly history for IMOVEIS ===")
opts = fetch_json("https://api.mktademicon.com.br/api/assembleias/?act=options")
months = opts.get('select', [])

imoveis_assemblies = []
for m in months:
    month_num, year, month_name = m
    param = f"{month_num}/{year}"
    try:
        d = fetch_json(f"https://api.mktademicon.com.br/api/assembleias/?act=assembleias_newcon&param={param}")
        results = d.get('results', [])
        lotteries = d.get('lotteries', {})
        if results:
            imoveis_assemblies.append({
                "month": param,
                "month_name": f"{month_name} {year}",
                "results": results,
                "lotteries": lotteries if isinstance(lotteries, dict) else {}
            })
            print(f"  {month_name} {year}: {len(results)} categorias")
    except Exception as e:
        print(f"  {month_name} {year}: ERRO - {e}")

# ============================================================
# VEICULOS ASSEMBLY HISTORY
# ============================================================
print("\n=== Collecting assembly history for VEICULOS ===")
opts_v = fetch_json("https://api.mktademicon.com.br/api/assembleias/?act=options_motors")
months_v = opts_v.get('select', [])

veiculos_assemblies = []
for m in months_v:
    month_num, year, month_name = m
    param = f"{month_num}/{year}"
    try:
        d = fetch_json(f"https://api.mktademicon.com.br/api/assembleias/?act=assembleias_veiculos&param={param}")
        results = d.get('results', [])
        lotteries = d.get('lotteries', {})
        if results:
            veiculos_assemblies.append({
                "month": param,
                "month_name": f"{month_name} {year}",
                "results": results,
                "lotteries": lotteries if isinstance(lotteries, dict) else {}
            })
            print(f"  {month_name} {year}: {len(results)} categorias")
    except Exception as e:
        print(f"  {month_name} {year}: ERRO - {e}")

# ============================================================
# ASSEMBLY CALENDAR (future assemblies)
# ============================================================
print("\n=== Collecting assembly calendar ===")
tenant = "da4c01e8-e329-4ad2-b941-2c6418ac2db6"
calendar = {}
for prod_id in [101, 102, 105, 106, 109]:
    url = f"https://api-simulador.ademicon.com.br/assemblies/calendar/new-format?idParceiro=1&idProduto={prod_id}"
    try:
        req = urllib.request.Request(url, headers={
            "Content-Type": "application/json",
            "x-tenant-id": tenant,
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
            cal = json.loads(resp.read())
            if cal:
                calendar[str(prod_id)] = cal
                print(f"  Produto {prod_id}: {len(cal)} assembleias futuras")
    except Exception as e:
        print(f"  Produto {prod_id}: ERRO - {e}")

# ============================================================
# SAVE ALL
# ============================================================
output = {
    "imoveis_assemblies": imoveis_assemblies,
    "veiculos_assemblies": veiculos_assemblies,
    "calendar": calendar
}

output_path = "/home/dev/workspace/precisamos-criar-um-sistema/dados_assembleias.json"
with open(output_path, 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"RESUMO:")
print(f"  Imoveis: {len(imoveis_assemblies)} meses de historico")
print(f"  Veiculos: {len(veiculos_assemblies)} meses de historico")
print(f"  Calendario futuro: {len(calendar)} produtos")
print(f"\nSalvo em {output_path}")
