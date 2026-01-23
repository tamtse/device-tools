FROM python:3.11-slim

ARG API_VERSION=1.0.0
ARG BUILD_DATE
ARG VCS_REF

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
LABEL version="${API_VERSION}" \
      build-date="${BUILD_DATE}" \
      vcs-ref="${VCS_REF}"


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
