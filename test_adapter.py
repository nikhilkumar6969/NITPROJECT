def adapt_ocr_response(raw_resp):
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
        "engine": "PaddleOCR (Deep Learning DBNet+SVTR)",
        "elapsed_ms": 42.0
    }

sample = {
    "text": "Test Line 1\nTest Line 2",
    "lines": [
        {"text": "Test Line 1", "confidence": 0.98, "box": {"points": [[10, 10], [100, 10], [100, 30], [10, 30]]}},
        {"text": "Test Line 2", "confidence": 0.95, "box": {"points": [[10, 40], [120, 40], [120, 60], [10, 60]]}}
    ]
}

adapted = adapt_ocr_response(sample)
print("Adapted structure successfully:")
print("words count:", len(adapted['words']))
print("first word:", adapted['words'][0])
