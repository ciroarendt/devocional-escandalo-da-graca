import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# Read the AVA PRO token
with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

# Use Firecrawl to execute JS in AVA PRO context and fetch groups
# The AVA PRO endpoints:
# - fetchGrupos: /tenants/60d0db2552fcc900beb502d5/simular/grupos?product={id}
# Base URL: https://apiv2.ademitech.com.br

tenant = "60d0db2552fcc900beb502d5"
base_url = "https://apiv2.ademitech.com.br"

# Try fetching directly from apiv2 with the token (it may work with proper headers)
print("=== DIRECT API CALL TO apiv2 ===")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

for pid in ["101", "102"]:
    url = f"{base_url}/tenants/{tenant}/simular/grupos?product={pid}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"\nProduct {pid}: HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and 'data' in data:
                print(f"  data: {len(data['data'])} items")
            elif isinstance(data, list):
                print(f"  {len(data)} groups")
            else:
                print(f"  Response: {str(data)[:300]}")
        else:
            print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

# Also try bifrost (login API)
print("\n\n=== DIRECT API CALL TO bifrost ===")
bifrost = "https://bifrost.ademitech.com.br"
for pid in ["101"]:
    url = f"{bifrost}/tenants/{tenant}/simular/grupos?product={pid}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"\nBifrost Product {pid}: HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  Response: {str(data)[:500]}")
        else:
            print(f"  Response: {r.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")

# Try api-clientv2
print("\n\n=== DIRECT API CALL TO api-clientv2 ===")
clientv2 = "https://api-clientv2.ademitech.com.br"
for pid in ["101"]:
    url = f"{clientv2}/tenants/{tenant}/simular/grupos?product={pid}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"\nclientv2 Product {pid}: HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  Response: {str(data)[:500]}")
        else:
            print(f"  Response: {r.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")
