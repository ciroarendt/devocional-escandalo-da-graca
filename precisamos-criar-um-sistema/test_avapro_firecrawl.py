import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Use Firecrawl to access AVA PRO login page and try to login
# First, let's just scrape the login page
result = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "url": "https://avapro.ademicon.com.br/login",
        "formats": ["html"],
        "waitFor": 5000
    },
    timeout=120
)

resp = result.json()
if 'data' in resp:
    html = resp['data'].get('html', '')
    print(f"HTML length: {len(html)}")
    # Look for form fields
    import re
    inputs = re.findall(r'<input[^>]+>', html)
    print(f"\nInputs ({len(inputs)}):")
    for inp in inputs:
        print(f"  {inp[:200]}")

    # Look for login-related text
    forms = re.findall(r'<form[^>]*>(.*?)</form>', html, re.DOTALL)
    print(f"\nForms: {len(forms)}")

    print(f"\nHTML preview:")
    print(html[:2000])
else:
    print(json.dumps(resp, indent=2)[:500])
