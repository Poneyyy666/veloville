"""Schémas Pydantic (entrées et sorties de l'API).

À compléter : schémas de lecture des trois ressources, enveloppe paginée, corps de
connexion, réponse de connexion, corps de changement de statut, réponses
des trois indicateurs.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["viewer", "analyst", "manager"]
QualityStatus = Literal["PASS", "WARNING", "FAIL"]


class RegisterRequest(BaseModel):
    """Données publiques d'inscription."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str


class RoleUpdateRequest(BaseModel):
    role: Role


class StationCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=50)
    commune: str = Field(min_length=1, max_length=50)
    capacite: int = Field(gt=1)
    latitude: float
    longitude: float
    date_mise_en_service: datetime


class TrajetCreate(BaseModel):
    velo_id: str = Field(min_length=1, max_length=10)
    depart_horodatage: datetime
    station_depart: str = Field(min_length=1, max_length=10)
    station_arrivee: str = Field(min_length=1, max_length=10)
    capacite: int = Field(gt=1)
    type_usager: str = Field(min_length=1, max_length=25)
    capacite: int = Field(gt=1)
    usager_ref: str = Field(min_length=1, max_length=10)


class IncidentCreate(BaseModel):
    date_signalement: datetime
    cible: str = Field(min_length=1, max_length=10)
    velo_id: Optional[str] = Field(min_length=1, max_length=10), None
    station_id: Optional[str] = Field(min_length=1, max_length=10), None
    type_incident: str = Field(min_length=1, max_length=25)
    statut: str = Field(min_length=1, max_length=25)
    date_resolution: Optional[datetime] = None
    technicien: Optional[str] = Field(min_length=1, max_length=50), None


class DatasetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=500)
    source: str = Field(min_length=1, max_length=150)
    format: str = Field(min_length=1, max_length=30)
    is_public: bool = False


class IncidenttUpdate(IncidentCreate):
    pass


class StationResponse(StationCreate):
    model_config = ConfigDict(from_attributes=True)

    station_id: str


class TrajetResponse(TrajetCreate):
    model_config = ConfigDict(from_attributes=True)

    trajet_id: str


class IncidentResponse(IncidentCreate):
    model_config = ConfigDict(from_attributes=True)

    incident_id: str


class QualityCheckCreate(BaseModel):
    dataset_id: int = Field(gt=0)
    checked_at: datetime
    score: float = Field(ge=0, le=100)
    status: QualityStatus
    comment: str = Field(min_length=1, max_length=500)


class QualityCheckUpdate(QualityCheckCreate):
    pass


class QualityCheckResponse(QualityCheckCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int

class PaginatedStationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stations: list

    # Informations nécessaires au client pour construire sa navigation.
    page: int
    page_size: int
    total: int
    pages: int

class PaginatedIncidentsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    incidents: list

    # Informations nécessaires au client pour construire sa navigation.
    page: int
    page_size: int
    total: int
    pages: int

class TrajetPeriodeResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  depart_horodatage: datetime
  totalamount: int

class TrajetPopulaireResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  station_depart: str
  station_arrivee: Optional[str] = None
  totalamount: int