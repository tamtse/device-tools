# Device Registration API

[![Docker Image Size (latest)](https://img.shields.io/docker/image-size/feugana1g/device-registration-api/latest?color=orange)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Pulls](https://img.shields.io/docker/pulls/feugana1g/device-registration-api?color=blue)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Stars](https://img.shields.io/docker/stars/feugana1g/device-registration-api?color=yellow)](https://hub.docker.com/r/feugana1g/device-registration-api)

API interne d'enregistrement des devices - FastAPI + PostgreSQL

## Quick Start
```bash
docker pull feugana1g/device-registration-api:latest

docker run -d \
  -p 8001:8000 \
  -e DATABASE_URL=postgresql://user:password@postgres:5432/devices \
  feugana1g/device-registration-api:latest
```

## Endpoints

- `POST /Device/register` - Enregistrement device
- `GET /health` - Health check
- `GET /docs` - Documentation Swagger

## Configuration
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
LOG_LEVEL=INFO
REQUEST_TIMEOUT_SECONDS=5
```

## Docker Compose
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: devices
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

  device-registration-api:
    image: feugana1g/device-registration-api:latest
    ports:
      - "8001:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/devices
```

## Tags

- `latest` - Dernière version
- `x.y.z` - Version spécifique
- `x.y.z-YYYYMMDD` - Version datée

Documentation complète : [GitHub](https://github.com/feugana/device-tools)