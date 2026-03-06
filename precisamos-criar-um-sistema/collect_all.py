#!/usr/bin/env python3
"""Collect detailed data for ALL groups via simulator API with exhaustive scanning."""
import json
import urllib.request
import ssl
import time

ssl_ctx = ssl.create_default_context()
tenant = "da4c01e8-e329-4ad2-b941-2c6418ac2db6"
base_url = "https://api-simulador.ademicon.com.br"

def fetch_sim(segment, value, value_type="amount"):
    payload = json.dumps({
        "data": {
            "customer": {
                "name": "S", "email": "s@s.com", "phone": "11999990000",
                "zipCode": "87000000", "document": "00000000000",
                "acceptsTerms": True, "acceptsCommunications": False,
                "documentType": "CPF"
            },
            "consortium": {
                "segment": segment,
                "credit": {"value": round(value, 2), "valueType": value_type},
                "offer": {"min": 0, "max": 999999, "valueType": "installment"}
            }
        },
        "metadata": {"proposal": {"quantity": {"min": 0, "max": 10}}}
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/simulations", data=payload,
        headers={
            "Content-Type": "application/json",
            "x-tenant-id": tenant,
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as resp:
        return json.loads(resp.read())


def scan_segment(segment, min_val, max_val, step):
    """Scan a segment with fine-grained steps to capture max groups."""
    groups = {}
    val = min_val
    consecutive_no_new = 0

    while val <= max_val:
        try:
            result = fetch_sim(segment, val)
            offers = result.get('data', {}).get('consortiumOffers', [])
            new = 0
            for o in offers:
                gid = o.get('group', 'unknown')
                if gid not in groups:
                    groups[gid] = o
                    new += 1
            if new > 0:
                print(f"  R$ {val:>12,.2f}: {len(offers)} ofertas, +{new} novos = {len(groups)} total")
                consecutive_no_new = 0
            else:
                consecutive_no_new += 1
        except Exception as e:
            print(f"  R$ {val:>12,.2f}: ERRO - {e}")

        val += step
        time.sleep(0.2)

    # Also scan by installment
    print(f"  --- Scanning by installment ---")
    for inst_val in range(200, 10000, 150):
        try:
            result = fetch_sim(segment, inst_val, "installment")
            offers = result.get('data', {}).get('consortiumOffers', [])
            new = 0
            for o in offers:
                gid = o.get('group', 'unknown')
                if gid not in groups:
                    groups[gid] = o
                    new += 1
            if new > 0:
                print(f"  Parcela R$ {inst_val:>6}: +{new} novos = {len(groups)} total")
        except:
            pass
        time.sleep(0.15)

    return groups


# ============================================================
# IMOVEIS - 116 grupos esperados, range 80k-1.27M
# ============================================================
print("=" * 60)
print("IMOVEIS (property-segment)")
print("=" * 60)
imoveis = scan_segment("property-segment", 80000, 1280000, 5000)
print(f"\nTOTAL IMOVEIS: {len(imoveis)}")

# ============================================================
# VEICULOS - 15 grupos, range 40k-503k
# ============================================================
print("\n" + "=" * 60)
print("VEICULOS (vehicle-segment)")
print("=" * 60)
veiculos = scan_segment("vehicle-segment", 15000, 510000, 5000)
print(f"\nTOTAL VEICULOS: {len(veiculos)}")

# ============================================================
# MOTOS (motorcycle-segment)
# ============================================================
print("\n" + "=" * 60)
print("MOTOS (motorcycle-segment)")
print("=" * 60)
motos = scan_segment("motorcycle-segment", 15000, 35000, 2000)
print(f"\nTOTAL MOTOS: {len(motos)}")

# ============================================================
# SERVICOS (service-segment)
# ============================================================
print("\n" + "=" * 60)
print("SERVICOS (service-segment)")
print("=" * 60)
servicos = scan_segment("service-segment", 15000, 35000, 2000)
print(f"\nTOTAL SERVICOS: {len(servicos)}")

# ============================================================
# OUTROS BENS MOVEIS (movable-assets-segment)
# ============================================================
print("\n" + "=" * 60)
print("OUTROS BENS MOVEIS (movable-assets-segment)")
print("=" * 60)
obm = scan_segment("movable-assets-segment", 100000, 210000, 5000)
print(f"\nTOTAL OBM: {len(obm)}")

# ============================================================
# SAVE ALL
# ============================================================
all_data = {
    "property-segment": {
        "label": "Imoveis",
        "groups": imoveis,
        "range": {"min": 80000, "max": 1273442.29}
    },
    "vehicle-segment": {
        "label": "Veiculos",
        "groups": veiculos,
        "range": {"min": 40000, "max": 502900}
    },
    "motorcycle-segment": {
        "label": "Motos",
        "groups": motos,
        "range": {"min": 15000, "max": 31254}
    },
    "service-segment": {
        "label": "Servicos",
        "groups": servicos,
        "range": {"min": 15055.5, "max": 33382.71}
    },
    "movable-assets-segment": {
        "label": "Outros Bens Moveis",
        "groups": obm,
        "range": {"min": 102180, "max": 204360}
    }
}

output = "/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json"
with open(output, 'w') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("RESUMO FINAL")
print("=" * 60)
total = 0
for k, v in all_data.items():
    count = len(v['groups'])
    total += count
    print(f"  {v['label']}: {count} grupos")
print(f"  TOTAL: {total} grupos")
print(f"\nSalvo em {output}")
