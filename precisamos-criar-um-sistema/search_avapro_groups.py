import re

with open('/tmp/avapro_bundle.js', 'r') as f:
    content = f.read()

# Search for group-related endpoints
patterns = [
    r'grupo|groups|group',
    r'/products/\$\{[^}]+\}/simulations',
    r'simulations',
    r'fetchTipoNeg',
    r'tipopagamento',
    r'planosGrupo',
    r'tipoVenda',
    r'credito',
    r'parcela',
]

for pat in patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches and len(matches) < 20:
        print(f"\n=== Pattern: '{pat}' ({len(matches)} matches) ===")
        for m in matches[:5]:
            s = max(0, m.start() - 150)
            e = min(len(content), m.end() + 400)
            snippet = content[s:e]
            print(f"  At {m.start()}: ...{snippet[:600]}...")
            print()
    elif matches:
        print(f"\n=== Pattern: '{pat}' ({len(matches)} matches - showing first 3) ===")
        for m in matches[:3]:
            s = max(0, m.start() - 100)
            e = min(len(content), m.end() + 300)
            snippet = content[s:e]
            print(f"  At {m.start()}: ...{snippet[:500]}...")
            print()
