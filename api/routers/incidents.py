"""Routeur incidents.

À compléter : GET /incidents (filtre statut, pagination) et
PUT /incidents/{incident_id}/statut (rôle exploitant).
"""
import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Incident, User
from api.schemas import IncidentResponse, PaginatedIncidentsResponse, IncidentUpdate, IncidentsIdsResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=PaginatedIncidentsResponse)
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

    if statut == "Tous" :
        incidents = db.scalars(
            select(Incident)
            .order_by(Incident.incident_id)
            .offset(offset)
            .limit(page_size)
        ).all()
    else :
        incidents = db.scalars(
            select(Incident)
            .where(Incident.statut == statut)
            .order_by(Incident.incident_id)
            .offset(offset)
            .limit(page_size)
        ).all()

    incidents_response = [
        IncidentResponse.model_validate(s) for s in incidents
    ]

    pages = math.ceil(total / page_size) if total else 0

    return PaginatedIncidentsResponse(
        incidents=incidents_response,
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    )

@router.get("/incidents_ids")
def list_incidents(
    db: Session = Depends(get_db),
):
    incidents = db.scalars(select(Incident)).all()
    ids = []
    for row in incidents :
        ids.append(row.incident_id)

    return list(ids)

@router.put("/{dataset_id}", response_model=IncidentResponse)
def update_dataset(
    id_incident: str,
    status_incident: str,
    db: Session = Depends(get_db),
):
    """Modifie uniquement le statut d'un incident selon les transitions autorisées."""

    TRANSITIONS_AUTORISEES = {
        "ouvert": {"en cours", "resolu"},
        "en cours": {"resolu"},
        "resolu": set(),
    }

    incident = db.get(Incident, id_incident)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident introuvable",
        )

    statut_actuel = incident.statut

    statuts_possibles = TRANSITIONS_AUTORISEES.get(statut_actuel, set())
    if status_incident not in statuts_possibles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transition impossible : un incident '{statut_actuel}' ne peut pas passer à '{status_incident}'.",
        )

    incident.statut = status_incident

    if status_incident == "resolu" and hasattr(incident, "date_resolution"):
        incident.date_resolution = datetime.now(timezone.utc)

    db.commit()
    db.refresh(incident)

    return incident