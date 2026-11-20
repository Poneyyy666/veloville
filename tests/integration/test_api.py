"""Tests d'intégration de l'API avec TestClient.
"""

from api.routers.incidents import list_incidents, update_dataset
from datetime import datetime, timezone
import pytest
from api.models import Incident
from tests.conftest import creer_incident_test

URL = "/incidents"

def test_list_incidents_tous_exploitant(client, db_session, exploitant_token):
    inc1 = creer_incident_test(incident_id="INC_T1", statut="ouvert")
    inc2 = creer_incident_test(incident_id="INC_T2", statut="en cours")
    inc3 = creer_incident_test(incident_id="INC_T3", statut="resolu")
    db_session.add_all([inc1, inc2, inc3])
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.get(
        URL,
        params={"statut": "Tous", "page": 1, "page_size": 5},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "incidents" in data
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["total"] >= 3
    assert len(data["incidents"]) <= 5


def test_list_incidents_filtre_statut_direction(client, db_session, direction_token):
    inc1 = creer_incident_test(incident_id="INC_F1", statut="ouvert")
    inc2 = creer_incident_test(incident_id="INC_F2", statut="resolu")
    db_session.add_all([inc1, inc2])
    db_session.flush()

    headers = {"Authorization": f"Bearer {direction_token}"}
    response = client.get(
        URL,
        params={"statut": "ouvert", "page": 1, "page_size": 10},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert all(item["statut"] == "ouvert" for item in data["incidents"])


def test_list_incidents_sans_token(client):
    response = client.get(URL, params={"statut": "Tous"})
    assert response.status_code in (401, 403)


def test_list_incidents_pagination_invalide(client, exploitant_token):
    headers = {"Authorization": f"Bearer {exploitant_token}"}
    # page_size > 50 doit déclencher une erreur 422
    response = client.get(
        URL,
        params={"statut": "Tous", "page": 1, "page_size": 100},
        headers=headers,
    )
    assert response.status_code == 422


def test_update_incident_ouvert_vers_en_cours(client, db_session, exploitant_token):
    inc = creer_incident_test(incident_id="INC_UPD_1", statut="ouvert")
    db_session.add(inc)
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.put(
        f"{URL}/INC_UPD_1",
        params={"id_incident": "INC_UPD_1", "status_incident": "en cours"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["statut"] == "en cours"


def test_update_incident_en_cours_vers_resolu(client, db_session, exploitant_token):
    inc = creer_incident_test(incident_id="INC_UPD_2", statut="en cours")
    db_session.add(inc)
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.put(
        f"{URL}/INC_UPD_2",
        params={"id_incident": "INC_UPD_2", "status_incident": "resolu"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["statut"] == "resolu"
    if "date_resolution" in data:
        assert data["date_resolution"] is not None


def test_update_incident_transition_interdite(client, db_session, exploitant_token):
    inc = creer_incident_test(incident_id="INC_UPD_3", statut="resolu")
    db_session.add(inc)
    db_session.flush()

    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.put(
        f"{URL}/INC_UPD_3",
        params={"id_incident": "INC_UPD_3", "status_incident": "ouvert"},
        headers=headers,
    )

    assert response.status_code == 400
    assert "Transition impossible" in response.json()["detail"]


def test_update_incident_introuvable(client, exploitant_token):
    headers = {"Authorization": f"Bearer {exploitant_token}"}
    response = client.put(
        f"{URL}/INC_INEXISTANT",
        params={"id_incident": "INC_INEXISTANT", "status_incident": "en cours"},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident introuvable"


def test_update_incident_interdit_pour_direction(client, db_session, direction_token):
    inc = creer_incident_test(incident_id="INC_UPD_4", statut="ouvert")
    db_session.add(inc)
    db_session.flush()

    headers = {"Authorization": f"Bearer {direction_token}"}
    response = client.put(
        f"{URL}/INC_UPD_4",
        params={"id_incident": "INC_UPD_4", "status_incident": "en cours"},
        headers=headers,
    )

    assert response.status_code == 403


def test_login_succes(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "exploitant01",
            "password": "Formation2026!",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
    assert data["role"] == "exploitant"


def test_login_mauvais_mot_de_passe(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "exploitant01",
            "password": "MauvaisPassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"


def test_login_utilisateur_inexistant(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "MauvaisUsername",
            "password": "Formation2026!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"


def test_login_payload_invalide(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "exploitant01",
        },
    )

    assert response.status_code == 422


def test_sante(client):
    response = client.get("/sante")

    assert response.status_code == 200
    assert response.json() == {"statut": "ok"}