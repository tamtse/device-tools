from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.db import models  # Import models to register them with Base
from app.core.logging import get_logger

logger = get_logger(__name__)


async def init_db():
    logger.info("Database initialization .....")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    logger.info("Close database connections")
    await engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.error("FastAPI lifespan context manager for database initialization.")
    # Startup: Create database tables
    await init_db()
    yield
    # Shutdown: Close database connections
    await close_db()
