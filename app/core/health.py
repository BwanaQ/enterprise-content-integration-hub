import logging

import redis
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings


logger = logging.getLogger(__name__)


def check_database(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("Database readiness check failed")
        return False


def check_redis() -> bool:
    client = None

    try:
        client = redis.from_url(settings.redis_url)
        client.ping()
        return True
    except Exception:
        logger.exception("Redis readiness check failed")
        return False
    finally:
        if client is not None:
            client.close()