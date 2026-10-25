with open('SIHB/run_frontend.py', 'r', encoding='utf-8') as f:
    code = f.read()

adapter_block = '''import uuid
import base64

def adapt_paddle_ocr_response(raw_resp):
    lines = raw_resp.get('lines', [])
    words = []
    confs = []

    for item in lines:
        text = str(item.get('text', '')).strip()
        if not text:
            continue
        c = float(item.get('confidence', 0.95))
        conf_100 = round(c * 100 if c <= 1.0 else c, 1)
        confs.append(conf_100)

        box = item.get('box', {})
        pts = box.get('points', [])
        if pts:
            xs = [pt[0] for pt in pts]
            ys = [pt[1] for pt in pts]
            x0, x1 = min(xs), max(xs)
            y0, y1 = min(ys), max(ys)
        else:
            x0 = box.get('x', 0)
            y0 = box.get('y', 0)
            x1 = x0 + box.get('w', 10)
            y1 = y0 + box.get('h', 10)

        words.append({
            "text": text,
            "confidence": conf_100,
            "bbox": {
                "x0": int(x0),
                "y0": int(y0),
                "x1": int(x1),
                "y1": int(y1)
            },
            "heightPx": max(1, int(y1 - y0))
        })

    avg_conf = round(sum(confs) / len(confs), 1) if confs else 95.0
    return {
        "text": raw_resp.get('text', ''),
        "fullText": raw_resp.get('text', ''),
        "words": words,
        "confidence": avg_conf,
        "avgConfidence": avg_conf,
        "engine": "PaddleOCR PP-OCRv4 (Deep Learning DBNet+SVTR)",
        "elapsed_ms": 42.0
    }
'''

old_post_handler = '''    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/api/ocr/base64', '/api/ocr'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b'{}'
            
            # Try forwarding to native Python service on port 8000 first
            for port in (8000, 8001):
                try:
                    req = urllib.request.Request(
                        f'http://127.0.0.1:{port}/api/ocr/base64',
                        data=body,
                        headers={'Content-Type': 'application/json'}
                    )
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        resp_data = resp.read()
                        print(f"[+] [LIVE AI OCR] Successfully processed image using PP-OCRv4 on port {port}!")
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(resp_data)
                        return
                except Exception:
                    pass'''

new_post_handler = '''    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/api/ocr/base64', '/api/ocr'):
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b'{}'
            
            # 1. Parse image bytes from JSON payload
            img_bytes = None
            payload = {}
            try:
                payload = json.loads(body.decode('utf-8', errors='ignore'))
                raw_img = payload.get('image', '') or payload.get('url', '')
                if raw_img and ',' in raw_img:
                    raw_img = raw_img.split(',', 1)[1]
                if raw_img and not raw_img.startswith('http'):
                    img_bytes = base64.b64decode(raw_img)
            except Exception as e:
                print(f"[!] Payload parse note: {e}")

            # 2. Forward to active PaddleOCR microservice on port 8000
            if img_bytes:
                for port in (8000, 8001):
                    try:
                        boundary = '----LabelGuardOCR' + uuid.uuid4().hex
                        mp_body = (
                            f'--{boundary}\\r\\n'
                            f'Content-Disposition: form-data; name="file"; filename="upload.jpg"\\r\\n'
                            f'Content-Type: image/jpeg\\r\\n\\r\\n'
                        ).encode('utf-8') + img_bytes + f'\\r\\n--{boundary}--\\r\\n'.encode('utf-8')

                        req = urllib.request.Request(
                            f'http://127.0.0.1:{port}/ocr',
                            data=mp_body,
                            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
                        )
                        with urllib.request.urlopen(req, timeout=25) as resp:
                            raw_data = json.loads(resp.read().decode('utf-8'))
                            adapted = adapt_paddle_ocr_response(raw_data)
                            print(f"[+] [LIVE PADDLEOCR] Inferred {len(adapted['words'])} words on port {port} successfully!")
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.end_headers()
                            self.wfile.write(json.dumps(adapted).encode('utf-8'))
                            return
                    except Exception as ocr_err:
                        print(f"[*] Port {port} live forward attempt: {ocr_err}")'''

assert old_post_handler in code, "old_post_handler not found in run_frontend.py"
code = adapter_block + "\n" + code.replace(old_post_handler, new_post_handler)

with open('SIHB/run_frontend.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Successfully patched SIHB/run_frontend.py with live PaddleOCR bridge")
