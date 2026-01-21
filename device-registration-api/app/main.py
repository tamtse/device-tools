from fastapi import FastAPI
from app.api.register import router as register_router
from app.__version__ import __version__

app = FastAPI(
    title="Device Registration API",
    version=__version__
)

app.include_router(register_router)
