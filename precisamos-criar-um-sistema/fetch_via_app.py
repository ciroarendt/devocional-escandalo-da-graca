import requests
import json

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# Login then navigate to the simulator page and intercept the API calls
print("=== LOGIN + NAVIGATE TO SIMULATOR ===")

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
            buttons.forEach(function(btn) { if (btn.textContent.trim() === 'Entrar') btn.click(); });
        }
    """},
    {"type": "wait", "milliseconds": 18000},
    # Intercept fetch calls and then navigate to simulator
    {"type": "executeJavascript", "script": """
        // Monkey-patch fetch to capture API calls
        window.__apiCalls = [];
        var origFetch = window.fetch;
        window.fetch = function(url, opts) {
            window.__apiCalls.push({url: url, method: (opts && opts.method) || 'GET'});
            return origFetch.apply(this, arguments);
        };
        // Navigate to simulator
        window.location.href = '/simulador';
    """},
    {"type": "wait", "milliseconds": 10000},
    # Check what API calls were made
    {"type": "executeJavascript", "script": """
        var calls = window.__apiCalls || [];
        document.title = 'CALLS:' + JSON.stringify(calls.map(function(c) { return c.url; }));
    """},
    {"type": "wait", "milliseconds": 3000}
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

    if 'CALLS:' in title:
        json_str = title.split('CALLS:', 1)[1]
        try:
            calls = json.loads(json_str)
            print(f"\nAPI calls intercepted ({len(calls)}):")
            for url in calls:
                print(f"  {url}")
        except:
            print(f"Raw: {json_str[:1000]}")

    md = result.get('data', {}).get('markdown', '')
    print(f"\nPage (300): {md[:300]}")
else:
    print(f"Error: {result.get('error', '')[:500]}")
