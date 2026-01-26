# Device Tools

Docker stack for Device Registration and Statistics APIs - FastAPI + PostgreSQL

## Docker Images

| Image | Description | Tags |
|-------|-------------|------|
| `feugana1g/device-registration-api` | Internal registration API | `latest`, `1.0.0` |
| `feugana1g/statistics-api` | Public statistics API | `latest`, `1.0.0` |
| `postgres:16` | Database | `16` |

## Tech Stack

- Python 3.11 / FastAPI / Uvicorn
- PostgreSQL 16
- SQLAlchemy 2.0

## Endpoints

### Device Registration API (port 8001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /Device/register | Register a device |
| GET | /health | Health check |

### Statistics API (port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /Log/auth | Log a device |
| GET | /Log/auth/statistics | Stats by device type |
| GET | /health | Health check |

## Environment Variables

```
DATABASE_URL=postgresql://user:password@postgres:5432/devices
POSTGRES_DB=devices
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DEVICE_REGISTRATION_API_URL=http://device-registration-api:8000
REQUEST_TIMEOUT_SECONDS=5
LOG_LEVEL=INFO
```

## Docker Compose Deployment

```bash
git clone https://github.com/feugana/device-tools
cd device-tools
cp .env.example .env
docker-compose up -d
```

## Kubernetes Deployment

See the [`kubernetes/`](kubernetes/) folder for manifests and configuration.

Per-service docs:
- [Device Registration API](device-registration-api/readme.md)
- [Statistics API](statistics-api/readme.md)
