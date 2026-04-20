# ──────────────────────────────────────────────────────────────────────────────
# SkillDelta Backend — Hugging Face Spaces Docker Image
# Port: 7860 (required by HF Spaces)
# User: appuser (uid=1000, required by HF Spaces security policy)
# ──────────────────────────────────────────────────────────────────────────────

FROM python:3.13.1-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (uid=1000) — required by Hugging Face Spaces
RUN useradd -m -u 1000 appuser

# Set working directory and give ownership to appuser
WORKDIR /app
RUN chown -R appuser:appuser /app

# Install Python dependencies as root (before switching user)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# HF Spaces listens on port 7860
ENV PORT=7860
EXPOSE 7860

# Start the app
CMD ["uvicorn", "skillrot_app.main:app", "--host", "0.0.0.0", "--port", "7860"]
