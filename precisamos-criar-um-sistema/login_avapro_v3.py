import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Login to AVA PRO with correct selectors
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
            {"type": "wait", "milliseconds": 10000},
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
    print(f"Final URL: {metadata.get('url', metadata.get('sourceURL', '?'))}")
    print(f"Title: {metadata.get('title', '?')}")
    print(f"Actions result: {json.dumps(actions_result, indent=2, ensure_ascii=False)[:2000]}")

    # Check for logged-in state
    if 'token' in str(actions_result).lower() or 'dashboard' in html.lower() or 'home' in metadata.get('url', '').lower():
        print("\nLOGIN SUCCESSFUL!")

        # Extract token from actions result
        if 'results' in actions_result:
            for r_item in actions_result['results']:
                if isinstance(r_item, str) and 'token' in r_item:
                    try:
                        data = json.loads(r_item)
                        token = data.get('token')
                        if token:
                            print(f"Token: {token[:80]}...")
                            with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
                                f.write(token)
                    except:
                        pass
    else:
        print("\nLogin may have failed.")
        print(f"HTML preview: {html[:1000]}")
else:
    error = resp.get('error', 'Unknown error')
    print(f"Error: {error}")
    print(f"Full response: {json.dumps(resp, indent=2)[:1000]}")
