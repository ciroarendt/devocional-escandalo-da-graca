import re

with open('/tmp/avapro_bundle.js', 'r') as f:
    content = f.read()

# Find the static class methods for fetching groups, plans, credits
patterns = [
    'fetchGrupos',
    'fetchPlanoGrupo',
    'fetchPrazos',
    'fetchCredito',
    '/simular/grupos',
    '/simular/produtos',
    'simular',
]

for pat in patterns:
    matches = list(re.finditer(re.escape(pat), content, re.IGNORECASE))
    print(f'\n=== {pat} ({len(matches)} matches) ===')
    for m in matches[:5]:
        s = max(0, m.start() - 100)
        e = min(len(content), m.end() + 500)
        snippet = content[s:e]
        print(snippet[:700])
        print('---')
