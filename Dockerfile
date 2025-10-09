﻿FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements-production.txt ./
RUN pip install --no-cache-dir -r requirements-production.txt

COPY working_api.py .
COPY rate_limit_handler.py .
COPY api_key_rotation.py .
COPY orche.env .

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "working_api:app"]
