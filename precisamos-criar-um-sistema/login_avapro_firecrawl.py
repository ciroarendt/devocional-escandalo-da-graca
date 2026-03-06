import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Use Firecrawl to login to AVA PRO via browser automation
result = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "url": "https://avapro.ademicon.com.br/login",
        "formats": ["html"],
        "waitFor": 5000,
        "actions": [
            {"type": "wait", "milliseconds": 3000},
            {"type": "write", "selector": "input[placeholder='Matrícula']", "text": "7118"},
            {"type": "write", "selector": "input[placeholder='Senha']", "text": "Netflix@84"},
            {"type": "wait", "milliseconds": 1000},
            {"type": "click", "selector": "button[type='submit']"},
            {"type": "wait", "milliseconds": 8000},
            {"type": "executeJavascript", "script": "return JSON.stringify({token: localStorage.getItem('token'), url: window.location.href, keys: Object.keys(localStorage)})"}
        ]
    },
    timeout=180
)

resp = result.json()
print(f"Status: {result.status_code}")

if 'data' in resp:
    html = resp['data'].get('html', '')
    metadata = resp['data'].get('metadata', {})
    actions_result = resp['data'].get('actions', {})

    print(f"HTML length: {len(html)}")
    print(f"Metadata: {json.dumps(metadata, indent=2)[:500]}")
    print(f"Actions result: {json.dumps(actions_result, indent=2)[:1000]}")

    # Check for token in the page
    if 'token' in html.lower():
        import re
        tokens = re.findall(r'token["\s:=]+["\']([^"\']+)["\']', html)
        if tokens:
            print(f"\nTokens found: {tokens[:3]}")

    # Print page title/URL from metadata
    print(f"\nFinal URL: {metadata.get('url', metadata.get('sourceURL', '?'))}")
    print(f"Title: {metadata.get('title', '?')}")

    # Print first 1000 chars of HTML to understand the page
    print(f"\nHTML preview:")
    print(html[:1500])
else:
    print(f"Error: {json.dumps(resp, indent=2)[:1000]}")
