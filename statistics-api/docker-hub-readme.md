# Statistics API

[![Docker Image Size (latest)](https://img.shields.io/docker/image-size/feugana1g/statistics-api/latest?color=orange)](https://hub.docker.com/r/feugana1g/statistics-api)
[![Docker Pulls](https://img.shields.io/docker/pulls/feugana1g/statistics-api?color=blue)](https://hub.docker.com/r/feugana1g/statistics-api)
[![Docker Stars](https://img.shields.io/docker/stars/feugana1g/statistics-api?color=yellow)](https://hub.docker.com/r/feugana1g/statistics-api)

API publique de statistiques et logs d'authentification - FastAPI + PostgreSQL

## Quick Start
```bash
docker pull feugana1g/statistics-api:latest

docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@postgres:5432/devices \
  -e DEVICE_REGISTRATION_API_URL=http://device-registration-api:8000 \
  feugana1g/statistic-api:latest
```

## Endpoints

- `POST /Log/auth` - Enregistrer un log d'authentification
- `GET /Log/auth/statistics` - Statistiques par type de device
- `GET /health` - Health check
- `GET /docs` - Documentation Swagger

## Configuration
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
DEVICE_REGISTRATION_API_URL=http://device-registration:8000
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
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/devices

  statistics-api:
    image: feugana1g/statistics-api:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/devices
      DEVICE_REGISTRATION_API_URL: http://device-registration-api:8000
```

## Tags

- `latest` - Dernière version
- `x.y.z` - Version spécifique
- `x.y.z-YYYYMMDD` - Version datée

Documentation complète : [GitHub](https://github.com/feugana/device-tools)