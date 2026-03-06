import requests, json

api_key = "fc-0fbdfa006bf0466eaa1338f8c4e5b9ad"

# First, let's see the login page HTML to find the right selectors
result = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "url": "https://avapro.ademicon.com.br/login",
        "formats": ["html"],
        "waitFor": 5000,
    },
    timeout=120
)

resp = result.json()
if 'data' in resp:
    html = resp['data'].get('html', '')
    print(f"HTML length: {len(html)}")

    import re
    # Find all buttons
    buttons = re.findall(r'<button[^>]*>([^<]*)</button>', html)
    print(f"\nButtons: {buttons}")

    # Find all button elements with their full HTML
    button_tags = re.findall(r'<button[^>]*>[^<]*</button>', html)
    print(f"\nButton HTML:")
    for b in button_tags:
        print(f"  {b}")

    # Find inputs
    inputs = re.findall(r'<input[^>]+>', html)
    print(f"\nInputs:")
    for i in inputs:
        print(f"  {i}")

    # Find all clickable elements
    clickable = re.findall(r'<(?:button|a|div)[^>]*(?:onClick|click|submit|Entrar|Acessar)[^>]*>[^<]*</(?:button|a|div)>', html, re.IGNORECASE)
    print(f"\nClickable elements:")
    for c in clickable:
        print(f"  {c}")

    # Look for "Entrar" or "Acessar" text
    enters = re.findall(r'>[^<]*(?:Entrar|Acessar|Login)[^<]*<', html, re.IGNORECASE)
    print(f"\nEntrar/Acessar text:")
    for e in enters:
        print(f"  {e}")

    # Print relevant section of HTML around the inputs
    input_idx = html.find('Matrícula')
    if input_idx >= 0:
        print(f"\nHTML around Matricula ({input_idx}):")
        print(html[input_idx:input_idx+2000])
