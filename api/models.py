"""Modèles ORM SQLAlchemy : Station, Trajet, Incident, Utilisateur.
"""

import sys
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

sys.path.append('../veloville')
from api.database import Base


class User(Base):
    """Utilisateur de l'API."""

    __tablename__ = "utilisateur"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # Seul le hash bcrypt est enregistré.
    password_hash: Mapped[str] = mapped_column(String(100))

    # viewer, analyst ou manager.
    role: Mapped[str] = mapped_column(String(20), default="viewer")


class Station(Base):
    """Jeu de données référencé dans le catalogue."""

    __tablename__ = "stations"

    station_id: Mapped[str] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(50))
    commune: Mapped[str] = mapped_column(String(50))
    capacite: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    date_mise_en_service: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Trajet(Base):
    """Jeu de données référencé dans le catalogue."""

    __tablename__ = "trajets"

    trajet_id: Mapped[str] = mapped_column(primary_key=True)
    velo_id: Mapped[str] = mapped_column(String(10))
    depart_horodatage: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    station_depart: Mapped[str] = mapped_column(String(10))
    station_arrivee: Mapped[str] = mapped_column(String(10))
    duree_secondes: Mapped[int] = mapped_column(Integer)
    type_usager: Mapped[str] = mapped_column(String(25))
    usager_ref: Mapped[str] = mapped_column(String(10))


class Incident(Base):
    """Jeu de données référencé dans le catalogue."""

    __tablename__ = "incidents"

    incident_id: Mapped[str] = mapped_column(primary_key=True)
    date_signalement: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    cible: Mapped[str] = mapped_column(String(10))
    velo_id: Mapped[str] = mapped_column(String(10))
    station_id: Mapped[str] = mapped_column(String(10))
    type_incident: Mapped[str] = mapped_column(String(25))
    statut: Mapped[str] = mapped_column(String(25))
    date_resolution: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    technicien: Mapped[str] = mapped_column(String(50))