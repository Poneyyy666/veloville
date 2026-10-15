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
from api.schemas import IncidentResponse, PaginatedIncidentsResponse

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

# @router.put("/{dataset_id}", response_model=IncidentResponse)
# def update_dataset(
#     dataset_id: int,
#     data: IncidenttUpdate,
#     db: Session = Depends(get_db),
#     # current_user: User = Depends(require_roles("manager")),
# ):
#     """Modifie un dataset."""

#     incident = db.get(Incident, dataset_id)

#     if incident is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Incident introuvable",
#         )

#     for field, value in data.model_dump().items():
#         setattr(incident, field, value)

#     db.commit()
#     db.refresh(incident)

#     return incident