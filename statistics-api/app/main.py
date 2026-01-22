from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.statistics import router as statistics_router
from app.__version__ import __version__
from app.api.health import router as health_router

app = FastAPI(
    title="Statistic API",
    version=__version__
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(statistics_router)
