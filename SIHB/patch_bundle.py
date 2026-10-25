import re

with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Navigation menu items: remove ecommerce-audit, audit, docs
old_nav = '{page:"ecommerce-audit",label:"E-Commerce Surveillance",icon:z1,badge:"Rule 6(10)"},'
if old_nav in text:
    text = text.replace(old_nav, '')
    print('[-] Removed ecommerce-audit nav item')

# Find where audit and docs are in navigation
pos = text.find('label:"System Audit Log"')
if pos != -1:
    print('Found audit at:', pos)
    print(repr(text[pos-40:pos+150]))

# 2. Badges: remove PRO and Surveillance Engine
old_pro = 'c.jsx("span",{className:"text-[10px] font-bold px-1.5 py-0.5 rounded bg-primary-500/20 text-primary-300 border border-primary-500/30",children:"PRO"})'
if old_pro in text:
    text = text.replace(old_pro, 'null')
    print('[-] Removed PRO badge')

old_engine_banner = 'c.jsxs("div",{className:"px-4 py-2.5 mx-3 mt-3 rounded-lg bg-ink-800/60 border border-ink-700/50 flex items-center justify-between",children:[c.jsxs("div",{className:"flex items-center gap-2",children:[c.jsxs("span",{className:"relative flex h-2 w-2",children:[c.jsx("span",{className:"animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"}),c.jsx("span",{className:"relative inline-flex rounded-full h-2 w-2 bg-emerald-500"})]}),c.jsx("span",{className:"text-xs font-medium text-ink-300",children:"Surveillance Engine"})]}),c.jsx("span",{className:"text-[10px] font-mono text-primary-400 bg-primary-950/60 px-1.5 py-0.5 rounded border border-primary-800/60",children:"v2.4 Active"})]})'
if old_engine_banner in text:
    text = text.replace(old_engine_banner, 'null')
    print('[-] Removed Surveillance Engine & v2.4 Active badge')

# 3. PaddleOCR offline red badge: do not show decorative offline badge
old_offline_badge = 'c.jsxs("span",{className:"inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 shadow-sm",title:"Start service via: uvicorn backend.ocr_service:app --port 8000",children:[c.jsx("span",{className:"w-2 h-2 rounded-full bg-rose-500"}),"PaddleOCR Service Offline (Port 8000 Required)"]})'
if old_offline_badge in text:
    text = text.replace(old_offline_badge, 'null')
    print('[-] Removed offline warning banner')

# 4. Summary numbers & Pass/Fail/Skipped
old_viol_header = 'P.length>0?`${P.length} Statutory Violations Detected`:"100% Fully Compliant"'
new_viol_header = 'P.length>0?`${P.length} Declarations Need Review`:"All Declarations Verified"'
if old_viol_header in text:
    text = text.replace(old_viol_header, new_viol_header)
    print('[+] Replaced Violations header')

old_badge_nc = 'P.length>0?"NON-COMPLIANT":"PASSED"'
new_badge_nc = 'P.length>0?"NEEDS REVIEW":"PASSED"'
if old_badge_nc in text:
    text = text.replace(old_badge_nc, new_badge_nc)
    print('[+] Replaced NON-COMPLIANT badge')

old_badge_cls = 'P.length>0?"bg-rose-100 text-rose-800":"bg-emerald-100 text-emerald-800"'
new_badge_cls = 'P.length>0?"bg-amber-100 text-amber-900 border border-amber-300":"bg-emerald-100 text-emerald-800"'
if old_badge_cls in text:
    text = text.replace(old_badge_cls, new_badge_cls)
    print('[+] Replaced badge styling to amber/review')

# Summary counts: passed, failed out of checks -> passed, failed, skipped out of rules
old_summary_text = 'K.filter(we=>we.status==="pass").length," passed,"," ",K.filter(we=>we.status==="fail").length," failed out of ",K.length," checks"'
new_summary_text = 'K.filter(we=>we.status==="pass").length," Passed • ",K.filter(we=>we.status==="fail").length," Failed • ",K.length-K.filter(we=>we.status==="pass").length-K.filter(we=>we.status==="fail").length," Skipped (out of ",K.length," Rules)"'
if old_summary_text in text:
    text = text.replace(old_summary_text, new_summary_text)
    print('[+] Updated summary numbers to Pass / Fail / Skipped out of Rules')

# 5. Replace headline confidence with Field Confidence
old_conf_headline = '"Detection Confidence"'
new_conf_headline = '"Field Confidence"'
if old_conf_headline in text:
    text = text.replace(old_conf_headline, new_conf_headline, 1)
    print('[+] Replaced headline detection confidence title')

# 6. Violations list title and enforcement action
old_viol_title = '"Statutory Violations & Regulatory Recommendations ("'
new_viol_title = '"Declarations Requiring Officer Review ("'
if old_viol_title in text:
    text = text.replace(old_viol_title, new_viol_title)
    print('[+] Updated findings title')

# Remove Enforcement Action recommendation box
enforce_pattern = r'c\.jsxs\("div",\{className:"mt-2\.5 pt-2 border-t border-rose-200/60[^"]*",children:\[c\.jsx\("strong",\{className:"text-rose-900",children:"Enforcement Action:"\}\),[^\]]*\]\}\)'
text = re.sub(enforce_pattern, 'null', text)
print('[-] Removed Enforcement Action box')

# Replace not found in extracted text
text = text.replace(': not found in the extracted label text.', ': Not detected, needs review.')
text = text.replace('not found in the extracted label text', 'Not detected, needs review')

# Hide regulation references: hide LMPCR and FSSR from display
text = re.sub(r'we\.rule\?\.regulation_reference\?\(c\.jsx\([^)]+\)\):null', 'null', text)
text = re.sub(r'v\.rule\?\.regulation_reference\?\(c\.jsx\([^)]+\)\):null', 'null', text)

with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('[+] Successfully patched dist bundle!')
