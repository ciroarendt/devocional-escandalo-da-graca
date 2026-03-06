import requests
import json

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# All-in-one: login + fetch groups for product 101
print("=== LOGIN + FETCH PRODUCT 101 ===")

actions = [
    {"type": "wait", "milliseconds": 5000},
    {"type": "executeJavascript", "script": """
        var matInput = document.querySelector("input[placeholder='Matrícula']");
        var senhaInput = document.querySelector("input[placeholder='Senha']");
        if (matInput && senhaInput) {
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(matInput, '7118');
            matInput.dispatchEvent(new Event('input', { bubbles: true }));
            matInput.dispatchEvent(new Event('change', { bubbles: true }));
            nativeInputValueSetter.call(senhaInput, 'Netflix@84');
            senhaInput.dispatchEvent(new Event('input', { bubbles: true }));
            senhaInput.dispatchEvent(new Event('change', { bubbles: true }));
            var buttons = document.querySelectorAll('button');
            var entrarBtn = null;
            buttons.forEach(function(btn) { if (btn.textContent.trim() === 'Entrar') entrarBtn = btn; });
            if (entrarBtn) entrarBtn.click();
        }
    """},
    {"type": "wait", "milliseconds": 18000},
    # Now fetch groups using the token from localStorage
    {"type": "executeJavascript", "script": """
(async function() {
    try {
        var token = localStorage.getItem('token');
        if (!token) {
            document.title = 'NO_TOKEN';
            return;
        }
        var tenant = '60d0db2552fcc900beb502d5';
        var resp = await fetch('https://apiv2.ademitech.com.br/tenants/' + tenant + '/simular/grupos?product=101', {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
        });
        var text = await resp.text();
        if (resp.status === 200) {
            var data = JSON.parse(text);
            var groups = data.data || data;
            if (Array.isArray(groups)) {
                var summary = groups.map(function(g) {
                    return g.cd_grupo || g.group || g.name || g._id || 'unknown';
                });
                document.title = 'OK:' + groups.length + ':' + summary.join(',');
            } else {
                document.title = 'NOTARR:' + text.substring(0, 400);
            }
        } else {
            document.title = 'HTTP' + resp.status + ':' + text.substring(0, 400);
        }
    } catch(e) {
        document.title = 'ERR:' + e.message;
    }
})();
    """},
    {"type": "wait", "milliseconds": 10000}
]

payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["markdown"],
    "actions": actions,
    "waitFor": 3000,
    "timeout": 90000
}
headers_fc = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {FIRECRAWL_KEY}"
}

r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers_fc, timeout=200)
result = r.json()

if result.get('success'):
    title = result.get('data', {}).get('metadata', {}).get('title', '')
    print(f"Title (first 2000): {title[:2000]}")

    if title.startswith('OK:'):
        parts = title.split(':', 2)
        count = parts[1]
        groups_str = parts[2] if len(parts) > 2 else ''
        print(f"\nGroups found: {count}")
        print(f"Group names: {groups_str[:500]}")
    elif title.startswith('HTTP'):
        print(f"\nAPI Error: {title[:500]}")
    elif title == 'NO_TOKEN':
        print("\nLogin failed - no token in localStorage")
    else:
        print(f"\nUnexpected: {title[:500]}")

    md = result.get('data', {}).get('markdown', '')
    # Check if page redirected (login succeeded)
    if 'simulador' in md.lower() or 'dashboard' in md.lower():
        print(f"\nPage looks like post-login content")
    else:
        print(f"\nPage (300): {md[:300]}")
else:
    print(f"Firecrawl error: {result.get('error', '')[:500]}")
