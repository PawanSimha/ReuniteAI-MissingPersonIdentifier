# syntax=docker/dockerfile:1.7
# ============================================================
# Stage 1: Builder — compile dlib + install all dependencies
# ============================================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Build toolchain required to compile dlib from source
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       cmake \
       libboost-dev \
       libboost-python-dev \
       libopenblas-dev \
       libjpeg-dev \
       zlib1g-dev \
       libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Install Python dependencies. --no-build-isolation forces builds to use the
# apt-provided CMake (3.25) instead of a pip-fetched bleeding-edge one that
# rejects dlib's bundled pybind11 (known CMake policy incompatibility).
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/opt/venv --no-build-isolation \
      --retries 10 --timeout 120 -r requirements.txt

# ============================================================
# Stage 2: Runtime — minimal image with compiled deps only
# ============================================================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    FLASK_DEBUG=False \
    PORT=8000

# Runtime libraries required by OpenCV / dlib (.so linkage)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgl1 \
       libglib2.0-0 \
       libopenblas0 \
       libjpeg62-turbo \
       libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for secure operation
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

# Installed dependencies from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PIP_NO_CACHE_DIR=1

# Application source + directory scaffolding
COPY app.py ./
COPY python_files/ ./python_files/
COPY templates/ ./templates/
COPY static/ ./static/
COPY requirements.txt .
COPY LICENSE ./
RUN mkdir -p /app/images/temp /app/images/database && chown -R appuser:appuser /app/images

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3); sys.exit(0)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "app:app"]