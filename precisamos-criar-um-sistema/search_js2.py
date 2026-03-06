import re

# Search all chunks for API endpoints related to bids/lances
for fname in [
    '/tmp/chunk_0984d1313cf12825.js',
    '/tmp/chunk_4be7b1173b3fb62d.js',
    '/tmp/chunk_59155b984a52a275.js',
    '/tmp/chunk_6d01377ca4556651.js',
    '/tmp/chunk_70dd047adc18cb66.js',
    '/tmp/chunk_7cf2d0eedfa12d8a.js',
    '/tmp/chunk_95b80df6e733971a.js',
    '/tmp/chunk_b99ebf8a9037d605.js',
    '/tmp/chunk_c638c266bd4a268c.js',
    '/tmp/chunk_ccc2716aa5f8f2a8.js',
    '/tmp/chunk_e5dc1d9df072d066.js',
]:
    try:
        with open(fname, 'r') as f:
            content = f.read()
    except:
        continue

    short = fname.split('/')[-1]

    # Search for API endpoint patterns with lance/bid/contemplation
    patterns = [
        r'/assemblies/[a-zA-Z]+',
        r'/simulations/[a-zA-Z]+',
        r'/groups/[a-zA-Z]+',
        r'assemblies.*(?:bid|lance|result|contempl)',
        r'(?:bid|lance|result|contempl).*assembl',
        r'/api/[a-zA-Z/_-]+(?:lance|bid|contempl)',
    ]

    for pat in patterns:
        for m in re.finditer(pat, content, re.IGNORECASE):
            s = max(0, m.start() - 50)
            e = min(len(content), m.end() + 100)
            print(f"[{short}] {pat}: ...{content[s:e]}...")
            print()

# Also search for specific endpoint paths
print("\n=== ENDPOINT SEARCH ===")
for fname in [
    '/tmp/chunk_0984d1313cf12825.js',
    '/tmp/chunk_ccc2716aa5f8f2a8.js',
    '/tmp/chunk_7cf2d0eedfa12d8a.js',
    '/tmp/chunk_c638c266bd4a268c.js',
]:
    try:
        with open(fname, 'r') as f:
            content = f.read()
    except:
        continue

    short = fname.split('/')[-1]

    # Find all URL-like paths
    for m in re.finditer(r'["\']/(assemblies|simulations|groups|bids|contemplations?|offers)/[^"\']*["\']', content):
        print(f"[{short}] Endpoint: {m.group()}")

    # Find fetch/axios calls with relevant endpoints
    for m in re.finditer(r'(?:fetch|get|post|put|delete)\(["\']([^"\']*(?:assembl|simulat|group|bid|lance|contempl|offer)[^"\']*)["\']', content, re.IGNORECASE):
        print(f"[{short}] API call: {m.group()}")
