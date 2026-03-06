#!/usr/bin/env python3
"""Collect ADEMICON consortium group data from their simulator API."""
import json
import urllib.request
import ssl
import time

ssl_ctx = ssl.create_default_context()
tenant = "da4c01e8-e329-4ad2-b941-2c6418ac2db6"
base_url = "https://api-simulador.ademicon.com.br"

segments = {
    "property-segment": {"min": 80000, "max": 1273442.29, "label": "Imoveis"},
    "vehicle-segment": {"min": 40000, "max": 502900, "label": "Veiculos"},
    "motorcycle-segment": {"min": 15000, "max": 31254, "label": "Motos"},
    "service-segment": {"min": 15055.5, "max": 33382.71, "label": "Servicos"},
    "movable-assets-segment": {"min": 102180, "max": 204360, "label": "Outros Bens Moveis"},
}

all_data = {}

for seg_key, seg_info in segments.items():
    print(f"\n{'='*60}")
    print(f"Coletando: {seg_info['label']} ({seg_key})")

    min_val = seg_info['min']
    max_val = seg_info['max']
    range_size = max_val - min_val

    # Generate test values spread across the range
    test_values = []
    num_points = 5
    for i in range(num_points):
        val = min_val + (range_size * i / (num_points - 1))
        test_values.append(round(val, 2))

    seg_groups = {}

    for val in test_values:
        payload = json.dumps({
            "data": {
                "customer": {
                    "name": "Sistema Analise",
                    "email": "analise@sistema.com",
                    "phone": "11999990000",
                    "zipCode": "87000000",
                    "document": "00000000000",
                    "acceptsTerms": True,
                    "acceptsCommunications": False,
                    "documentType": "CPF"
                },
                "consortium": {
                    "segment": seg_key,
                    "credit": {
                        "value": val,
                        "valueType": "amount"
                    },
                    "offer": {
                        "min": 0,
                        "max": 999999,
                        "valueType": "installment"
                    }
                }
            },
            "metadata": {
                "proposal": {
                    "quantity": {"min": 0, "max": 10}
                }
            }
        }).encode()

        req = urllib.request.Request(
            f"{base_url}/simulations",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-tenant-id": tenant,
                "User-Agent": "Mozilla/5.0"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as resp:
                result = json.loads(resp.read())
                offers = result.get('data', {}).get('consortiumOffers', [])
                print(f"  R$ {val:,.2f}: {len(offers)} grupos")

                for offer in offers:
                    grp = offer.get('group', 'unknown')
                    if grp not in seg_groups:
                        seg_groups[grp] = offer
        except Exception as e:
            print(f"  R$ {val:,.2f}: ERRO - {e}")

        time.sleep(0.5)

    all_data[seg_key] = {
        "label": seg_info['label'],
        "range": seg_info,
        "groups": seg_groups
    }
    print(f"  Total grupos unicos: {len(seg_groups)}")

# Save all data
output_path = "/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json"
with open(output_path, 'w') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print("RESUMO:")
total = 0
for key, info in all_data.items():
    count = len(info['groups'])
    total += count
    print(f"  {info['label']}: {count} grupos")
print(f"  TOTAL: {total} grupos")
print(f"\nDados salvos em {output_path}")
