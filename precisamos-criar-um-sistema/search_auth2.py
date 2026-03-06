import re

# Search ALL chunks for avapro, firebase, getIdToken, signIn, auth
for fname in [
    '/tmp/chunk_0984d1313cf12825.js',
    '/tmp/chunk_ccc2716aa5f8f2a8.js',
    '/tmp/chunk_7cf2d0eedfa12d8a.js',
    '/tmp/chunk_c638c266bd4a268c.js',
    '/tmp/chunk_70dd047adc18cb66.js',
    '/tmp/chunk_4be7b1173b3fb62d.js',
    '/tmp/chunk_b99ebf8a9037d605.js',
    '/tmp/chunk_95b80df6e733971a.js',
    '/tmp/chunk_59155b984a52a275.js',
    '/tmp/chunk_6d01377ca4556651.js',
    '/tmp/chunk_e5dc1d9df072d066.js',
]:
    try:
        with open(fname, 'r') as f:
            content = f.read()
    except:
        continue

    short = fname.split('/')[-1]

    for pattern in ['avapro', 'firebase', 'getIdToken', 'signIn', 'wallets', '/wallets']:
        count = content.lower().count(pattern.lower())
        if count > 0:
            print(f"[{short}] '{pattern}' found {count} times")
            # Show first occurrence with context
            idx = content.lower().find(pattern.lower())
            s = max(0, idx - 100)
            e = min(len(content), idx + 500)
            print(f"  First: ...{content[s:e][:600]}...")
            print()
