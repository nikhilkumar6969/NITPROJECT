with open('SIHB/src/lib/compliance-engine.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace \b before/after Devanagari words
text = text.replace(r"\b(?:रुपये|रु\.?)\s*", r"(?:रुपये|रु\.?)\s*")
text = text.replace(r"\b(?:ग्राम|ग्रा\.?)\b", r"(?:ग्राम|ग्रा\.?)")
text = text.replace(r"\b(?:किलोग्राम|कि\.ग्रा\.?|किग्रा)\b", r"(?:किलोग्राम|कि\.ग्रा\.?|किग्रा)")
text = text.replace(r"\b(?:मिलीलीटर|मि\.ली\.?|मिली)\b", r"(?:मिलीलीटर|मि\.ली\.?|मिली)")
text = text.replace(r"\b(?:लीटर|ली\.?)\b", r"(?:लीटर|ली\.?)")
text = text.replace(r"\b(?:शुद्ध\s*मात्रा|नेट\s*वजन)\b", r"(?:शुद्ध\s*मात्रा|नेट\s*वजन)")
text = text.replace(r"\b(?:अधिकतम\s*खुदरा\s*मूल्य|एम\.?आर\.?पी\.?)\b", r"(?:अधिकतम\s*खुदरा\s*मूल्य|एम\.?आर\.?पी\.?)")
text = text.replace(r"\b(?:उत्पादन\s*तिथि|पैकिंग\s*तिथि)\b", r"(?:उत्पादन\s*तिथि|पैकिंग\s*तिथि)")
text = text.replace(r"\b(?:उपयोग\s*की\s*अंतिम\s*तिथि|अवसान\s*तिथि)\b", r"(?:उपयोग\s*की\s*अंतिम\s*तिथि|अवसान\s*तिथि)")
text = text.replace(r"\b(?:बैच\s*संख्या|घान\s*संख्या)\b", r"(?:बैच\s*संख्या|घान\s*संख्या)")
text = text.replace(r"\b(?:निर्माता|द्वारा\s*निर्मित)\b", r"(?:निर्माता|द्वारा\s*निर्मित)")

with open('SIHB/src/lib/compliance-engine.ts', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed Devanagari regex boundaries in compliance-engine.ts")
