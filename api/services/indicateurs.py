"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
import sys
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import date

sys.path.append('../veloville')
from api.database import get_db
from api.models import Incident, Trajet

def trajets_periode(
    date_debut : date, 
    date_fin : date,
    db: Session = Depends(get_db)
):
    trajets = db.scalar(
        select(
            Trajet.station_depart, 
            func.count(Trajet.station_depart).label("totalamount")
        ).where(
            Trajet.depart_horodatage >= date_debut,
            Trajet.depart_horodatage <= date_fin,
        ).group_by(
            Trajet.station_depart
        ).order_by(
            func.desc("totalamount"))
    ).all()

    return trajets

def trajets_stations(
    limit: int,
    db: Session = Depends(get_db)
):
    trajets = db.scalar(select(
        Trajet.station_depart, 
        Trajet.station_arrivee, 
        func.count("*").label("totalamount")
    ).group_by(
        Trajet.station_depart,
        Trajet.station_arrivee
    ).order_by(
        func.desc("totalamount")
    ).limit(limit)
    ).all()

    return trajets

def incidents_statut(
    limit: int,
    db: Session = Depends(get_db)
):
    incidents = db.scalar(select(
        Incident.statut, 
        func.count(Incident.statut).label("totalamount")
    ).group_by(
        Incident.statut
    ).order_by(
        func.desc("totalamount")
    ).limit(limit)
    ).all()

    duree = Incident.date_signalement - Incident.date_resolution

    return (incidents, duree)