from app.database import SessionLocal

from typing import Generator

import logging


logger = logging.getLogger(__name__)

# Dependency to get a database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("DB Closed....")
        db.close()