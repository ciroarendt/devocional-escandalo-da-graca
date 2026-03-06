import re

with open('/tmp/chunk_0984d1313cf12825.js', 'r') as f:
    content = f.read()

# Find the /offers endpoint usage and parameters
idx = content.find('/offers?')
if idx >= 0:
    s = max(0, idx - 1500)
    e = min(len(content), idx + 3000)
    snippet = content[s:e]
    print("=== /offers endpoint context ===")
    print(snippet)

# Also try /simulations endpoint
print("\n\n=== /simulations endpoint ===")
for m in re.finditer(r'simulations', content):
    s = max(0, m.start() - 300)
    e = min(len(content), m.end() + 500)
    snippet = content[s:e]
    if 'SIMULATOR_API' in snippet or 'request' in snippet:
        print(snippet[:800])
        print("\n---\n")
