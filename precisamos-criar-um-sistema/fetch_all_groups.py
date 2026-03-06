import requests
import json

# The AVA PRO uses apiv2.ademitech.com.br with tenant 60d0db2552fcc900beb502d5
# But the public simulator API has a similar structure
# Let's try the public simulator first since WAF blocks ademitech

tenant = "da4c01e8-e329-4ad2-b941-2c6418ac2db6"
sim_base = "https://api-simulador.ademicon.com.br"
headers_sim = {"x-tenant-id": tenant}

# AVA PRO tenant and endpoints
ava_tenant = "60d0db2552fcc900beb502d5"

# Product IDs (from calendar data)
products = {
    "101": "Imoveis",
    "102": "Veiculos",
    "105": "Veiculos/Pesados",
    "106": "Servicos",
    "109": "OBM"
}

# First try: public simulator - list groups per segment
print("=== TRYING PUBLIC SIMULATOR API ===")
segments = [
    "property-segment",
    "vehicle-segment",
    "motorcycle-segment",
    "service-segment",
    "movable-assets-segment"
]

for seg in segments:
    r = requests.get(f"{sim_base}/groups?segment={seg}", headers=headers_sim, timeout=15)
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list):
            print(f"\n{seg}: {len(data)} groups")
            if data:
                print(f"  Sample: {json.dumps(data[0], ensure_ascii=False)[:300]}")
        elif isinstance(data, dict):
            print(f"\n{seg}: dict with keys {list(data.keys())[:10]}")
    else:
        print(f"\n{seg}: HTTP {r.status_code}")

# Second try: the /tenants/{tenant}/simular/grupos?product={id} pattern from AVA PRO
# but using the public simulator base URL
print("\n\n=== TRYING /tenants/simular/grupos PATTERN ===")
for pid, pname in products.items():
    url = f"{sim_base}/tenants/{tenant}/simular/grupos?product={pid}"
    r = requests.get(url, headers=headers_sim, timeout=15)
    print(f"\nProduct {pid} ({pname}): HTTP {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list):
            print(f"  {len(data)} groups")
            if data:
                print(f"  Sample: {json.dumps(data[0], ensure_ascii=False)[:300]}")
        elif isinstance(data, dict):
            print(f"  Keys: {list(data.keys())[:10]}")
            if 'data' in data:
                d = data['data']
                if isinstance(d, list):
                    print(f"  data: {len(d)} items")
                    if d:
                        print(f"  Sample: {json.dumps(d[0], ensure_ascii=False)[:300]}")

# Third try: maybe the product is not an ID but a MongoDB ObjectId
# Let's check the existing grupos data for product IDs
print("\n\n=== CHECKING EXISTING DATA FOR PRODUCT IDS ===")
with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    grupos = json.load(f)

product_ids = set()
for seg_key, seg_data in grupos.items():
    for gid, gdata in seg_data['groups'].items():
        offers = gdata.get('offers', [])
        for offer in offers:
            pid = offer.get('productId') or offer.get('product_id') or offer.get('id_produto')
            if pid:
                product_ids.add(str(pid))
        # Check group-level product info
        for key in ['productId', 'product_id', 'id_produto']:
            if key in gdata:
                product_ids.add(str(gdata[key]))

print(f"Product IDs found in existing data: {product_ids}")
