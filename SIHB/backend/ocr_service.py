import base64
import io
import os
import sys
import time
from typing import Optional, List

import cv2
import numpy as np
import urllib.request
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidocr_onnxruntime import RapidOCR
from PIL import Image

app = FastAPI(
    title="LabelGuard AI - PaddleOCR Service",
    description="High-Accuracy Deep Learning OCR Engine (PP-OCRv4 DBNet + SVTR)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("[*] Initializing PaddleOCR (PP-OCRv4 High-Precision ONNX Engine)...")
t0 = time.time()
# Optimized PP-OCRv4 hyperparameters for packaging labels & legal metrology:
# - det_limit_side_len=1536: Prevents aggressive downscaling, keeping 1mm statutory text legible
# - det_box_thresh=0.45: Captures faint dot-matrix batch/date codes & colored label backgrounds
# - det_unclip_ratio=1.8: Expands boundary boxes so symbols like ₹, g, ml, :, / are not clipped
# - det_thresh=0.3: Highly sensitive text boundary detection
# - text_score=0.4: Preserves low-contrast packaging declarations for human review
ocr_engine = RapidOCR(
    det_limit_side_len=1536,
    det_box_thresh=0.45,
    det_unclip_ratio=1.8,
    det_thresh=0.3,
    text_score=0.4,
)
print(f"[+] PaddleOCR PP-OCRv4 Engine ready in {time.time() - t0:.2f}s")


import ipaddress
import urllib.parse
import socket

MAX_IMAGE_BYTES = 15 * 1024 * 1024  # 15 MB limit

def validate_and_fetch_url(target_url: str) -> bytes:
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ('http', 'https'):
        raise HTTPException(status_code=400, detail="Only http and https protocols are supported")
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid hostname in URL")
    
    # Resolve host to IP addresses and block private/loopback/link-local/multicast/reserved
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot resolve hostname: {str(e)}")
        
    for item in addr_info:
        ip_str = item[4][0]
        ip = ipaddress.ip_address(ip_str)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            raise HTTPException(status_code=403, detail="Access to internal/private network addresses is forbidden")
            
    req = urllib.request.Request(
        target_url,
        headers={'User-Agent': 'LabelGuard-OCR/1.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        content_length = resp.headers.get('Content-Length')
        if content_length and int(content_length) > MAX_IMAGE_BYTES:
            raise HTTPException(status_code=413, detail=f"Image exceeds maximum size of {MAX_IMAGE_BYTES} bytes")
        chunks = []
        bytes_read = 0
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            bytes_read += len(chunk)
            if bytes_read > MAX_IMAGE_BYTES:
                raise HTTPException(status_code=413, detail=f"Image exceeds maximum size of {MAX_IMAGE_BYTES} bytes")
            chunks.append(chunk)
        return b"".join(chunks)


class ImagePayload(BaseModel):
    image: Optional[str] = None  # Base64 string or data URI
    image_path: Optional[str] = None  # Direct file path on disk
    url: Optional[str] = None  # Remote or public HTTP/HTTPS URL


class BoundingBox(BaseModel):
    x0: int
    y0: int
    x1: int
    y1: int


class OcrWord(BaseModel):
    text: str
    confidence: float
    bbox: BoundingBox


class OcrResponse(BaseModel):
    text: str
    confidence: float
    words: List[OcrWord]
    engine: str = "PaddleOCR PP-OCRv4 (Deep Learning)"
    elapsed_ms: float


def decode_image_bytes(data: bytes) -> np.ndarray:
    img_array = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        pil_img = Image.open(io.BytesIO(data)).convert("RGB")
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img


def transform_point(x: float, y: float, deg: int, H: int, W: int):
    if deg == 0:
        return int(x), int(y)
    elif deg == 90:
        return int(y), int(H - 1 - x)
    elif deg == 180:
        return int(W - 1 - x), int(H - 1 - y)
    elif deg == 270:
        return int(W - 1 - y), int(x)
    return int(x), int(y)


def run_smart_multi_orientation_ocr(img: np.ndarray):
    H, W = img.shape[:2]
    rotations = [
        (0, None),
        (270, cv2.ROTATE_90_COUNTERCLOCKWISE),
        (90, cv2.ROTATE_90_CLOCKWISE),
        (180, cv2.ROTATE_180),
    ]

    candidates = []
    for deg, flag in rotations:
        r_img = img if flag is None else cv2.rotate(img, flag)
        res, _ = ocr_engine(r_img)
        if not res:
            continue
        total_len = sum(len(str(x[1]).strip()) for x in res)
        candidates.append((total_len, deg, res))

    if not candidates:
        return []

    # Sort so that orientation with highest total text length/density is primary
    candidates.sort(key=lambda c: c[0], reverse=True)

    seen_clean = set()
    merged_items = []

    for _, deg, res in candidates:
        for box, text, score in res:
            text = str(text).strip()
            if not text:
                continue
            clean = "".join(c for c in text if c.isalnum()).lower()
            if len(clean) < 2:
                continue

            if any(clean in sc for sc in seen_clean):
                continue
            seen_clean.add(clean)

            orig_box = [transform_point(pt[0], pt[1], deg, H, W) for pt in box]
            merged_items.append((orig_box, text, score))

    # Sort merged bounding boxes in standard reading order (top-to-bottom, left-to-right)
    if merged_items:
        avg_h = np.mean([max(10, max(pt[1] for pt in item[0]) - min(pt[1] for pt in item[0])) for item in merged_items])
        line_bucket = max(12, int(avg_h * 0.6))
        merged_items.sort(key=lambda item: (min(pt[1] for pt in item[0]) // line_bucket, min(pt[0] for pt in item[0])))

    return merged_items


def process_ocr_result(raw_result, elapsed_ms: float) -> OcrResponse:
    if not raw_result:
        return OcrResponse(text="", confidence=0.0, words=[], elapsed_ms=elapsed_ms)

    lines: List[str] = []
    words: List[OcrWord] = []
    conf_scores: List[float] = []

    for item in raw_result:
        box, text, score = item
        text = str(text).strip()
        if not text:
            continue

        conf_100 = round(float(score) * 100, 1)
        conf_scores.append(conf_100)
        lines.append(text)

        xs = [int(pt[0]) for pt in box]
        ys = [int(pt[1]) for pt in box]
        x0, x1 = min(xs), max(xs)
        y0, y1 = min(ys), max(ys)

        token_list = text.split()
        if not token_list:
            continue
        token_width = max(1, (x1 - x0) // len(token_list))
        for idx, tok in enumerate(token_list):
            wx0 = x0 + idx * token_width
            wx1 = min(x1, wx0 + token_width)
            words.append(
                OcrWord(
                    text=tok,
                    confidence=conf_100,
                    bbox=BoundingBox(x0=wx0, y0=y0, x1=wx1, y1=y1)
                )
            )

    full_text = "\n".join(lines)
    avg_conf = round(sum(conf_scores) / len(conf_scores), 1) if conf_scores else 0.0

    return OcrResponse(
        text=full_text,
        confidence=avg_conf,
        words=words,
        elapsed_ms=round(elapsed_ms, 1)
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ready": True,
        "engine": "PaddleOCR PP-OCRv4 (DBNet + SVTR)",
        "backend": "ONNX Runtime",
        "device": "CPU"
    }


@app.post("/api/ocr", response_model=OcrResponse)
async def recognize_upload(file: UploadFile = File(...)):
    t0 = time.time()
    try:
        content = await file.read(MAX_IMAGE_BYTES + 1)
        if len(content) > MAX_IMAGE_BYTES:
            raise HTTPException(status_code=413, detail=f"File exceeds maximum size of {MAX_IMAGE_BYTES} bytes")
        img = decode_image_bytes(content)
        result = run_smart_multi_orientation_ocr(img)
        elapsed = (time.time() - t0) * 1000
        return process_ocr_result(result, elapsed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/api/ocr/base64", response_model=OcrResponse)
def recognize_base64(payload: ImagePayload):
    t0 = time.time()
    try:
        # 1. Direct local file path (restricted to safe workspace boundaries)
        if payload.image_path:
            real_path = os.path.realpath(payload.image_path)
            allowed_root = os.path.realpath(os.getcwd())
            if not real_path.startswith(allowed_root) and not real_path.startswith('/tmp'):
                raise HTTPException(status_code=403, detail="Access to file path outside allowed workspace is forbidden")
            if not os.path.exists(real_path):
                raise HTTPException(status_code=404, detail=f"File not found: {payload.image_path}")
            img = cv2.imread(real_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Could not read image file: {payload.image_path}")
            result = run_smart_multi_orientation_ocr(img)
            elapsed = (time.time() - t0) * 1000
            return process_ocr_result(result, elapsed)

        # 2. Remote HTTP/HTTPS URL or direct image string starting with http (with SSRF protection)
        target_url = payload.url or (payload.image if payload.image and payload.image.startswith(('http://', 'https://')) else None)
        if target_url:
            data = validate_and_fetch_url(target_url)
            img = decode_image_bytes(data)
            result = run_smart_multi_orientation_ocr(img)
            elapsed = (time.time() - t0) * 1000
            return process_ocr_result(result, elapsed)

        # 3. Base64 encoded string or Data URI
        if payload.image:
            raw_b64 = payload.image
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(raw_b64)
            img = decode_image_bytes(img_bytes)
            result = run_smart_multi_orientation_ocr(img)
            elapsed = (time.time() - t0) * 1000
            return process_ocr_result(result, elapsed)

        raise HTTPException(status_code=400, detail="Either 'image', 'url', or 'image_path' required.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/ocr", response_model=OcrResponse)
async def recognize_upload_alias(file: UploadFile = File(...)):
    return await recognize_upload(file)


if __name__ == "__main__":
    import uvicorn
    import socket

    def is_port_in_use(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', p)) == 0

    target_port = 8000
    if is_port_in_use(8000):
        print("[!] Port 8000 is already occupied by another process.")
        print("[*] Binding to alternate port 8001 (supported by LabelGuard frontend)...")
        target_port = 8001

    print(f"[+] Starting LabelGuard PaddleOCR Service on http://127.0.0.1:{target_port} ...")
    uvicorn.run(app, host="127.0.0.1", port=target_port, log_level="info")
