"""Routeur indicateurs.

À compléter : GET /indicateurs/activite-par-jour,
GET /indicateurs/stations-actives et
GET /indicateurs/incidents-par-statut.
"""

import math
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Trajet, Incident
from api.schemas import TrajetResponse, IncidentResponse
from api.services.indicateurs import trajets_periode, trajets_stations, incidents_statut

router = APIRouter(prefix="/indicateurs", tags=["Indicateurs"])

@router.get("/", response_model=TrajetResponse)
def get_public_dataset(
    date_debut: datetime,
    date_fin: datetime,
    db: Session = Depends(get_db),
):

    trajets = trajets_periode(date_debut, date_fin, db)

    return trajets

@router.get("/", response_model=TrajetResponse)
def get_public_dataset(
    limit: int,
    db: Session = Depends(get_db),
):

    trajets = trajets_stations(limit, db)

    return trajets

@router.get("/", response_model=IncidentResponse)
def get_public_dataset(
    db: Session = Depends(get_db),
):

    incidents, duree = incidents_statut(db)

    return incidents, duree