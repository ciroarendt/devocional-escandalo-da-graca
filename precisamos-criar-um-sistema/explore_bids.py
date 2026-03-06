import requests, json

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

crm = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Try bids config with different parameter formats
print("=== BIDS CONFIG - Various formats ===")
tests = [
    "/wallets/bids/config?groups=001010",
    "/wallets/bids/config?groups=1010,860,870",
    "/wallets/bids/config?groups=001010,000860",
    "/wallets/bids/config?groups[]=1010&groups[]=860",
    "/wallets/bids/config",
]
for ep in tests:
    r = requests.get(f"{crm}{ep}", headers=headers, timeout=15)
    print(f"\nGET {ep}")
    print(f"  Status: {r.status_code}, Response: {r.text[:300]}")

# Try POST instead of GET
print("\n=== BIDS CONFIG - POST ===")
r = requests.post(f"{crm}/wallets/bids/config", headers=headers,
                   json={"groups": ["1010", "860"]}, timeout=15)
print(f"POST /wallets/bids/config: {r.status_code}")
print(f"  Response: {r.text[:300]}")

# Try analysis with range to find more data
print("\n=== ANALYSIS WITH RANGE ===")
for min_r, max_r in [(0, 10), (0, 50), (0, 100), (0, 500), (-500, 500)]:
    r = requests.get(
        f"{crm}/wallets/analysis?drawDate=2026-02-21&type=properties&minRange={min_r}&maxRange={max_r}",
        headers=headers, timeout=15
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  Range [{min_r},{max_r}]: {len(data)} items")
        if data:
            # Show prize statuses
            statuses = {}
            for item in data:
                ps = item.get('prizeStatus', {})
                key = f"status={ps.get('status')}|lance={ps.get('lanceType')}|label={ps.get('label','')[:50]}"
                statuses[key] = statuses.get(key, 0) + 1
            for k, v in sorted(statuses.items()):
                print(f"    {k}: {v}x")

# Try to discover other endpoints by testing common patterns
print("\n=== DISCOVERING MORE ENDPOINTS ===")
other_endpoints = [
    "/wallets/bids",
    "/wallets/bids/history",
    "/wallets/bids/results",
    "/wallets/contemplated",
    "/wallets/contemplations",
    "/wallets/groups",
    "/wallets/groups/1010",
    "/wallets/lottery/history",
    "/wallets/statistics",
    "/wallets/summary",
]
for ep in other_endpoints:
    r = requests.get(f"{crm}{ep}", headers=headers, timeout=10)
    if r.status_code != 404:
        print(f"\nGET {ep}: {r.status_code}")
        print(f"  Response: {r.text[:300]}")
