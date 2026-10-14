"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from api.database import get_db
from api.models import Station, Trajet, User

def list_public_datasets(
    date_debut : date, 
    date_fin : date,
    db: Session = Depends(get_db)
):
    dataset = db.scalar(
        select(Trajet).where(
            Trajet.depart_horodatage >= date_debut,
            Trajet.depart_horodatage <= date_fin,
        )
    )

    return len(dataset)