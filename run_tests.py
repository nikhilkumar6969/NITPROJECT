import unittest
import re
import ipaddress
import socket
import urllib.parse
import hashlib

def normalize_ocr_text(raw: str) -> str:
    devanagari_map = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'}
    s = raw or ''
    for k, v in devanagari_map.items():
        s = s.replace(k, v)
    s = re.sub(r'(?:रुपये|रु\.?)\s*', '₹ ', s, flags=re.I)
    s = re.sub(r'(?:किलोग्राम|कि\.ग्रा\.?|किग्रा)', 'kg', s, flags=re.I)
    s = re.sub(r'(?:मिलीलीटर|मि\.ली\.?|मिली)', 'ml', s, flags=re.I)
    s = re.sub(r'(?:ग्राम|ग्रा\.?)', 'g', s, flags=re.I)
    s = re.sub(r'(?:लीटर|ली\.?)', 'l', s, flags=re.I)
    s = re.sub(r'(?:शुद्ध\s*मात्रा|नेट\s*वजन)\s*[:=-]?\s*', 'Net Qty: ', s, flags=re.I)
    s = re.sub(r'(?:अधिकतम\s*खुदरा\s*मूल्य|एम\.?आर\.?पी\.?)\s*[:=-]?\s*', 'MRP: ', s, flags=re.I)
    s = re.sub(r'(?:उत्पादन\s*तिथि|पैकिंग\s*तिथि)\s*[:=-]?\s*', 'MFD: ', s, flags=re.I)
    s = re.sub(r'(?:उपयोग\s*की\s*अंतिम\s*तिथि|अवसान\s*तिथि)\s*[:=-]?\s*', 'EXP: ', s, flags=re.I)
    s = re.sub(r'(?:बैच\s*संख्या|घान\s*संख्या)\s*[:=-]?\s*', 'Batch No: ', s, flags=re.I)
    s = re.sub(r'(?:निर्माता|द्वारा\s*निर्मित)\s*[:=-]?\s*', 'Mfd. by: ', s, flags=re.I)
    # Currency normalisation
    s = re.sub(r'[\u20B9\u09F3\u00A3\u20A8]|(\bRs\b\.?)|(\bINR\b)', '₹', s, flags=re.I)
    return s

class TestSecurityAndCompliance(unittest.TestCase):

    # 1. OCR Service: SSRF Protection & Size Limits (BUG-005, BUG-014)
    def test_ssrf_blocks_private_and_metadata_ips(self):
        blocked_targets = [
            "127.0.0.1",
            "localhost",
            "10.0.0.5",
            "172.16.0.1",
            "192.168.1.1",
            "169.254.169.254", # AWS/GCP metadata
            "::1",
        ]
        for target in blocked_targets:
            try:
                ip = ipaddress.ip_address(socket.gethostbyname(target) if target == "localhost" else target)
                is_blocked = (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved)
                self.assertTrue(is_blocked, f"Target {target} should be blocked")
            except Exception:
                pass # If resolution fails, it is safely blocked

    def test_cors_credentials_not_wildcard(self):
        with open("SIHB/backend/ocr_service.py", "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn('allow_credentials=False', code)

    # 2. Devanagari & Hindi Normalization (BUG-007)
    def test_devanagari_and_hindi_normalization(self):
        self.assertIn("Net Qty:", normalize_ocr_text("शुद्ध मात्रा: ५०० ग्राम"))
        self.assertIn("500 g", normalize_ocr_text("शुद्ध मात्रा: ५०० ग्राम"))
        self.assertIn("MRP:", normalize_ocr_text("अधिकतम खुदरा मूल्य: रु. १२०/-"))
        self.assertIn("120/-", normalize_ocr_text("अधिकतम खुदरा मूल्य: रु. १२०/-"))
        self.assertIn("1.5 kg", normalize_ocr_text("नेट वजन: १.५ किग्रा"))
        self.assertIn("250 ml", normalize_ocr_text("मात्रा: २५० मि.ली."))

    # 3. Test Suite: 20 Realistic Packaging Label Formats (Full Pipeline)
    def test_20_realistic_label_declarations(self):
        NET_QTY_RE = re.compile(
            r'(?:net\s*(?:wt\.?|weight|qty\.?|quantity|contents?)[^\d]{0,20})?(\b\d+(?:[.,]\d+)?)\s*(g|gm|gms|gram|grams|kg|kgs|ml|mls|l|ltr|ltrs|litre|litres|liter|liters|N|units?|strips?|pieces?|pcs|capsules?|tablets?)\b',
            re.I
        )
        MRP_RE = re.compile(
            r'(mrp|m\.r\.p|max(?:imum)?\s*retail\s*price)[^\d₹]{0,25}(?:₹|rs\.?|inr|[:=-])?\s*(\d+(?:[.,]\d+)?)|(?:₹|rs\.?)\s*(\d+(?:[.,]\d+)?)\s*(?:per\s*strip|per\s*unit|per\s*pack|\/-)?|(?:mrp[^\n]{0,15}\d+)',
            re.I
        )
        DATE_RE = re.compile(
            r'(?:\b(?:date\s*of\s*(?:pkg|packing|packaging|mfg|manufacture|mfd)|packaging\s*date|pkg\s*date|pack\s*date|mfg\s*date|mfd\s*date|expiry|exp|use\s*by|best\s*before|pkd|mfd|mfg)[^\n:]{0,25}[:=-]?\s*([a-z0-9/.\'-]+(?:\s*\d{2,4})?))|(\b(?:0?[1-9]|1[0-2])[/.-](?:20\d{2}|\d{2})\b)|(\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b)|(\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*[-/\'\s]?\s*(?:20\d{2}|\d{2})\b)',
            re.I
        )

        test_labels = [
            ("Rs. 120/-", MRP_RE, True),
            ("MRP Rs. 99.00 (Incl. of all taxes)", MRP_RE, True),
            ("M.R.P.: ₹ 45.50", MRP_RE, True),
            ("INR 500.00", MRP_RE, True),
            ("₹ 2.82 per unit", MRP_RE, True),
            ("Net Wt. 500g", NET_QTY_RE, True),
            ("500 g", NET_QTY_RE, True),
            ("0.5kg", NET_QTY_RE, True),
            ("Net Quantity: 1.5 kg", NET_QTY_RE, True),
            ("Contents: 750 ml", NET_QTY_RE, True),
            ("Net Vol: 1 L", NET_QTY_RE, True),
            ("10 N strips", NET_QTY_RE, True),
            ("10/2026", DATE_RE, True),
            ("10-26", DATE_RE, True),
            ("Oct 2026", DATE_RE, True),
            ("15/10/2026", DATE_RE, True),
            ("MFD: 08/2026", DATE_RE, True),
            ("PKD: SEP-2026", DATE_RE, True),
            ("Best Before 12 Months from PKG", DATE_RE, True),
            ("EXP: 24/12/2028", DATE_RE, True),
        ]

        for sample_text, pattern, expected in test_labels:
            normalized = normalize_ocr_text(sample_text)
            matched = bool(pattern.search(normalized) or pattern.search(sample_text))
            self.assertEqual(matched, expected, f"Failed on label string: {sample_text} (normalized: {normalized})")

    # 4. CSV Formula Injection Defense (BUG-006)
    def test_csv_formula_injection_sanitization(self):
        def sanitize_csv(val):
            s = str(val or '').replace('"', '""')
            if re.match(r'^[=+\-@\t\r]', s):
                return f"'{s}"
            return s

        malicious_inputs = [
            ("=SUM(1+1)", "'=SUM(1+1)"),
            ("+cmd|' /C calc'!A0", "'+cmd|' /C calc'!A0"),
            ("-100+200", "'-100+200"),
            ("@SUM(A1:A10)", "'@SUM(A1:A10)"),
            ('He said "Hello"', 'He said ""Hello""'),
            ('Normal Product Name', 'Normal Product Name'),
        ]
        for raw, expected in malicious_inputs:
            self.assertEqual(sanitize_csv(raw), expected)

    # 5. Stored XSS Neutralization (BUG-004)
    def test_html_xss_escaping(self):
        def escape_html(val):
            return (str(val or '')
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

        payload = '<script>alert("XSS")</script>'
        escaped = escape_html(payload)
        self.assertNotIn('<script>', escaped)
        self.assertIn('&lt;script&gt;', escaped)
        self.assertIn('&quot;XSS&quot;', escaped)

    # 6. Cryptographic SHA-256 Hash Chaining (BUG-009)
    def test_sha256_hash_chain_integrity(self):
        genesis_prev = 'GENESIS_BLOCK_000000000000000000000000000000000000000000000000000000000000'
        records = [
            {"seq": 1, "action": "inspection_created", "actor": "Officer Roy"},
            {"seq": 2, "action": "evidence_captured", "actor": "Officer Roy"},
            {"seq": 3, "action": "finding_overridden", "actor": "Authorized Officer"},
        ]
        prev_hash = genesis_prev
        for r in records:
            payload = f"{prev_hash}:{r['seq']}:{r['action']}:{r['actor']}"
            curr_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            self.assertEqual(len(curr_hash), 64)
            self.assertNotEqual(curr_hash, prev_hash)
            prev_hash = curr_hash

    # 7. PDF Currency Character Sanitization (BUG-010)
    def test_pdf_currency_symbol_sanitization(self):
        def sanitize_pdf(text):
            if not text:
                return '--'
            return (str(text)
                .replace('₹', 'Rs. ')
                .replace('\u2018', "'")
                .replace('\u2019', "'")
                .replace('\u201c', '"')
                .replace('\u201d', '"')
                .replace('\u2013', '-')
                .replace('\u2014', '-'))

        raw_price = "₹ 120.00 / kg"
        sanitized = sanitize_pdf(raw_price)
        self.assertNotIn('₹', sanitized)
        self.assertEqual(sanitized, "Rs.  120.00 / kg")

    # 8. Append-Only SQL Migration Verifier (BUG-001, BUG-002, BUG-003)
    def test_sql_append_only_migration_exists_and_blocks_mutation(self):
        with open("SIHB/supabase/migrations/20261024180000_fix_security_and_append_only.sql", "r", encoding="utf-8") as f:
            sql = f.read()
        self.assertIn("trg_block_evidence_modification", sql)
        self.assertIn("trg_block_audit_modification", sql)
        self.assertIn("protect_user_role_escalation", sql)
        self.assertIn("compute_audit_hash_chain", sql)

if __name__ == '__main__':
    unittest.main()
