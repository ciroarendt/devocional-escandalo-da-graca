import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

def login_and_execute(js_code):
    """Login to AVA PRO and execute JS code, return title"""
    actions = [
        {"type": "wait", "milliseconds": 5000},
        {"type": "executeJavascript", "script": """
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            var matInput = document.querySelector("input[placeholder='Matrícula']");
            var senhaInput = document.querySelector("input[placeholder='Senha']");
            nativeInputValueSetter.call(matInput, '7118');
            matInput.dispatchEvent(new Event('input', { bubbles: true }));
            matInput.dispatchEvent(new Event('change', { bubbles: true }));
            nativeInputValueSetter.call(senhaInput, 'Netflix@84');
            senhaInput.dispatchEvent(new Event('input', { bubbles: true }));
            senhaInput.dispatchEvent(new Event('change', { bubbles: true }));
            var buttons = document.querySelectorAll('button');
            buttons.forEach(function(btn) { if (btn.textContent.trim() === 'Entrar') btn.click(); });
        """},
        {"type": "wait", "milliseconds": 15000},
        {"type": "executeJavascript", "script": js_code},
        {"type": "wait", "milliseconds": 5000}
    ]

    payload = {
        "url": "https://avapro.ademicon.com.br/login",
        "formats": ["markdown"],
        "actions": actions,
        "waitFor": 5000,
        "timeout": 90000
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIRECRAWL_KEY}"
    }

    r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=180)
    result = r.json()

    if result.get('success'):
        title = result.get('data', {}).get('metadata', {}).get('title', '')
        return title
    else:
        return f"ERROR:{result.get('error', '')}"

# Fetch groups for product 101 (imoveis)
print("=== FETCHING GROUPS FOR PRODUCT 101 (IMOVEIS) ===")

js_fetch_101 = """
(async function() {
    try {
        var token = localStorage.getItem('token');
        if (!token) { document.title = 'NO_TOKEN'; return; }
        var tenant = '60d0db2552fcc900beb502d5';
        var resp = await fetch('https://apiv2.ademitech.com.br/tenants/' + tenant + '/simular/grupos?product=101', {
            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }
        });
        var text = await resp.text();
        // Title has 1MB limit, so just extract counts and first groups
        try {
            var data = JSON.parse(text);
            var groups = data.data || data;
            if (Array.isArray(groups)) {
                // Extract just essential fields: id_grupo, cd_grupo, st_situacao, vl_credito etc
                var summary = groups.map(function(g) {
                    return {
                        id: g.id_grupo || g._id,
                        cd: g.cd_grupo || g.group,
                        nm: g.nm_grupo || g.name,
                        sit: g.st_situacao || g.status,
                        cred: g.vl_credito || g.amount
                    };
                });
                document.title = 'DATA:' + JSON.stringify({count: groups.length, groups: summary.slice(0, 20), fullFirst: groups[0]});
            } else {
                document.title = 'NOTARRAY:' + text.substring(0, 500);
            }
        } catch(pe) {
            document.title = 'PARSE_ERR:' + resp.status + ':' + text.substring(0, 300);
        }
    } catch(e) {
        document.title = 'FETCH_ERR:' + e.message;
    }
})();
"""

title = login_and_execute(js_fetch_101)
print(f"Result: {title[:2000]}")

if 'DATA:' in title:
    json_str = title.split('DATA:', 1)[1]
    try:
        data = json.loads(json_str)
        print(f"\nGroups count: {data.get('count')}")
        print(f"\nFirst 5 groups:")
        for g in data.get('groups', [])[:5]:
            print(f"  {g}")
        print(f"\nFull first group:")
        print(json.dumps(data.get('fullFirst', {}), indent=2, ensure_ascii=False)[:1000])
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
