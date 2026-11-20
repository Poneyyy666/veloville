"""Connexion à PostgreSQL (SQLAlchemy 2).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.config import DATABASE_URL

# Connexion générale à PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Fabrique de sessions injectées dans les endpoints.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Classe de base commune à tous les modèles."""
    pass


def get_db():
    """Injecte une session SQLAlchemy puis la ferme après usage."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()