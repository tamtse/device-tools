# Device Registration API
[![Docker Image Size (latest)](https://img.shields.io/docker/feugana1g/device-registration-api/latest?color=orange)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Pulls](https://img.shields.io/docker/pulls/feugana1g/device-registration-api?color=blue)](https://hub.docker.com/r/feugana1g/device-registration-api)
[![Docker Stars](https://img.shields.io/docker/stars/feugana1g/device-registration-api?color=yellow)](https://hub.docker.com/r/feugana1g/device-registration-api)

# Statistic API
[![Docker Image Size (latest)](https://img.shields.io/docker/feugana1g/statistic-api/latest?color=orange)](https://hub.docker.com/r/feugana1g/statistic-api)
[![Docker Pulls](https://img.shields.io/docker/pulls/feugana1g/statistic-api?color=blue)](https://hub.docker.com/r/feugana1g/statistic-api)
[![Docker Stars](https://img.shields.io/docker/stars/feugana1g/statistic-api?color=yellow)](https://hub.docker.com/r/feugana1g/statistic-api)

Docker Stack pour **Device Tools API** - FastAPI + PostgreSQL

## 🐳 Images Docker utilisées

| Image                               | Description                      | Tags              |
|-------------------------------------|----------------------------------|-------------------|
| `feugana1g/statistics-api`          | API d'enregistrement des devices | `latest`, `1.0.0` |
| `feugana1g/device-registration-api` | API d'enregistrement des devices | `latest`, `1.0.0` |
| `postgres:16-alpine`                | Base de données                  | `16-alpine`       |

## 📊 Stack technique
└── FastAPI + SQLAlchemy + Alembic + PostgreSQL
└── API: Uvicorn/FastAPI (Python 3.11)
└── DB: PostgreSQL 16
└── ORM: SQLAlchemy 2.0

## 🔗 Device Registration Service - Endpoints API
| Méthode | Endpoint         | Description           |
| ------- | ---------------- | --------------------- |
| POST    | /Device/register | Enregistrement device |
| POST    | /Device/register | Enregistrement device |
| GET     | /health          | Health Check          |
| GET     | /docs            | Documentation FastAPI |

## 🔗 Statistic Service - Endpoints API
| Méthode | Endpoint                          | Description             |
| ------- | --------------------------------- | ------------------------|
| POST    | /Log/auth                         | Store user device       |
| POST    | /Log/auth/statistics              | Get statistic by device |
| GET     | /health                           | Health Check            |
| GET     | /docs                             | Documentation FastAPI   |

## 🛠️ Variables d'environnement

 - DATABASE_URL="postgresql://user:password@postgres:5432/devices"
 - POSTGRES_DB=devices
 - POSTGRES_USER=user
 - POSTGRES_PASSWORD=password
 - DEVICE_REGISTRATION_API_URL=http://device-registration-api:8000
 - REQUEST_TIMEOUT_SECONDS=5
 - LOG_LEVEL=INFO

## 🚀 Déploiement rapide Docker Compose

```bash
git clone https://github.com/feugana/device-tools
cd device-tools
cp .env.example .env 
docker-compose up -d

📋 Configuration
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - internal
    ports:
    - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
  
  device-registration-api:
    image: feugana1g/device-registration-api:1.0.0
    restart: unless-stopped
    environment:
      DATABASE_URL: ${DATABASE_URL}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    depends_on:
      - postgres
    networks:
      - internal
    ports:
    - "8001:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  statistic-api:
    image: feugana1g/statistic-api:1.0.0
    restart: unless-stopped
    environment:
      DEVICE_REGISTRATION_API_URL: ${DEVICE_REGISTRATION_API_URL}
      DATABASE_URL: ${DATABASE_URL}
      REQUEST_TIMEOUT_SECONDS: ${REQUEST_TIMEOUT_SECONDS}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    depends_on:
      - postgres
    networks:
      - internal
      - outside 
    ports:
    - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

volumes:
  pgdata:

networks:
  internal:
  outside: #public network
```
## 🚀 Déploiement avancé sur Kubernetes

Consultez la documentation complète dans le dossier [`kubernetes/`](kubernetes/) pour :
- Configuration des manifestes
- Déploiement step-by-step
- NetworkPolicies et sécurité

Ou consultez les README spécifiques :
- [Device Registration API - Kubernetes](device-registration-api/readme.md#how-to-deploy-on-kubernetes)
- [Statistics API - Kubernetes](statistics-api/readme.md#how-to-deploy-on-kubernetes)
