import requests, json, time

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

def login_and_fetch(js_code, wait_after=5000):
    """Login to AVA PRO and execute JS to fetch data"""
    result = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "url": "https://avapro.ademicon.com.br/login",
            "formats": ["rawHtml"],
            "waitFor": 3000,
            "timeout": 60000,
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
        timeout=120
    )
    resp = result.json()
    if 'data' in resp:
        title = resp['data'].get('metadata', {}).get('title', '')
        return title
    return f"ERROR: {resp.get('error', 'Unknown')[:200]}"

# Step 1: Try to list available products/groups
print("=== Test 1: List groups for product 101 ===")
js1 = """
async function run() {
    try {
        const t = localStorage.getItem('token');
        const h = {'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'};
        const r = await fetch('https://apiv2.ademitech.com.br/api/connector/tenants/60d0db2552fcc900beb502d5/grupos?productId=101', {headers: h});
        const d = await r.json();
        document.title = 'OK:' + JSON.stringify(d).substring(0, 8000);
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
}
run();
"""
result = login_and_fetch(js1)
print(f"Result: {result[:500]}")

if result.startswith('ERR:') or result.startswith('ERROR:'):
    # Try different endpoint
    print("\n=== Test 2: Try /products endpoint ===")
    js2 = """
    async function run() {
        try {
            const t = localStorage.getItem('token');
            const h = {'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'};
            const r = await fetch('https://apiv2.ademitech.com.br/api/connector/products', {headers: h});
            const d = await r.json();
            document.title = 'OK:' + JSON.stringify(d).substring(0, 8000);
        } catch(e) {
            document.title = 'ERR:' + e.message;
        }
    }
    run();
    """
    result2 = login_and_fetch(js2)
    print(f"Result: {result2[:500]}")

# Try querying the simulator API FROM the browser (no WAF)
print("\n=== Test 3: Simulator API from browser ===")
js3 = """
async function run() {
    try {
        const r = await fetch('https://api-simulador.ademicon.com.br/simulations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-tenant-id': 'da4c01e8-e329-4ad2-b941-2c6418ac2db6'
            },
            body: JSON.stringify({
                segment: 'property-segment',
                value: 100000,
                valueType: 'amount'
            })
        });
        const d = await r.json();
        const groups = d.data ? d.data.map(g => g.group + ':' + g.amount) : [];
        document.title = 'SIM:' + groups.join('|');
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
}
run();
"""
result3 = login_and_fetch(js3, 3000)
print(f"Result: {result3[:500]}")
