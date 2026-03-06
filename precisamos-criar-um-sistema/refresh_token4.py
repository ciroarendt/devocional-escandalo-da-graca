import requests
import json

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

print("=== LOGIN TO AVA PRO (attempt 4) ===")

# Use executeJavascript to fill the form and submit it programmatically
actions = [
    {"type": "wait", "milliseconds": 5000},
    {"type": "executeJavascript", "script": """
        // Fill in the matricula
        var matInput = document.querySelector("input[placeholder='Matrícula']");
        var senhaInput = document.querySelector("input[placeholder='Senha']");
        if (matInput && senhaInput) {
            // Use React's internal setter to trigger proper state updates
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(matInput, '7118');
            matInput.dispatchEvent(new Event('input', { bubbles: true }));
            matInput.dispatchEvent(new Event('change', { bubbles: true }));
            nativeInputValueSetter.call(senhaInput, 'Netflix@84');
            senhaInput.dispatchEvent(new Event('input', { bubbles: true }));
            senhaInput.dispatchEvent(new Event('change', { bubbles: true }));
            // Find and click the submit button
            var buttons = document.querySelectorAll('button');
            var entrarBtn = null;
            buttons.forEach(function(btn) {
                if (btn.textContent.trim() === 'Entrar') entrarBtn = btn;
            });
            if (entrarBtn) {
                entrarBtn.click();
                document.title = 'CLICKED_ENTRAR';
            } else {
                document.title = 'NO_ENTRAR_BTN:' + buttons.length + ' buttons found';
            }
        } else {
            document.title = 'NO_INPUTS:mat=' + !!matInput + ',senha=' + !!senhaInput;
        }
    """},
    {"type": "wait", "milliseconds": 15000},
    {"type": "executeJavascript", "script": "document.title = 'TOKEN:' + (localStorage.getItem('token') || 'NONE');"},
    {"type": "wait", "milliseconds": 2000}
]

payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["markdown"],
    "actions": actions,
    "waitFor": 5000,
    "timeout": 60000
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {FIRECRAWL_KEY}"
}

r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=180)
result = r.json()

if result.get('success'):
    metadata = result.get('data', {}).get('metadata', {})
    title = metadata.get('title', '')
    print(f"Title: {title[:500]}")

    if 'TOKEN:' in title and title.split('TOKEN:', 1)[1] != 'NONE':
        token = title.split('TOKEN:', 1)[1]
        print(f"\nGot token! Length: {len(token)}")

        with open('/home/dev/workspace/precisamos-criar-um-sistema/avapro_token.txt', 'w') as f:
            f.write(token)
        print("Token saved!")

        # Immediately test with apiv2
        print("\n=== TESTING TOKEN ===")
        tenant = "60d0db2552fcc900beb502d5"
        test_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        for pid in ["101", "102"]:
            url = f"https://apiv2.ademitech.com.br/tenants/{tenant}/simular/grupos?product={pid}"
            try:
                resp = requests.get(url, headers=test_headers, timeout=15)
                print(f"Product {pid}: HTTP {resp.status_code} - {resp.text[:300]}")
            except Exception as e:
                print(f"Product {pid}: Error: {e}")
    elif 'NONE' in title:
        print("Login did not work - no token in localStorage")
    else:
        print(f"Unexpected result")

    md = result.get('data', {}).get('markdown', '')
    print(f"\nPage (first 300): {md[:300]}")
else:
    print(f"Firecrawl error: {result.get('error', '')[:300]}")
