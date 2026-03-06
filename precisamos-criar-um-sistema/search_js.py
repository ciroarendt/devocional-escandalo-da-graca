import re

with open('/tmp/chunk_0984d1313cf12825.js', 'r') as f:
    content = f.read()

# Find ContemplationOption and surrounding code
idx = content.find('ContemplationOption')
if idx >= 0:
    start = max(0, idx - 500)
    end = min(len(content), idx + 2000)
    snippet = content[start:end]
    print("=== ContemplationOption context ===")
    print(snippet)
    print("\n\n")

# Search for "contemplation" or "contemplacao" more broadly
for m in re.finditer(r'contemplat', content, re.IGNORECASE):
    s = max(0, m.start() - 300)
    e = min(len(content), m.end() + 800)
    snippet = content[s:e]
    print(f"=== Found 'contemplat' at {m.start()} ===")
    print(snippet[:1200])
    print("\n---\n")

# Also search for "lance" in a more targeted way - skip "ambulance"
for m in re.finditer(r'(?<![a-zA-Z])lance', content, re.IGNORECASE):
    s = max(0, m.start() - 200)
    e = min(len(content), m.end() + 500)
    snippet = content[s:e]
    if 'ambulance' not in snippet.lower()[:50]:
        print(f"=== Found 'lance' at {m.start()} ===")
        print(snippet[:800])
        print("\n---\n")

# Search for "oferta" (bid/offer in Portuguese)
for m in re.finditer(r'oferta', content, re.IGNORECASE):
    s = max(0, m.start() - 200)
    e = min(len(content), m.end() + 500)
    snippet = content[s:e]
    print(f"=== Found 'oferta' at {m.start()} ===")
    print(snippet[:800])
    print("\n---\n")
