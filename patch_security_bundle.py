with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'r', encoding='utf-8') as f:
    bundle = f.read()

# 1. Patch CSV formula injection (BUG-006)
old_csv_map = 'T.map(X=>`"${X}"`).join(",")'
new_csv_map = 'T.map(X=>{const s=String(X??"").replace(/"/g,\'""\');return /^[=+\\-@\\t\\r]/.test(s)?`"\'`+s+`"`:`"${s}"`}).join(",")'

if old_csv_map in bundle:
    bundle = bundle.replace(old_csv_map, new_csv_map, 1)
    print('[+] Patched CSV formula injection in bundle!')
else:
    print('[-] old_csv_map not found in bundle')

# 2. Patch Stored XSS in report generation (BUG-004)
old_table_row = '<tr><td>${((U=k.product)==null?void 0:U.name)??"Unknown"}</td><td>${((T=k.product)==null?void 0:T.brand)??""}</td>'
new_table_row = '<tr><td>${String(((U=k.product)==null?void 0:U.name)??"Unknown").replace(/[&<>"\\\']/g,m=>({ "&":"&amp;", "<":"&lt;", ">":"&gt;", \'"\':"&quot;", "\'":"&#39;" })[m])}</td><td>${String(((T=k.product)==null?void 0:T.brand)??"").replace(/[&<>"\\\']/g,m=>({ "&":"&amp;", "<":"&lt;", ">":"&gt;", \'"\':"&quot;", "\'":"&#39;" })[m])}</td>'

if old_table_row in bundle:
    bundle = bundle.replace(old_table_row, new_table_row, 1)
    print('[+] Patched Stored XSS in report generation in bundle!')
else:
    print('[-] old_table_row not found in bundle')

with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'w', encoding='utf-8') as f:
    f.write(bundle)
