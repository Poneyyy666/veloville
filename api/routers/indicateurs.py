"""Routeur indicateurs.
"""

import math
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import User
from api.schemas import TrajetPopulaireResponse, TrajetPeriodeResponse, IncidentStatusResponse
from api.services.indicateurs import trajets_periode, trajets_stations, incidents_statut
from api.dependencies import require_roles

router = APIRouter(prefix="/indicateurs", tags=["Indicateurs"])

@router.get("/trajet_periode", response_model=list[TrajetPeriodeResponse])
def get_trajets_periode(
    date_debut: datetime,
    date_fin: datetime,
    db: Session = Depends(get_db),
    current_manager: User = Depends(require_roles("exploitant", "direction")),
):

    trajets = trajets_periode(date_debut, date_fin, db)

    return trajets

@router.get("/trajets_stations", response_model=list[TrajetPopulaireResponse])
def get_trajets_stations(
    limit: int,
    db: Session = Depends(get_db),
    current_manager: User = Depends(require_roles("exploitant", "direction")),
):

    trajets = trajets_stations(limit, db)

    return trajets

@router.get("/incidents_statut", response_model=list[IncidentStatusResponse])
def get_incidents_statut(
    limit: int,
    db: Session = Depends(get_db),
    current_manager: User = Depends(require_roles("exploitant", "direction")),
):

    incidents = incidents_statut(limit, db)

    return incidents