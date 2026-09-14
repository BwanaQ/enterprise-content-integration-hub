from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.health import check_database, check_redis
from app.db.session import get_db


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/readiness")
def readiness_check(db: Session = Depends(get_db)):
    database_healthy = check_database(db)
    redis_healthy = check_redis()

    dependencies = {
        "database": "ok" if database_healthy else "unavailable",
        "redis": "ok" if redis_healthy else "unavailable",
    }

    if database_healthy and redis_healthy:
        return {
            "status": "ready",
            "dependencies": dependencies,
        }

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "not_ready",
            "dependencies": dependencies,
        },
    )