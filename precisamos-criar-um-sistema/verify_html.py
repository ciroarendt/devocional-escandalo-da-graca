with open('/home/dev/workspace/precisamos-criar-um-sistema/index.html') as f:
    content = f.read()

markers = ['<style>', '</style>', '<script>', '</script>', '<header', '<footer', 'const DADOS', 'ADEMICON']
for m in markers:
    count = content.count(m)
    print(f'{m}: {count} occurrences')

print(f'Total length: {len(content)} chars')
print(f'Has SVG logo: {"<svg" in content}')
print(f'Has CSS vars: {"--red" in content}')
print(f'Has app.js code: {"renderDashboard" in content}')
print(f'Has dados: {"groups" in content}')
