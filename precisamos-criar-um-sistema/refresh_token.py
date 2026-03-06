import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# Login to AVA PRO and extract fresh token
print("=== REFRESHING AVA PRO TOKEN ===")

actions = [
    {"type": "wait", "milliseconds": 5000},
    # First screenshot to see what's on the page
    {"type": "screenshot"},
    {"type": "click", "selector": "input"},
    {"type": "write", "text": "7118"},
    {"type": "press", "key": "Tab"},
    {"type": "write", "text": "Netflix@84"},
    {"type": "press", "key": "Enter"},
    {"type": "wait", "milliseconds": 15000},
    {"type": "executeJavascript", "script": "document.title = 'TOKEN:' + (localStorage.getItem('token') || 'NONE');"},
    {"type": "wait", "milliseconds": 2000}
]

payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["markdown", "screenshot@fullPage"],
    "actions": actions,
    "waitFor": 5000,
    "timeout": 60000
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {FIRECRAWL_KEY}"
}

r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=180)
result = r.json()

if result.get('success'):
    metadata = result.get('data', {}).get('metadata', {})
    title = metadata.get('title', '')

    if 'TOKEN:' in title and title.split('TOKEN:', 1)[1] != 'NONE':
        token = title.split('TOKEN:', 1)[1]
        print(f"Got token! Length: {len(token)}")
        print(f"Token prefix: {token[:50]}...")

        # Save token
        with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
            f.write(token)
        print("Token saved!")

        # Test it immediately
        print("\n=== TESTING TOKEN ===")
        tenant = "60d0db2552fcc900beb502d5"
        test_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        for pid in ["101", "102"]:
            url = f"https://apiv2.ademitech.com.br/tenants/{tenant}/simular/grupos?product={pid}"
            try:
                resp = requests.get(url, headers=test_headers, timeout=15)
                print(f"\nProduct {pid}: HTTP {resp.status_code}")
                if resp.status_code == 200:
                    data = resp.json()
                    groups = data.get('data', data)
                    if isinstance(groups, list):
                        print(f"  {len(groups)} groups!")
                        if groups:
                            print(f"  First: {json.dumps(groups[0], ensure_ascii=False)[:300]}")
                    else:
                        print(f"  Response: {str(data)[:300]}")
                else:
                    print(f"  Response: {resp.text[:300]}")
            except Exception as e:
                print(f"  Error: {e}")
    else:
        print(f"No token found. Title: {title[:200]}")
        md = result.get('data', {}).get('markdown', '')
        print(f"Page content: {md[:500]}")
else:
    print(f"Firecrawl error: {json.dumps(result, indent=2)[:500]}")
