import requests
import json
import time

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

def scrape_with_js(url, js_code, wait_ms=5000):
    """Use Firecrawl to navigate to URL and execute JS"""
    payload = {
        "url": url,
        "formats": ["markdown"],
        "actions": [
            {"type": "wait", "milliseconds": wait_ms},
            {"type": "executeJavascript", "script": js_code}
        ],
        "waitFor": 3000
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIRECRAWL_KEY}"
    }
    r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=120)
    return r.json()

# Navigate to AVA PRO simulator page and fetch groups via browser JS
# First, let's login and then call the API from within the browser

# Step 1: Login to AVA PRO
print("=== STEP 1: LOGIN AND FETCH GROUPS ===")

login_js = """
(async function() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            document.title = 'NO_TOKEN';
            return;
        }
        const tenant = '60d0db2552fcc900beb502d5';
        const resp = await fetch('https://apiv2.ademitech.com.br/tenants/' + tenant + '/simular/grupos?product=101', {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
        });
        const data = await resp.json();
        const groups = data.data || data;
        document.title = 'GROUPS:' + JSON.stringify({
            count: Array.isArray(groups) ? groups.length : 'not-array',
            sample: Array.isArray(groups) ? groups.slice(0, 3) : groups,
            status: resp.status
        });
    } catch(e) {
        document.title = 'ERROR:' + e.message;
    }
})();
"""

result = scrape_with_js("https://avapro.ademicon.com.br/simulador", login_js, wait_ms=8000)

if result.get('success'):
    md = result.get('data', {}).get('markdown', '')
    metadata = result.get('data', {}).get('metadata', {})
    title = metadata.get('title', '')
    print(f"Title: {title[:500]}")
    if 'GROUPS:' in title:
        json_str = title.split('GROUPS:', 1)[1]
        try:
            data = json.loads(json_str)
            print(f"\nGroups count: {data.get('count')}")
            print(f"Status: {data.get('status')}")
            sample = data.get('sample', [])
            if isinstance(sample, list):
                for g in sample:
                    print(f"\n  Group: {json.dumps(g, ensure_ascii=False)[:400]}")
            else:
                print(f"Sample: {json.dumps(sample, ensure_ascii=False)[:500]}")
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Raw: {json_str[:500]}")
    elif 'NO_TOKEN' in title:
        print("No token in localStorage - need to login first")
    else:
        print(f"Unexpected title: {title[:200]}")
        print(f"Page markdown (first 300): {md[:300]}")
else:
    print(f"Firecrawl error: {result}")
