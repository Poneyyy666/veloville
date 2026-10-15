"""Routeur trajets.

À compléter : GET /trajets (filtres date_debut, date_fin, station ; pagination).
"""

import math
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Trajet, User
from api.schemas import TrajetResponse

router = APIRouter(prefix="/trajets", tags=["Trajets"])

@router.get("", response_model=list[TrajetResponse])
def list_trajets(
    date_debut: datetime,
    date_fin: datetime,
    station: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    total = db.scalar(
        select(func.count()).select_from(Trajet)
    ) or 0

    offset = (page - 1) * page_size

    trajets = db.scalars(
        select(Trajet)
        .where
            ((Trajet.depart_horodatage > (date_debut)) 
            and (Trajet.depart_horodatage < (date_fin)) 
            and (Trajet.station_depart.is_(station) or Trajet.station_arrivee.is_(station)))
        .order_by(Trajet.trajet_id)
        .offset(offset)
        .limit(page_size)
    ).all()

    pages = math.ceil(total / page_size) if total else 0

    return db.scalars(
        items=trajets,
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    ).all()