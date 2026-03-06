import requests, json

base = "https://api-clientv2.ademitech.com.br"

# Login to AVA PRO
login_data = {
    "identifier": "7118",
    "password": "Netflix@84"
}

# Try login
r = requests.post(
    f"{base}/users/v4/login",
    params={"origin": "avaweb"},
    json=login_data,
    timeout=15
)
print(f"Login status: {r.status_code}")
print(f"Response: {r.text[:1000]}")

if r.status_code == 200:
    data = r.json()
    token = data.get("token") or data.get("data", {}).get("token")
    if token:
        print(f"\nToken obtained! Length: {len(token)}")
        print(f"Token preview: {token[:50]}...")

        # Save token for later use
        with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
            f.write(token)

        # Test wallets endpoints on CRM API
        crm_base = "https://crm-consultor.ademicon.com.br"
        headers = {"Authorization": f"Bearer {token}"}

        endpoints = [
            "/wallets/bids/config?groups=1010",
            "/wallets/lottery/draw-dates",
            "/wallets/analysis?type=property",
        ]

        for ep in endpoints:
            r2 = requests.get(f"{crm_base}{ep}", headers=headers, timeout=15)
            print(f"\nGET {ep}")
            print(f"  Status: {r2.status_code}")
            print(f"  Response: {r2.text[:500]}")
    else:
        print(f"\nFull response: {json.dumps(data, indent=2, ensure_ascii=False)[:2000]}")
