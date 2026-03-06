import requests, json

base = "https://crm-consultor.ademicon.com.br"

# Check security schemes from spec
spec = json.load(open('/home/dev/workspace/precisamos-criar-um-sistema/crm_api_spec.json'))
security_schemes = spec.get('components', {}).get('securitySchemes', {})
print("Security schemes:")
print(json.dumps(security_schemes, indent=2))
print(f"\nGlobal security: {spec.get('security', 'none')}")

# Test wallets endpoints without auth
endpoints = [
    "/wallets",
    "/wallets/bids/config?groups=1010",
    "/wallets/lottery/draw-dates",
    "/wallets/lottery/results-by-draw-date?drawDate=2026-01-17",
    "/wallets/lottery/extraction?drawDate=2026-01-17&type=property",
    "/wallets/analysis?drawDate=2026-01-17&type=property",
]

for ep in endpoints:
    r = requests.get(f"{base}{ep}", timeout=10)
    print(f"\nGET {ep}")
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.text[:300]}")
