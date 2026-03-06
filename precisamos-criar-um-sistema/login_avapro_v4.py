import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Login to AVA PRO - skip the JS execution that causes errors
# Just get the page HTML after login to verify it worked
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
            {"type": "click", "selector": "button.bg-\\[\\#EE3124\\]"},
            {"type": "wait", "milliseconds": 12000},
            {"type": "screenshot"}
        ]
    },
    timeout=240
)

resp = result.json()
print(f"Status: {result.status_code}")

if 'data' in resp:
    html = resp['data'].get('html', '')
    metadata = resp['data'].get('metadata', {})
    actions_result = resp['data'].get('actions', {})

    print(f"HTML length: {len(html)}")
    print(f"Final URL: {metadata.get('url', metadata.get('sourceURL', '?'))}")
    print(f"Title: {metadata.get('title', '?')}")

    # Check if screenshot was taken
    if actions_result and 'screenshots' in actions_result:
        print(f"Screenshots: {len(actions_result['screenshots'])}")

    # Look for indicators of login success
    indicators = ['dashboard', 'home', 'bem-vindo', 'carlos', 'sair', 'logout', 'menu']
    for ind in indicators:
        if ind.lower() in html.lower():
            print(f"  Found '{ind}' in HTML - LOGIN LIKELY SUCCESSFUL!")

    # Print HTML snippet
    print(f"\nHTML preview (first 2000 chars):")
    print(html[:2000])

    # Look for token-related data in HTML
    import re
    token_patterns = re.findall(r'(?:token|jwt|Bearer)["\s:=]+["\']?([A-Za-z0-9._-]{20,})', html)
    if token_patterns:
        print(f"\nToken-like patterns found: {len(token_patterns)}")
        for t in token_patterns[:3]:
            print(f"  {t[:80]}...")
else:
    error = resp.get('error', 'Unknown error')
    print(f"Error: {error}")
