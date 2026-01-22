FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r app && useradd -r -g app visitor

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
RUN chmod -R 755 .

USER visitor

LABEL org.opencontainers.image.source="https://github.com/tamtse"
LABEL org.opencontainers.image.version="1.0.0"


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
