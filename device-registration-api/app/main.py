from fastapi import FastAPI
from app.api.register import router as register_router
from app.api.health import router as health_router
from app.__version__ import __version__
from app.db.init_db import lifespan
from app.core.logging import setup_logging
from app.core.config import settings

setup_logging(settings.log_level)

app = FastAPI(
    title="Device Registration API",
    version=__version__,
    lifespan=lifespan
)
app.include_router(health_router)
app.include_router(register_router)
