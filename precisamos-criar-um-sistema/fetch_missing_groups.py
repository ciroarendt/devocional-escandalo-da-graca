import requests, json, time

with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt') as f:
    token = f.read().strip()

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_crm.json') as f:
    crm = json.load(f)

with open('/home/dev/workspace/precisamos-criar-um-sistema/dados_grupos.json') as f:
    sim = json.load(f)

# Get all groups from extractions that are NOT in the simulator
sim_groups = set()
for seg_key, seg_data in sim.items():
    for gid in seg_data['groups']:
        sim_groups.add(gid)

missing_groups = []
for tp in ['properties', 'vehicles']:
    latest_key = sorted(crm['extractions'][tp].keys())[-1]
    ext = crm['extractions'][tp][latest_key]
    first = ext.get('extractionFirstNumber', {}).get('extraction', {})
    for cat_letter, cat_data in first.items():
        for g in cat_data.get('groups', []):
            if g not in sim_groups:
                missing_groups.append({
                    'group': g,
                    'segment': tp,
                    'category': cat_letter,
                    'participants': cat_data.get('numberOfVacancies', 0)
                })

print(f"Missing groups: {len(missing_groups)}")

# Try CRM API endpoints that might have group details
crm_base = "https://crm-consultor.ademicon.com.br"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test: Can we get wallet data for specific groups?
# The /wallets endpoint shows quotaCredit per quota
# Let's check if we can search by group
print("\n=== Testing CRM endpoints for group data ===")

# Test wallets with quotasIds filter
test_groups = ["12164", "12152", "1010"]
for g in test_groups:
    padded = g.zfill(6)
    r = requests.get(f"{crm_base}/wallets?page=1&pageSize=10&name={padded}", headers=headers, timeout=15)
    print(f"\nGET /wallets?name={padded}: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        items = data.get('items', [])
        print(f"  Items: {len(items)}, Total: {data.get('totalItems')}")
        if items:
            print(f"  First: group={items[0].get('quotaGroup')}, credit={items[0].get('quotaCredit')}")

# Try the apiv2 connector API via Firecrawl
# The AVA PRO uses apiv2.ademitech.com.br/api/connector for products/simulations
# Let's try to access it through Firecrawl since direct calls are WAF-blocked
print("\n\n=== Testing ademitech API via Firecrawl ===")
api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# First: try to fetch group data from the AVA PRO while logged in
# The AVA PRO has a simulator page that loads group data
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
            {"type": "wait", "milliseconds": 12000},
            # Now try to fetch group data via JS in the browser context
            {"type": "executeJavascript", "script": """
                async function fetchGroups() {
                    try {
                        const token = localStorage.getItem('token');
                        const headers = {
                            'Authorization': 'Bearer ' + token,
                            'Content-Type': 'application/json'
                        };

                        // Try to fetch simulation data for product 101 (imoveis)
                        const r1 = await fetch('https://apiv2.ademitech.com.br/api/connector/products/101/simulations', {
                            method: 'GET',
                            headers: headers
                        });
                        const d1 = await r1.json();

                        document.title = 'SIMDATA:' + JSON.stringify(d1).substring(0, 5000);
                    } catch(e) {
                        document.title = 'ERROR:' + e.message;
                    }
                }
                fetchGroups();
            """},
            {"type": "wait", "milliseconds": 8000},
        ]
    },
    timeout=240
)

resp = result.json()
if 'data' in resp:
    metadata = resp['data'].get('metadata', {})
    title = metadata.get('title', '')
    print(f"Title: {title[:500]}")
else:
    print(f"Error: {resp.get('error', 'Unknown')[:300]}")
