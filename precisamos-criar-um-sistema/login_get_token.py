import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Login and extract token via JS
result = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "url": "https://avapro.ademicon.com.br/login",
        "formats": ["rawHtml"],
        "waitFor": 5000,
        "actions": [
            {"type": "wait", "milliseconds": 2000},
            {"type": "click", "selector": "input[placeholder='Matrícula']"},
            {"type": "write", "selector": "input[placeholder='Matrícula']", "text": "7118"},
            {"type": "click", "selector": "input[placeholder='Senha']"},
            {"type": "write", "selector": "input[placeholder='Senha']", "text": "Netflix@84"},
            {"type": "wait", "milliseconds": 500},
            {"type": "click", "selector": "button.bg-\\[\\#EE3124\\]"},
            {"type": "wait", "milliseconds": 15000},
            # Use scrapeOptions to inject script that writes token to DOM
            {"type": "executeJavascript", "script": "document.title = 'TOKEN:' + (localStorage.getItem('token') || 'NONE')"},
            {"type": "wait", "milliseconds": 1000},
        ]
    },
    timeout=240
)

resp = result.json()
if 'data' in resp:
    metadata = resp['data'].get('metadata', {})
    title = metadata.get('title', '')
    print(f"Title: {title[:200]}")

    if title.startswith('TOKEN:') and title != 'TOKEN:NONE':
        token = title[6:]
        print(f"\nTOKEN EXTRACTED! Length: {len(token)}")
        print(f"Token: {token[:100]}...")

        with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
            f.write(token)
        print("Token saved!")
    else:
        # Try rawHtml for token
        raw = resp['data'].get('rawHtml', '')
        print(f"Raw HTML length: {len(raw)}")

        import re
        # Check title tag in raw HTML
        title_match = re.search(r'<title>(.*?)</title>', raw)
        if title_match:
            print(f"Title from HTML: {title_match.group(1)[:200]}")

        # Try to find token in any script or meta tag
        token_patterns = re.findall(r'["\']([A-Za-z0-9_-]{100,}\.(?:[A-Za-z0-9_-]{50,})\.?[A-Za-z0-9_-]*)["\']', raw)
        if token_patterns:
            print(f"\nJWT-like patterns: {len(token_patterns)}")
            for t in token_patterns[:3]:
                print(f"  {t[:100]}...")
else:
    print(f"Error: {resp.get('error', 'Unknown')}")
