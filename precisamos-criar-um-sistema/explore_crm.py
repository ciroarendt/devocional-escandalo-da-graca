import requests, json, re

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# Use Firecrawl to scrape the CRM login page for API endpoints
result = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "url": "https://crmapollo.com.br/ademicon-noroeste/",
        "formats": ["html", "links"],
        "waitFor": 3000
    },
    timeout=120
)

resp = result.json()
if 'data' in resp:
    html = resp['data'].get('html', '')
    links = resp['data'].get('links', [])
    print(f"HTML length: {len(html)}")
    print(f"Links: {len(links)}")
    for link in links:
        print(f"  {link}")

    # Look for API URLs in the HTML
    api_urls = re.findall(r'(https?://[^\s"\'<>]+(?:api|ajax|php)[^\s"\'<>]*)', html)
    print(f"\nAPI URLs found: {len(api_urls)}")
    for url in set(api_urls):
        print(f"  {url}")

    # Look for JS script sources
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
    print(f"\nScript sources: {len(scripts)}")
    for s in scripts:
        print(f"  {s}")

    # Look for form actions
    forms = re.findall(r'<form[^>]+action=["\']([^"\']+)["\']', html)
    print(f"\nForm actions: {len(forms)}")
    for f in forms:
        print(f"  {f}")
else:
    print(json.dumps(resp, indent=2)[:1000])
