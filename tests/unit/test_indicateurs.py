"""Tests des fonctions de calcul des indicateurs.
"""

from datetime import datetime, timezone
import pytest
from api.models import Trajet, Incident
from tests.conftest import creer_incident_test, creer_trajet_test

URL = "/indicateurs"

def test_get_trajets_periode_succes_exploitant(client, db_session, exploitant_token):
    t1 = creer_trajet_test(
        db_session,
        trajet_id="TRJ_P1",
        depart_horodatage=datetime(2026, 5, 10, 10, 0, tzinfo=timezone.utc),
    )
    t2 = creer_trajet_test(
        db_session,
        trajet_id="TRJ_P2",
        depart_horodatage=datetime(2026, 5, 10, 10, 0, tzinfo=timezone.utc),
    )
    t_hors = creer_trajet_test(
        db_session,
        trajet_id="TRJ_P3",
        depart_horodatage=datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc),
    )
    db_session.add_all([t1, t2, t_hors])
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    params = {
        "date_debut": "2026-05-01T00:00:00",
        "date_fin": "2026-05-31T23:59:59",
    }

    response = client.get(f"{URL}/trajet_periode", params=params, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["totalamount"] >= 2 for item in data)


def test_get_trajets_periode_succes_direction(client, direction_token):
    headers = {"Authorization": f"Bearer {direction_token}"}
    params = {
        "date_debut": "2026-05-01T00:00:00",
        "date_fin": "2026-05-31T23:59:59",
    }

    response = client.get(f"{URL}/trajet_periode", params=params, headers=headers)
    assert response.status_code == 200


def test_get_trajets_periode_sans_token(client):
    params = {
        "date_debut": "2026-05-01T00:00:00",
        "date_fin": "2026-05-31T23:59:59",
    }
    response = client.get(f"{URL}/trajet_periode", params=params)
    assert response.status_code in (401, 403)


def test_get_trajets_periode_parametres_manquants(client, exploitant_token):
    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.get(f"{URL}/trajet_periode", headers=headers)
    assert response.status_code == 422



def test_get_trajets_stations_succes(client, db_session, exploitant_token):
    trajets = [
        creer_trajet_test(
            db_session,
            trajet_id="TRJ_S1",
            station_depart="ST1",
            station_arrivee="ST2",
        ),
        creer_trajet_test(
            db_session,
            trajet_id="TRJ_S2",
            station_depart="ST1",
            station_arrivee="ST3",
        ),
    ]
    db_session.add_all(trajets)
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.get(f"{URL}/trajets_stations", params={"limit": 5}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_get_trajets_stations_sans_token(client):
    response = client.get(f"{URL}/trajets_stations", params={"limit": 5})
    assert response.status_code in (401, 403)



def test_get_incidents_statut_succes_exploitant(client, db_session, exploitant_token):
    inc1 = creer_incident_test(
        incident_id="INC_ST1",
        statut="resolu",
        date_signalement=datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc),
        date_resolution=datetime(2026, 5, 3, 10, 0, tzinfo=timezone.utc),
    )
    inc2 = creer_incident_test(
        incident_id="INC_ST2",
        statut="ouvert",
        date_signalement=datetime(2026, 5, 2, 10, 0, tzinfo=timezone.utc),
        date_resolution=datetime(2026, 5, 2, 12, 0, tzinfo=timezone.utc),
    )
    db_session.add_all([inc1, inc2])
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.get(f"{URL}/incidents_statut", params={"limit": 10}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_incidents_statut_role_direction(client, direction_token):
    headers = {"Authorization": f"Bearer {direction_token}"}
    response = client.get(f"{URL}/incidents_statut", params={"limit": 10}, headers=headers)

    assert response.status_code == 200