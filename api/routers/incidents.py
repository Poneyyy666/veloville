"""Routeur incidents.

À compléter : GET /incidents (filtre statut, pagination) et
PUT /incidents/{incident_id}/statut (rôle exploitant).
"""
import math

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Incident, User
from api.schemas import IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    statut: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    total = db.scalar(
        select(func.count()).select_from(Incident)
    ) or 0

    offset = (page - 1) * page_size

    stations = db.scalars(
        select(Incident)
        .where(Incident.statut == statut)
        .order_by(Incident.incident_id)
        .offset(offset)
        .limit(page_size)
    ).all()

    pages = math.ceil(total / page_size) if total else 0

    return db.scalars(
        items=stations,
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    ).all()