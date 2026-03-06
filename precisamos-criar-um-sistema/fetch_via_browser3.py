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

# The apiv2 connector needs a different token.
# From the JS: za.interceptors.request.use with simulator-storage.state.noSalePlan
# Let's check what tokens exist in localStorage and try the connector with the right one
print("=== Test 1: Check all localStorage keys ===")
js1 = """
async function run() {
    try {
        const keys = Object.keys(localStorage);
        const data = {};
        keys.forEach(k => {
            const v = localStorage.getItem(k);
            data[k] = v ? v.substring(0, 200) : null;
        });
        document.title = 'KEYS:' + JSON.stringify(data).substring(0, 8000);
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
}
run();
"""
result = login_and_fetch(js1)
print(f"Result: {result[:2000]}")

# Try calling the connector with the correct interceptor setup
print("\n\n=== Test 2: Connector API with proper auth ===")
js2 = """
async function run() {
    try {
        const t = localStorage.getItem('token');
        const simStorage = JSON.parse(localStorage.getItem('simulator-storage') || '{}');
        const noSalePlan = simStorage.state ? simStorage.state.noSalePlan : false;

        // The connector API needs the token and noSalePlan param
        const url = 'https://apiv2.ademitech.com.br/api/connector/consultas/motivos_aquisicao?productId=101&noSalePlan=' + noSalePlan;
        const r = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + t,
                'Content-Type': 'application/json'
            }
        });
        const text = await r.text();
        document.title = 'RES:' + r.status + ':' + text.substring(0, 7000);
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
}
run();
"""
result2 = login_and_fetch(js2)
print(f"Result: {result2[:1000]}")

# The real approach: use the AVA PRO's own simulation endpoint
# From JS: fetchTipoNegociacao -> /tenants/{tenant}/tipopagamento/avapro
print("\n\n=== Test 3: Fetch group list from AVA PRO simulation ===")
js3 = """
async function run() {
    try {
        const t = localStorage.getItem('token');
        // Try listing deals/simulations for product 101
        const url = 'https://api-clientv2.ademitech.com.br/tenants/60d0db2552fcc900beb502d5/tipopagamento/avapro';
        const r = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + t,
                'Content-Type': 'application/json'
            }
        });
        const d = await r.json();
        document.title = 'TIPO:' + JSON.stringify(d).substring(0, 8000);
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
}
run();
"""
result3 = login_and_fetch(js3)
print(f"Result: {result3[:2000]}")
