import requests, json

# Read token
with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

print(f"Token: {token[:50]}...")

# Base URLs
client_api = "https://api-clientv2.ademitech.com.br"
crm_api = "https://crm-consultor.ademicon.com.br"
apiv2 = "https://apiv2.ademitech.com.br"

headers_client = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

headers_crm = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Test 1: CRM Consultor API - wallets endpoints
print("\n=== CRM CONSULTOR API ===")
crm_endpoints = [
    "/wallets/bids/config?groups=1010",
    "/wallets/lottery/draw-dates",
    "/wallets/lottery/results-by-draw-date?drawDate=2026-01-17",
    "/wallets/lottery/extraction?drawDate=2026-01-17&type=property",
    "/wallets/analysis?type=property&drawDate=2026-01-17",
    "/wallets/analysis?type=property",
    "/wallets?page=1&pageSize=10",
]

for ep in crm_endpoints:
    try:
        r = requests.get(f"{crm_api}{ep}", headers=headers_crm, timeout=15)
        print(f"\nGET {ep}")
        print(f"  Status: {r.status_code}")
        text = r.text[:800] if len(r.text) < 2000 else r.text[:800] + "..."
        print(f"  Response: {text}")
    except Exception as e:
        print(f"  Error: {e}")

# Test 2: Client API - lance endpoints
print("\n\n=== CLIENT API (ademitech) - LANCES ===")
client_endpoints = [
    ("/api/v2/lances/quota/info", "POST", {"CD_Grupo": "1010", "CD_Cota": "1", "Versao": "1"}),
    ("/api/v2/lances/quota/search", "POST", {"CD_Grupo": "1010", "CD_Cota": "1", "Versao": "1", "document": "", "name": ""}),
    ("/api/v2/lances/list?page=1&size=10", "GET", None),
    ("/offers/sells?all=true", "GET", None),
    ("/offers/inprogress", "GET", None),
]

for ep, method, body in client_endpoints:
    try:
        if method == "GET":
            r = requests.get(f"{client_api}{ep}", headers=headers_client, timeout=15)
        else:
            r = requests.post(f"{client_api}{ep}", headers=headers_client, json=body, timeout=15)
        print(f"\n{method} {ep}")
        print(f"  Status: {r.status_code}")
        text = r.text[:800] if len(r.text) < 2000 else r.text[:800] + "..."
        print(f"  Response: {text}")
    except Exception as e:
        print(f"  Error: {e}")

# Test 3: Apiv2 - products/simulations
print("\n\n=== APIv2 (ademitech) ===")
apiv2_headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
apiv2_endpoints = [
    "/api/connector/products",
    "/api/connector/groups",
]

for ep in apiv2_endpoints:
    try:
        r = requests.get(f"{apiv2}{ep}", headers=apiv2_headers, timeout=15)
        print(f"\nGET {ep}")
        print(f"  Status: {r.status_code}")
        text = r.text[:800] if len(r.text) < 2000 else r.text[:800] + "..."
        print(f"  Response: {text}")
    except Exception as e:
        print(f"  Error: {e}")
