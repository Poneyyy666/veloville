"""Routeur stations.

À compléter : GET /stations (filtre commune, pagination) et GET /stations/{station_id}.
"""

import math

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Station, User
from api.schemas import StationResponse, PaginatedStationsResponse

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("", response_model=PaginatedStationsResponse)
def list_stations(
    commune: str  = Query(default="Toutes"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    count_stmt = select(func.count()).select_from(Station)
    if commune != "Toutes":
        count_stmt = count_stmt.where((Station.commune == commune))

    total = db.scalar(count_stmt) or 0

    offset = (page - 1) * page_size

    if commune == "Toutes" :
        stations = db.scalars(
            select(Station)
            .order_by(Station.station_id)
            .offset(offset)
            .limit(page_size)
        ).all()
    else :
        stations = db.scalars(
            select(Station)
            .where((Station.commune == commune))
            .order_by(Station.station_id)
            .offset(offset)
            .limit(page_size)
        ).all()

    stations_response = [
      StationResponse.model_validate(s) for s in stations
    ]

    pages = math.ceil(total / page_size) if total else 0

    return PaginatedStationsResponse(
        stations=stations_response,
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
    )

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