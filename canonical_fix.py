import glob, re, os

base = r'C:\Users\我的电脑\AccioWork\2026-06-16-17-59-48\shanlinyang-site'
domain = 'https://www.shanlinyang.com'
issues = []

html_files = glob.glob(os.path.join(base, '**', '*.html'), recursive=True)

for f in html_files:
    if 'node_modules' in f: continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading {f}: {e}")
        continue
    
    rel_path = os.path.relpath(f, base).replace('\\', '/')
    
    # Handle home page and directory indexes
    if rel_path == 'index.html':
        expected_canonical = domain + '/'
    elif rel_path.endswith('/index.html'):
        expected_canonical = domain + '/' + rel_path[:-10]
    else:
        expected_canonical = domain + '/' + rel_path

    canonical_pattern = re.compile(r'<link[^>]*rel=[\"\']canonical[\"\'][^>]*href=[\"\']([^\"\']+)[\"\']', re.IGNORECASE)
    canonical_match = canonical_pattern.search(content)
    
    if not canonical_match:
        # Try to insert after <head>
        head_match = re.search(r'<head>', content, re.IGNORECASE)
        if head_match:
            # Check if there is already a newline after <head>
            insertion_point = head_match.end()
            new_tag = f'\n<link rel="canonical" href="{expected_canonical}">'
            content = content[:insertion_point] + new_tag + content[insertion_point:]
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            issues.append(f'FIXED (Added): {rel_path}')
        else:
            issues.append(f'FAILED (No <head>): {rel_path}')
    else:
        current_canonical = canonical_match.group(1)
        if current_canonical != expected_canonical:
            # Replace the href value carefully
            old_tag = canonical_match.group(0)
            new_tag = re.sub(r'href=[\"\'][^\"\']+[\"\']', f'href="{expected_canonical}"', old_tag)
            content = content.replace(old_tag, new_tag)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            issues.append(f'FIXED (Updated): {rel_path} ({current_canonical} -> {expected_canonical})')

print(f'Total actions: {len(issues)}')
for i in issues:
    print(i)
