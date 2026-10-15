"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
import sys
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import date

sys.path.append('../veloville')
from api.database import get_db
from api.models import Station, Trajet, User

def trajets_periode(
    date_debut : date, 
    date_fin : date,
    db: Session = Depends(get_db)
):
    dataset = db.scalar(
        select(Trajet).where(
            Trajet.depart_horodatage >= date_debut,
            Trajet.depart_horodatage <= date_fin,
        )
    ).all()

    return len(dataset)

def trajets_stations(
    db: Session = Depends(get_db)
):
    dataset = db.query(Trajet.station_depart, func.count(Trajet.station_depart)).group_by(Trajet.station_depart).all()

    return len(dataset)

def incidents_statut(
    db: Session = Depends(get_db)
):
    dataset = db.query(Trajet.station_depart, func.count(Trajet.station_depart)).group_by(Trajet.station_depart).all()

    return len(dataset)