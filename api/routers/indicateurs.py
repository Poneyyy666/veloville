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
from api.schemas import IncidentResponse, TrajetPopulaireResponse, TrajetPeriodeResponse
from api.services.indicateurs import trajets_periode, trajets_stations, incidents_statut

router = APIRouter(prefix="/indicateurs", tags=["Indicateurs"])

@router.get("/trajet_periode", response_model=list[TrajetPeriodeResponse])
def get_trajets_periode(
    date_debut: datetime,
    date_fin: datetime,
    db: Session = Depends(get_db),
):

    trajets = trajets_periode(date_debut, date_fin, db)

    return trajets

@router.get("/trajets_stations", response_model=list[TrajetPopulaireResponse])
def get_trajets_stations(
    limit: int,
    db: Session = Depends(get_db),
):

    trajets = trajets_stations(limit, db)

    return trajets

@router.get("/incidents_statut", response_model=IncidentResponse)
def get_incidents_statut(
    db: Session = Depends(get_db),
):

    incidents, duree = incidents_statut(db)

    return incidents, duree