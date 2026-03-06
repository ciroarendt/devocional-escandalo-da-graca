import re

with open('/tmp/avapro_bundle.js', 'r') as f:
    content = f.read()

# Find detailed context around lance endpoints
endpoints_to_find = [
    '/api/v2/lances/quota/info',
    '/api/v2/lances/quota/search',
    '/api/v2/lances/quota/simulation',
    '/api/v2/lances/simulation',
    '/offers/inprogress',
    '/offers/sells',
    '/offers/by-deal/',
    'conciliatory-link/wallet',
    'wallets/bids/config',
    'wallets/lottery',
    'wallets/analysis',
]

for ep in endpoints_to_find:
    idx = content.find(ep)
    if idx >= 0:
        s = max(0, idx - 500)
        e = min(len(content), idx + 1000)
        snippet = content[s:e]
        print(f"\n=== {ep} (at {idx}) ===")
        print(snippet[:1500])
        print("---")

# Also find all references to "ademitech" API endpoints
print("\n\n=== ADEMITECH API CALLS ===")
for m in re.finditer(r'ademitech\.com\.br([^"\'`\s,]+)', content):
    path = m.group(1)
    s = max(0, m.start() - 200)
    e = min(len(content), m.end() + 300)
    context = content[s:e]
    print(f"\nPath: {path}")
    print(f"  Context: {context[:500]}")
    print()
