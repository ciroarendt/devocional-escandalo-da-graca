import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

def scrape_with_actions(url, actions, wait_for=3000):
    payload = {
        "url": url,
        "formats": ["markdown"],
        "actions": actions,
        "waitFor": wait_for
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIRECRAWL_KEY}"
    }
    r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=180)
    return r.json()

# Login to AVA PRO then fetch groups - all in one Firecrawl call
print("=== LOGIN + FETCH GROUPS ===")

# Login actions
actions = [
    {"type": "wait", "milliseconds": 5000},
    {"type": "click", "selector": "input[type='text']"},
    {"type": "write", "text": "7118"},
    {"type": "click", "selector": "input[type='password']"},
    {"type": "write", "text": "Netflix@84"},
    {"type": "click", "selector": "button[type='button']"},
    {"type": "wait", "milliseconds": 12000},
    # After login, fetch groups for all products
    {"type": "executeJavascript", "script": """
(async function() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            document.title = 'NO_TOKEN_AFTER_LOGIN';
            return;
        }
        const tenant = '60d0db2552fcc900beb502d5';
        const results = {};

        for (const pid of ['101', '102', '105', '106', '109', '111']) {
            try {
                const resp = await fetch('https://apiv2.ademitech.com.br/tenants/' + tenant + '/simular/grupos?product=' + pid, {
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    }
                });
                const data = await resp.json();
                const groups = data.data || data;
                results[pid] = {
                    status: resp.status,
                    count: Array.isArray(groups) ? groups.length : 0,
                    error: data.error || null
                };
            } catch(e) {
                results[pid] = {error: e.message};
            }
        }

        document.title = 'RESULTS:' + JSON.stringify(results);
    } catch(e) {
        document.title = 'ERROR:' + e.message;
    }
})();
"""},
    {"type": "wait", "milliseconds": 15000}
]

result = scrape_with_actions("https://avapro.ademicon.com.br/login", actions, wait_for=5000)

if result.get('success'):
    metadata = result.get('data', {}).get('metadata', {})
    title = metadata.get('title', '')
    print(f"Title: {title[:1000]}")

    if 'RESULTS:' in title:
        json_str = title.split('RESULTS:', 1)[1]
        try:
            data = json.loads(json_str)
            print(f"\nResults per product:")
            for pid, info in data.items():
                print(f"  Product {pid}: {info}")
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
    elif 'NO_TOKEN' in title:
        print("Login failed - no token")
    elif 'ERROR:' in title:
        print(f"Error: {title}")
else:
    print(f"Firecrawl error: {json.dumps(result, indent=2)[:500]}")

# If results show groups, do a second call to get full data for product 101
# We'll do this in the next step
