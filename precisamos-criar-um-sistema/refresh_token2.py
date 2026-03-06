import requests
import json

FIRECRAWL_KEY = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"
FIRECRAWL_URL = "https://api.firecrawl.dev/v1"

# First just get the HTML to see the form structure
print("=== GETTING LOGIN PAGE HTML ===")
payload = {
    "url": "https://avapro.ademicon.com.br/login",
    "formats": ["html"],
    "waitFor": 5000
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {FIRECRAWL_KEY}"
}
r = requests.post(f"{FIRECRAWL_URL}/scrape", json=payload, headers=headers, timeout=60)
result = r.json()

if result.get('success'):
    html = result.get('data', {}).get('html', '')
    # Find input elements
    import re
    inputs = re.findall(r'<input[^>]*>', html)
    print(f"\nFound {len(inputs)} input elements:")
    for inp in inputs:
        print(f"  {inp[:200]}")

    buttons = re.findall(r'<button[^>]*>.*?</button>', html, re.DOTALL)
    print(f"\nFound {len(buttons)} buttons:")
    for btn in buttons:
        print(f"  {btn[:200]}")
else:
    print(f"Error: {result}")
