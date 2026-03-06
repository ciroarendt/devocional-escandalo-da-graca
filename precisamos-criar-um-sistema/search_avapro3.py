import re

with open('/tmp/avapro_bundle.js', 'r') as f:
    content = f.read()

# Find the Un class and its base URL/tenant
patterns = [
    'class Un',
    'class Jf',
    'super.tenant',
    'ademitech',
    '60d0db2552fcc900beb502d5',
    'api-clientv2',
    'baseURL',
]

for pat in patterns:
    matches = list(re.finditer(re.escape(pat), content))
    print(f'\n=== {pat} ({len(matches)} matches) ===')
    for m in matches[:3]:
        s = max(0, m.start() - 200)
        e = min(len(content), m.end() + 300)
        snippet = content[s:e]
        print(snippet[:600])
        print('---')
