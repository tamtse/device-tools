from fastapi import FastAPI
from app.api.register import router as register_router

app = FastAPI(
    title="Device Registration API",
    version="1.0.0"
)

app.include_router(register_router)
