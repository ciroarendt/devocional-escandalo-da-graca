import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

def login_and_fetch(js_code, wait_after=5000):
    result = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "url": "https://avapro.ademicon.com.br/login",
            "formats": ["rawHtml"],
            "waitFor": 3000,
            "timeout": 90000,
            "actions": [
                {"type": "wait", "milliseconds": 2000},
                {"type": "click", "selector": "input[placeholder='Matrícula']"},
                {"type": "write", "selector": "input[placeholder='Matrícula']", "text": "7118"},
                {"type": "click", "selector": "input[placeholder='Senha']"},
                {"type": "write", "selector": "input[placeholder='Senha']", "text": "Netflix@84"},
                {"type": "wait", "milliseconds": 500},
                {"type": "click", "selector": "button.bg-\\[\\#EE3124\\]"},
                {"type": "wait", "milliseconds": 10000},
                {"type": "executeJavascript", "script": js_code},
                {"type": "wait", "milliseconds": wait_after},
            ]
        },
        timeout=180
    )
    resp = result.json()
    if 'data' in resp:
        return resp['data'].get('metadata', {}).get('title', '')
    return f"ERROR: {resp.get('error', 'Unknown')[:200]}"

# The AVA PRO uses these API patterns found in the JS bundle:
# - Xn.create({baseURL:"https://api-clientv2.ademitech.com.br"})
# - za = Xn.create({baseURL:"https://apiv2.ademitech.com.br/api/connector"})
# - Sme = Xn.create({baseURL:"https://apiv2.ademitech.com.br/api/ecommerce"})

# Try the connector API with different paths for group listings
endpoints_to_try = [
    'https://apiv2.ademitech.com.br/api/connector/consultas/motivos_aquisicao?productId=101',
    'https://apiv2.ademitech.com.br/api/connector/products/101/offers',
    'https://apiv2.ademitech.com.br/api/connector/products/101/groups',
    'https://apiv2.ademitech.com.br/api/connector/products/101/simulations',
    'https://api-clientv2.ademitech.com.br/api/v2/lances/quota/search',
]

for i, endpoint in enumerate(endpoints_to_try):
    print(f"\n=== Test {i+1}: {endpoint.split('.com.br')[-1]} ===")

    if 'quota/search' in endpoint:
        # POST with body
        js = f"""
        async function run() {{
            try {{
                const t = localStorage.getItem('token');
                const r = await fetch('{endpoint}', {{
                    method: 'POST',
                    headers: {{'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'}},
                    body: JSON.stringify({{CD_Grupo: '1010', CD_Cota: '1', Versao: '1', document: '', name: ''}})
                }});
                const d = await r.json();
                document.title = 'OK:' + JSON.stringify(d).substring(0, 8000);
            }} catch(e) {{
                document.title = 'ERR:' + e.message;
            }}
        }}
        run();
        """
    else:
        js = f"""
        async function run() {{
            try {{
                const t = localStorage.getItem('token');
                const r = await fetch('{endpoint}', {{
                    headers: {{'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'}}
                }});
                const d = await r.json();
                document.title = 'OK:' + JSON.stringify(d).substring(0, 8000);
            }} catch(e) {{
                document.title = 'ERR:' + e.message;
            }}
        }}
        run();
        """

    result = login_and_fetch(js)
    print(f"Result: {result[:800]}")
