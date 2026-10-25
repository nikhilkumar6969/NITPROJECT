import re

with open('SIHB/src/lib/compliance-engine.ts', 'r', encoding='utf-8') as f:
    text = f.read()

new_block = """  // Normalize Hindi statutory keywords and metric units (compounds ordered first)
  s = s.replace(/(?:रुपये|रु\\.?)\\s*/gi, '₹ ');
  s = s.replace(/(?:किलोग्राम|कि\\.ग्रा\\.?|किग्रा)/gi, 'kg');
  s = s.replace(/(?:मिलीलीटर|मि\\.ली\\.?|मिली)/gi, 'ml');
  s = s.replace(/(?:ग्राम|ग्रा\\.?)/gi, 'g');
  s = s.replace(/(?:लीटर|ली\\.?)/gi, 'l');
  s = s.replace(/(?:शुद्ध\\s*मात्रा|नेट\\s*वजन)\\s*[:=-]?\\s*/gi, 'Net Qty: ');
  s = s.replace(/(?:अधिकतम\\s*खुदरा\\s*मूल्य|एम\\.?आर\\.?पी\\.?)\\s*[:=-]?\\s*/gi, 'MRP: ');
  s = s.replace(/(?:उत्पादन\\s*तिथि|पैकिंग\\s*तिथि)\\s*[:=-]?\\s*/gi, 'MFD: ');
  s = s.replace(/(?:उपयोग\\s*की\\s*अंतिम\\s*तिथि|अवसान\\s*तिथि)\\s*[:=-]?\\s*/gi, 'EXP: ');
  s = s.replace(/(?:बैच\\s*संख्या|घान\\s*संख्या)\\s*[:=-]?\\s*/gi, 'Batch No: ');
  s = s.replace(/(?:निर्माता|द्वारा\\s*निर्मित)\\s*[:=-]?\\s*/gi, 'Mfd. by: ');"""

text = re.sub(
    r"  // Normalize Hindi statutory keywords and metric units.*?(?=  // Normalize common OCR rupee)",
    lambda m: new_block + "\n\n",
    text,
    flags=re.DOTALL
)

with open('SIHB/src/lib/compliance-engine.ts', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated compliance-engine.ts with ordered metric compounds")
