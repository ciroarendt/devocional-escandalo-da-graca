import requests, json

# Try to login to AVA PRO with the CRM credentials
base = "https://api-clientv2.ademitech.com.br"

# Login endpoint found in JS: /users/v4/login?origin=avaweb
login_data = {
    "identifier": "carlos.felipe",
    "password": "netflix123"
}

r = requests.post(
    f"{base}/users/v4/login?origin=avaweb",
    json=login_data,
    timeout=15
)
print(f"Login attempt 1 (carlos.felipe): {r.status_code}")
print(f"  Response: {r.text[:500]}")

# Try with just "carlos" as identifier
login_data2 = {
    "identifier": "carlos",
    "password": "netflix123"
}
r2 = requests.post(
    f"{base}/users/v4/login?origin=avaweb",
    json=login_data2,
    timeout=15
)
print(f"\nLogin attempt 2 (carlos): {r2.status_code}")
print(f"  Response: {r2.text[:500]}")

# Also try the main ademitech API
base2 = "https://apiv2.ademitech.com.br"
r3 = requests.post(
    f"{base2}/users/v4/login?origin=avaweb",
    json=login_data,
    timeout=15
)
print(f"\nLogin attempt 3 (apiv2): {r3.status_code}")
print(f"  Response: {r3.text[:500]}")
