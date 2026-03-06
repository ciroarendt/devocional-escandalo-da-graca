import re

with open('/tmp/avapro_bundle.js', 'r') as f:
    content = f.read()

# Find route definitions
patterns = [
    'simulador',
    'simula',
    '/nova-venda',
    '/venda',
    'path:.*simul',
    'NEWCON_SIMULATOR',
]

for pat in patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    print(f'\n=== {pat} ({len(matches)} matches) ===')
    for m in matches[:5]:
        s = max(0, m.start() - 150)
        e = min(len(content), m.end() + 300)
        snippet = content[s:e]
        print(snippet[:500])
        print('---')
