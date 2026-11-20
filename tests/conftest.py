"""Fixtures pytest communes.
"""

import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import get_db
from api.main import app
from api.models import Trajet, Incident, Station
from datetime import datetime, timezone, timedelta

load_dotenv()
engine_test = create_engine(os.environ["TEST_DATABASE_URL"], pool_pre_ping=True)
SessionTest = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)

@pytest.fixture()
def db_session():
    connexion = engine_test.connect()
    transaction = connexion.begin()
    session = SessionTest(bind=connexion, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connexion.close()
        
@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def _login_and_get_token(
    client: TestClient,
    username: str,
    password: str,
) -> str:
    """Effectue un vrai login comme le ferait un client de l'API."""

    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture()
def exploitant_token(client):
    """JWT appartenant à un utilisateur exploitant."""

    return _login_and_get_token(
        client,
        "exploitant01",
        "Formation2026!",
    )


@pytest.fixture()
def direction_token(client):
    """JWT appartenant à un utilisateur direction."""

    return _login_and_get_token(
        client,
        "direction01",
        "Formation2026!",  
    )

def creer_station_test(db_session, station_id: str = "S01", **kwargs) -> Station:
    """Crée (ou retourne) une station dans la session de test pour satisfaire les clés étrangères."""
    existante = db_session.get(Station, station_id)
    if existante:
        return existante

    donnees = {
        "station_id": station_id,
        "nom": f"Station {station_id}",
        "commune": "Lyon",
        "capacite": 20,
        "latitude": 45.7640,
        "longitude": 4.8357,
        "date_mise_en_service": datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc),
    }
    donnees.update(kwargs)
    station = Station(**donnees)
    db_session.add(station)
    db_session.flush()
    return station


def creer_incident_test(**kwargs) -> Incident:
    """Crée un Incident cohérent avec les contraintes CHECK et NOT NULL."""
    cible = kwargs.get("cible", "velo")
    date_signalement = kwargs.get(
        "date_signalement", datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc)
    )

    donnees_defaut = {
        "incident_id": "INC_DEF",
        "date_signalement": date_signalement,
        "cible": cible,
        "velo_id": "V01" if cible == "velo" else None,
        "station_id": None if cible == "velo" else "S01",
        "type_incident": "vandalisme",
        "statut": "ouvert",
        "date_resolution": date_signalement + timedelta(hours=2),
        "technicien": "Tech Test",
    }
    donnees_defaut.update(kwargs)
    return Incident(**donnees_defaut)


def creer_trajet_test(db_session=None, **kwargs) -> Trajet:
    """Crée un Trajet et garantit l'existence des stations référencées si db_session est fourni."""
    station_depart = kwargs.get("station_depart", "S01")
    station_arrivee = kwargs.get("station_arrivee", "S02")

    if db_session is not None:
        creer_station_test(db_session, station_depart)
        creer_station_test(db_session, station_arrivee)

    donnees_defaut = {
        "trajet_id": "TRJ_DEF",
        "velo_id": "V01",
        "depart_horodatage": datetime(2026, 5, 10, 10, 0, tzinfo=timezone.utc),
        "station_depart": station_depart,
        "station_arrivee": station_arrivee,
        "duree_secondes": 600,
        "type_usager": "abonne",
        "usager_ref": "USR01",
    }
    donnees_defaut.update(kwargs)
    return Trajet(**donnees_defaut)