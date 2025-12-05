# ============================
# Stage 1: Builder
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================
# Stage 2: Runtime
# ============================
FROM python:3.14-slim AS runtime

ENV TZ=UTC
WORKDIR /app

# Install cron and tzdata
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY . /app

# Create directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Copy cron file (system cron)
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Set correct permissions (no crontab command!)
RUN chmod 0644 /etc/cron.d/2fa-cron \
    && sed -i -e '$a\' /etc/cron.d/2fa-cron  # ensure newline at EOF

# Expose API port
EXPOSE 8080

# Start cron in foreground and FastAPI app
CMD cron -f & uvicorn app.main:app --host 0.0.0.0 --port 8080
