from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.__version__ import __version__

app = FastAPI(
    title="Statistic API",
    version=__version__
)

app.include_router(auth_router)
