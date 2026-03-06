import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# Step 1: Login and get token
print("=== STEP 1: LOGIN ===")
actions_login = [
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
        document.title = 'LOGGING_IN';
    """},
    {"type": "wait", "milliseconds": 20000},
    {"type": "executeJavascript", "script": "document.title = 'TOKEN:' + (localStorage.getItem('token') || 'NONE') + '|URL:' + window.location.href;"},
]

payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["markdown"],
    "actions": actions_login,
    "waitFor": 5000,
    "timeout": 60000
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {FIRECRAWL_KEY}"
}

r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=120)
result = r.json()

if not result.get('success'):
    print(f"Login failed: {result.get('error', '')[:300]}")
    exit()

title = result.get('data', {}).get('metadata', {}).get('title', '')
print(f"Title: {title[:200]}")

if 'TOKEN:' not in title or 'TOKEN:NONE' in title:
    print("Login failed - no token")
    md = result.get('data', {}).get('markdown', '')
    print(f"Page: {md[:300]}")
    exit()

token = title.split('TOKEN:', 1)[1].split('|URL:')[0]
url_after = title.split('|URL:', 1)[1] if '|URL:' in title else ''
print(f"Token: {token[:50]}...")
print(f"URL after login: {url_after}")

# Save token
with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
    f.write(token)

# Step 2: Now navigate to the simulator page and fetch groups from there
print("\n=== STEP 2: FETCH GROUPS FROM SIMULATOR PAGE ===")

# Navigate to the simulator page where the app naturally loads groups
actions_fetch = [
    {"type": "wait", "milliseconds": 8000},
    {"type": "executeJavascript", "script": """
(async function() {
    try {
        var token = localStorage.getItem('token');
        if (!token) { document.title = 'NO_TOKEN_PAGE2'; return; }
        var tenant = '60d0db2552fcc900beb502d5';
        var allGroups = {};

        for (var pid of ['101', '102', '105', '106', '109', '111']) {
            try {
                var resp = await fetch('https://apiv2.ademitech.com.br/tenants/' + tenant + '/simular/grupos?product=' + pid, {
                    headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }
                });
                var data = await resp.json();
                var groups = data.data || data;
                if (Array.isArray(groups)) {
                    allGroups[pid] = { count: groups.length, status: resp.status };
                } else {
                    allGroups[pid] = { error: data.error || 'not array', status: resp.status };
                }
            } catch(e) {
                allGroups[pid] = { error: e.message };
            }
        }
        document.title = 'GROUPS:' + JSON.stringify(allGroups);
    } catch(e) {
        document.title = 'ERROR:' + e.message;
    }
})();
    """},
    {"type": "wait", "milliseconds": 15000}
]

# Navigate to the simulator page (user is already logged in)
payload2 = {
    "url": "https://avapro.ademicon.com.br/simulador",
    "formats": ["markdown"],
    "actions": actions_fetch,
    "waitFor": 5000,
    "timeout": 60000,
    "headers": {"Cookie": f"token={token}"}
}

r2 = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload2, headers=headers, timeout=120)
result2 = r2.json()

if result2.get('success'):
    title2 = result2.get('data', {}).get('metadata', {}).get('title', '')
    print(f"Result: {title2[:1000]}")

    if 'GROUPS:' in title2:
        json_str = title2.split('GROUPS:', 1)[1]
        try:
            data = json.loads(json_str)
            print(f"\nGroups per product:")
            for pid, info in data.items():
                print(f"  Product {pid}: {info}")
        except json.JSONDecodeError as e:
            print(f"JSON error: {e}")
else:
    print(f"Fetch failed: {result2.get('error', '')[:300]}")
    # Try the simulator page - maybe it redirects to login
    md = result2.get('data', {}).get('markdown', '') if result2.get('data') else ''
    print(f"Page: {md[:300]}")
