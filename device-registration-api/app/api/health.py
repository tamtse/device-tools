from fastapi import APIRouter, status
from datetime import datetime
from app.__version__ import __version__

router = APIRouter(tags=["Health"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "version": __version__,
        "service": "Device Registration API",
        "timestamp": datetime.utcnow()
    }