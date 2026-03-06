import requests
import json

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

print("=== LOGIN TO AVA PRO ===")

actions = [
    {"type": "wait", "milliseconds": 5000},
    {"type": "click", "selector": "input[placeholder='Matrícula']"},
    {"type": "write", "text": "7118"},
    {"type": "click", "selector": "input[placeholder='Senha']"},
    {"type": "write", "text": "Netflix@84"},
    # The Entrar button - it's the button with class containing bg-[#EE3124]
    {"type": "click", "selector": "button.bg-\\[\\#EE3124\\]"},
    {"type": "wait", "milliseconds": 15000},
    {"type": "executeJavascript", "script": "document.title = 'TOKEN:' + (localStorage.getItem('token') || 'NONE');"},
    {"type": "wait", "milliseconds": 2000}
]

payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["markdown"],
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
        print(f"Token prefix: {token[:80]}...")

        with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
            f.write(token)
        print("Token saved to avapro_token.txt")
    else:
        print(f"Login may have failed. Title: {title[:200]}")
        md = result.get('data', {}).get('markdown', '')
        print(f"Page: {md[:300]}")
else:
    err = result.get('error', '')
    print(f"Firecrawl error: {err[:300]}")

    # If button selector failed, try finding it
    if 'not found' in err.lower():
        print("\nTrying to get page HTML to debug button selector...")
        payload2 = {
            "url": "https://avapro.ademicon.com.br/login",
            "formats": ["html"],
            "actions": [
                {"type": "wait", "milliseconds": 5000},
                {"type": "click", "selector": "input[placeholder='Matrícula']"},
                {"type": "write", "text": "7118"},
                {"type": "click", "selector": "input[placeholder='Senha']"},
                {"type": "write", "text": "Netflix@84"},
            ],
            "waitFor": 3000
        }
        r2 = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload2, headers=headers, timeout=60)
        result2 = r2.json()
        if result2.get('success'):
            html = result2.get('data', {}).get('html', '')
            import re
            buttons = re.findall(r'<button[^>]*class="[^"]*"[^>]*>', html)
            print(f"Buttons after filling form:")
            for btn in buttons:
                print(f"  {btn[:200]}")
