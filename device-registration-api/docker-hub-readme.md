# Device Registration API

[![Docker Image Size (latest)](https://img.shields.io/docker/image-size/feugana1g/device-registration-api/latest?color=orange)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Pulls](https://img.shields.io/docker/pulls/feugana1g/device-registration-api?color=blue)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Stars](https://img.shields.io/docker/stars/feugana1g/device-registration-api?color=yellow)](https://hub.docker.com/r/feugana1g/device-registration-api)

Internal device registration API - FastAPI + PostgreSQL

## Quick Start
```bash
docker pull feugana1g/device-registration-api:latest

docker run -d \
  -p 8001:8000 \
  -e DATABASE_URL=postgresql://user:password@postgres:5432/devices \
  feugana1g/device-registration-api:latest
```

## Endpoints

- `POST /Device/register` - Register a device
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

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
    image: postgres:16
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

- `latest` - Latest version
- `x.y.z` - Specific version
- `x.y.z-YYYYMMDD` - Dated version

Full documentation: [GitHub](https://github.com/feugana/device-tools)
