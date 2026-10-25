# LabelGuard — AI-Powered Legal Metrology Compliance Inspection Platform

[![Tests](https://img.shields.io/badge/tests-9%20passed-brightgreen.svg)](#verification--testing)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#prerequisites)
[![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](#prerequisites)
[![License](https://img.shields.io/badge/compliance-LMPCR%202011-orange.svg)](#statutory-rules-implemented)

**LabelGuard** is an automated compliance verification system designed for Legal Metrology officers and packaging inspectors. It validates packaged commodity labels against the statutory requirements of the **Legal Metrology (Packaged Commodities) Rules, 2011 (LMPCR)** using deep learning OCR and an automated regulatory rule engine.

---

## 🌟 Key Features

1. **Side-by-Side Visual Inspection**:
   - High-resolution packaging view on the left with interactive, colored bounding boxes for every detected text field.
   - Comprehensive compliance findings panel on the right with rule codes and severity tags.

2. **Full Statutory Compliance Engine**:
   - **Rule 6(1)(a)**: Name and address of the manufacturer, packer, or importer.
   - **Rule 6(1)(b)**: Generic or common name of the commodity.
   - **Rule 6(1)(c)**: Net quantity declaration with standard SI units and volume/mass rules.
   - **Rule 6(1)(d)**: Month and year of manufacture, packing, or import.
   - **Rule 6(1)(da)**: Maximum Retail Price (MRP) inclusive of all taxes.
   - **Rule 6(11)**: Unit Sale Price (USP) declaration (e.g. `₹ / g`, `₹ / ml`, `₹ / piece`, `per strip`), with single-unit package exemptions under Rule 26.
   - **Rule 6(1)(n)**: Consumer care details (name, address, telephone number, and email ID).
   - **Rule 9**: Bilingual declarations in English and Hindi (Devanagari numerals and units supported).
   - **Rule 13 (Table 1)**: Minimum font and numeral height calculation calibrated to Principal Display Panel (PDP) area.

3. **Severity-Sorted Findings**:
   - Instant categorization into **Critical**, **Major**, and **Minor** non-compliances.
   - Summary badge at the top (e.g., `3 Critical · 8 Major · 4 Minor`).
   - Distinct amber styling for unreadable or unconfirmed fields requiring manual officer review.

4. **Deep Learning OCR with PaddleOCR**:
   - Multi-angle, high-confidence text recognition.
   - Precise bounding box coordinate mapping and font height estimation in pixels and millimeters.

5. **Tamper-Evident Evidence Logging**:
   - Cryptographic SHA-256 hash chaining on all inspection evidence and officer overrides.
   - Exportable, standardized PDF violation dossiers.

---

## 🏗️ Architecture

```
nikhilkumar6969/NITPROJECT
├── SIHB/                          # Core Application Module
│   ├── src/                       # React 18 + TypeScript + Tailwind CSS Frontend
│   │   ├── pages/                 # NewInspection, Dashboard, InspectionDetail, Rules
│   │   ├── components/            # UI components, layout, and visualizer
│   │   └── lib/                   # Compliance engine, mock-data, toast, PDF export
│   ├── backend/                   # FastAPI OCR microservice (PaddleOCR ONNX / PyTorch)
│   ├── dist/                      # Production-ready web assets
│   ├── Dockerfile                 # Multi-stage production container
│   ├── docker-compose.yml         # Container orchestration
│   ├── requirements.txt           # Python backend dependencies
│   ├── run_frontend.py            # Unified single-binary web proxy & static server
│   └── package.json               # Node.js dependencies and build scripts
├── AUDIT.md                       # Comprehensive security and QA audit report
├── run_tests.py                   # Automated compliance and security unit test suite
├── docker-compose.yml             # Root container configuration
├── vercel.json                    # Vercel serverless deployment specification
└── README.md                      # Documentation
```

---

## 🚀 Quick Start

### Option 1: Run with Python (Single Process Server)
Serve both the compiled frontend and the reverse-proxy in one command:
```bash
cd SIHB
python run_frontend.py
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### Option 2: Run with Docker Compose
```bash
docker-compose up --build
```
The application will be accessible at [http://localhost:5173](http://localhost:5173) with backend OCR on [http://localhost:8000](http://localhost:8000).

### Option 3: Development Mode (Vite + FastAPI)
1. **Start Backend OCR Server**:
   ```bash
   cd SIHB
   python -m venv paddle-env
   source paddle-env/bin/activate  # On Windows: .\paddle-env\Scripts\activate
   pip install -r requirements.txt
   python backend/ocr_service.py
   ```
2. **Start Frontend Dev Server**:
   ```bash
   cd SIHB
   npm install
   npm run dev
   ```

---

## 🧪 Verification & Testing

Execute the comprehensive test suite to verify regex rules, bilingual normalization, security controls, and adapter transformations:

```bash
python run_tests.py
```

Expected output:
```
.........
----------------------------------------------------------------------
Ran 9 tests in 0.020s

OK
```

---

## ☁️ Cloud Deployment

### Vercel
1. Import repository `nikhilkumar6969/NITPROJECT` on [Vercel](https://vercel.com).
2. Set Root Directory to `SIHB` (or leave default root with the included `vercel.json`).
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Click **Deploy**.

### Render / Railway / Cloud Run
Deploy using the provided `SIHB/Dockerfile` as a Web Service. Ensure port `5173` is exposed.

---

## 📜 Statutory Rules Implemented
- Legal Metrology Act, 2009
- Legal Metrology (Packaged Commodities) Rules, 2011 (as amended up to 2024)
- FSSAI Packaging & Labelling Regulations (Cross-referenced for food commodities)

---

## 👥 Contributors & NIT Project Team
Developed for National Institute of Technology (NIT) Legal Metrology Hackathon & Deployment.
