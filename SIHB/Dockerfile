# Stage 1: Build Frontend Assets
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Unified Production Runtime (FastAPI + PaddleOCR + Static Serving)
FROM python:3.11-slim
WORKDIR /app

# Install system runtime dependencies for OpenCV and ONNX
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and built frontend assets
COPY --from=frontend-builder /app/dist ./dist
COPY backend ./backend
COPY run_frontend.py ./

EXPOSE 5173
EXPOSE 8000

ENV PORT=5173
ENV HOST=0.0.0.0

# Start both OCR microservice and Unified Frontend Server
CMD ["sh", "-c", "python backend/ocr_service.py & python run_frontend.py"]
