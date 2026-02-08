# STAGE 1: Build React frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci  # Need dev dependencies for the build process
COPY frontend/ .
# Copy the .env file to ensure environment variables are available during build
COPY frontend/.env* ./
RUN npm run build

# STAGE 2: Build FastAPI backend + embed frontend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Copy built frontend into ./static directory
COPY --from=frontend-builder /build/build ./static

# HF Spaces REQUIREMENTS
ENV PORT=7860
ENV HOST=0.0.0.0
ENV DEBUG=False
EXPOSE 7860

# Start application
CMD ["python", "main.py"]