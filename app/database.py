from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from typing import Any


# SQLite database URL (relative path to the database file)
SQLALCHEMY_DATABASE_URL = "sqlite:///./project.db"

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()