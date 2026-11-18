"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
import sys
from fastapi import Depends
from sqlalchemy import select, func, union_all
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
    total_alias = func.count().label("totalamount")

    trajets = (
        select(
            Trajet.depart_horodatage, 
            total_alias
        ).where(
            Trajet.depart_horodatage >= date_debut,
            Trajet.depart_horodatage <= date_fin,
        ).group_by(
            Trajet.depart_horodatage,
        ).order_by(
            total_alias.desc())
    )

    result = db.execute(trajets).all()
    return [
        {
            "depart_horodatage": row.depart_horodatage,
            "totalamount": row.totalamount,
        }
        for row in result
    ]

def trajets_stations(
    limit: int,
    db: Session = Depends(get_db),
):
    departs = select(Trajet.station_depart.label("station"))
    arrivees = select(Trajet.station_arrivee.label("station"))

    stations = union_all(departs, arrivees).subquery()
    total_alias = func.count().label("totalamount")

    stmt = (
        select(
            stations.c.station,
            total_alias,
        )
        .group_by(stations.c.station)
        .order_by(total_alias.desc())
        .limit(limit)
    )

    result = db.execute(stmt).all()
    return [
        {
            "station": row.station,
            "totalamount": row.totalamount,
        }
        for row in result
    ]

def incidents_statut(
    limit: int,
    db: Session = Depends(get_db)
):
    total_alias = func.count(Incident.statut).label("totalamount")
    duree_alias = func.avg(Incident.date_resolution - Incident.date_signalement).label("duree_moyenne")

    query = (
        select(
            Incident.statut, 
            total_alias,
            duree_alias
        )
        .group_by(Incident.statut)
        .order_by(total_alias.desc())  # Tri décroissant correct
        .limit(limit)
    )

    result = db.execute(query).all()

    return [
        {
            "statut": row.statut,
            "totalamount": row.totalamount,
            "duree_moyenne_execution": row.duree_moyenne
        }
        for row in result
    ]

# def incidents_statut(
#     limit: int,
#     db: Session = Depends(get_db)
# ):
#     incidents = db.scalar(select(
#         Incident.statut, 
#         func.count(Incident.statut).label("totalamount")
#     ).group_by(
#         Incident.statut
#     ).order_by(
#         func.desc("totalamount")
#     ).limit(limit)
#     ).all()

#     duree = Incident.date_signalement - Incident.date_resolution

#     return (incidents, duree)