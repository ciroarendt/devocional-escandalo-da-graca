import re

# Search JS chunks for auth/login/token patterns
for fname in [
    '/tmp/chunk_0984d1313cf12825.js',
    '/tmp/chunk_ccc2716aa5f8f2a8.js',
    '/tmp/chunk_7cf2d0eedfa12d8a.js',
    '/tmp/chunk_c638c266bd4a268c.js',
    '/tmp/chunk_70dd047adc18cb66.js',
    '/tmp/chunk_4be7b1173b3fb62d.js',
    '/tmp/chunk_b99ebf8a9037d605.js',
]:
    try:
        with open(fname, 'r') as f:
            content = f.read()
    except:
        continue

    short = fname.split('/')[-1]

    # Search for auth-related patterns
    for pattern in ['avapro', 'firebase', 'getIdToken', 'CRM_API_URL', 'Bearer', 'authorization', 'jwt-avapro']:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            s = max(0, m.start() - 200)
            e = min(len(content), m.end() + 500)
            snippet = content[s:e]
            print(f"[{short}] Found '{pattern}' at {m.start()}")
            print(f"  {snippet[:700]}")
            print()
