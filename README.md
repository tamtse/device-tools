# Device Tools

Stack Docker pour les APIs Device Registration et Statistics - FastAPI + PostgreSQL

## Images Docker

| Image | Description | Tags |
|-------|-------------|------|
| `feugana1g/device-registration-api` | API interne d'enregistrement | `latest`, `1.0.0` |
| `feugana1g/statistics-api` | API publique de statistiques | `latest`, `1.0.0` |
| `postgres:16-alpine` | Base de données | `16-alpine` |

## Stack technique

- Python 3.11 / FastAPI / Uvicorn
- PostgreSQL 16
- SQLAlchemy 2.0

## Endpoints

### Device Registration API (port 8001)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /Device/register | Enregistrement device |
| GET | /health | Health check |

### Statistics API (port 8000)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /Log/auth | Enregistrer un device |
| GET | /Log/auth/statistics | Stats par type de device |
| GET | /health | Health check |

## Variables d'environnement

```
DATABASE_URL=postgresql://user:password@postgres:5432/devices
POSTGRES_DB=devices
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DEVICE_REGISTRATION_API_URL=http://device-registration-api:8000
REQUEST_TIMEOUT_SECONDS=5
LOG_LEVEL=INFO
```

## Déploiement Docker Compose

```bash
git clone https://github.com/feugana/device-tools
cd device-tools
cp .env.example .env
docker-compose up -d
```

## Déploiement Kubernetes

Voir le dossier [`kubernetes/`](kubernetes/) pour les manifestes et la configuration.

Documentation par service :
- [Device Registration API](device-registration-api/readme.md)
- [Statistics API](statistics-api/readme.md)
