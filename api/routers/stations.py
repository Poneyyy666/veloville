"""Routeur stations.

À compléter : GET /stations (filtre commune, pagination) et GET /stations/{station_id}.
"""

import math

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Station, User
from api.schemas import StationResponse

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("", response_model=list[StationResponse])
def list_stations(
    commune: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    total = db.scalar(
        select(func.count()).select_from(Station)
    ) or 0

    offset = (page - 1) * page_size

    stations = db.scalars(
        select(Station)
        .where(Station.commune.is_(commune))
        .order_by(Station.id)
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


@router.get("/{station_id}", response_model=StationResponse)
def get_station(
    station_id: str,
    db: Session = Depends(get_db),
):

    station = db.scalar(
        select(Station).where(
            Station.station_id == station_id,
        )
    )

    if station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset introuvable",
        )

    return station