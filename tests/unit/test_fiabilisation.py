"""Tests unitaires des règles de fiabilisation.
"""

from api.services.fiabilisation import correction_doublons, capacite_zero, format_date, correlation_dates, correlation_cible, id_existant, correlation_usager, technicien_manquant, station_manquante, format_statut
import pytest
import pandas as pd
from datetime import date

def test_correction_doublons():
    df = pd.DataFrame({
        "id": [1, 2, 1],
        "nom": ["A", "B", "A"]
    })
    df_clean, invalides = correction_doublons(df, "stations.csv")

    assert len(df_clean) == 2
    assert len(invalides) == 1
    assert invalides[0]["identifiant"] == 2
    assert invalides[0]["fichier_source"] == "stations.csv"
    assert invalides[0]["colonne"] == "toutes"
    assert invalides[0]["valeur"] == "/"
    assert invalides[0]["motif"] == "lignes dupliquées"
    assert invalides[0]["décision"] == "rejet"


def test_capacite_zero():
    df = pd.DataFrame({
        "station": ["S1", "S2", "S3"],
        "capacite": [10, 0, -5]
    })
    df_clean, invalides = capacite_zero(df)

    assert len(df_clean) == 1
    assert df_clean.iloc[0]["station"] == "S1"
    assert len(invalides) == 2
    assert invalides[0]["identifiant"] == 1
    assert invalides[0]["valeur"] == 0
    assert invalides[1]["identifiant"] == 2
    assert invalides[1]["valeur"] == -5
    assert invalides[0]["décision"] == "rejet"


def test_format_date():
    df = pd.DataFrame({
        "date_col": ["2026-05-10", "15/06/2026 14:30", None]
    })
    df_clean, invalides = format_date(df, "incidents.csv", "date_col", "%Y-%m-%d")

    assert df_clean.loc[0, "date_col"] == date(2026, 5, 10)
    assert df_clean.loc[1, "date_col"] == date(2026, 6, 15)
    assert pd.isna(df_clean.loc[2, "date_col"])
    assert len(invalides) == 2
    assert invalides[0]["identifiant"] == 0
    assert invalides[0]["valeur"] == "2026-05-10"
    assert invalides[1]["identifiant"] == 1
    assert invalides[1]["valeur"] == "15/06/2026 14:30"
    assert invalides[1]["décision"] == "modification"


def test_correlation_dates():
    df = pd.DataFrame({
        "date_signalement": pd.to_datetime(["2026-01-01", "2026-01-05", "2026-01-03", "2026-01-02"]),
        "date_resolution": pd.to_datetime(["2026-01-02", "2026-01-04", "2026-01-03", None])
    })
    df_clean, invalides = correlation_dates(df)

    assert list(df_clean.index) == [0, 3]
    assert len(invalides) == 2
    assert [err["identifiant"] for err in invalides] == [1, 2]
    assert invalides[0]["décision"] == "rejet"


def test_correlation_cible():
    df = pd.DataFrame({
        "cible": ["velo", "velo", "station", "station"],
        "velo_id": ["V1", "V2", None, "V3"],
        "station_id": [None, "S1", "S2", "S3"]
    })
    df_clean, invalides = correlation_cible(df)

    assert list(df_clean.index) == [0, 2]
    assert len(invalides) == 2
    assert [err["identifiant"] for err in invalides] == [1, 3]
    assert invalides[0]["décision"] == "rejet"


def test_id_existant():
    df = pd.DataFrame({"velo_id": ["V1", "V99", None]})
    df_ref = pd.DataFrame({"id": ["V1", "V2"]})

    df_clean, invalides = id_existant(df, df_ref, "velo_id", "id", "trajets.csv")

    assert list(df_clean.index) == [0, 2]
    assert len(invalides) == 1
    assert invalides[0]["identifiant"] == 1
    assert invalides[0]["valeur"] == "V99"
    assert invalides[0]["décision"] == "rejet"


def test_correlation_usager():
    df = pd.DataFrame({
        "type_usager": ["occasionnel", "occasionnel", "abonne", "abonne"],
        "usager_ref": [None, "U123", "U456", None]
    })
    df_clean, invalides = correlation_usager(df)

    assert list(df_clean.index) == [0, 2]
    assert len(invalides) == 2
    assert [err["identifiant"] for err in invalides] == [1, 3]
    assert invalides[0]["décision"] == "rejet"


def test_technicien_manquant():
    df = pd.DataFrame({
        "statut": ["resolu", "resolu", "ouvert", "en_cours", "en_cours"],
        "technicien": ["Tech1", None, None, None, "Tech2"]
    })
    invalides = technicien_manquant(df)

    assert len(invalides) == 2
    assert [err["identifiant"] for err in invalides] == [1, 3]
    assert all(err["décision"] == "gardé" for err in invalides)


def test_station_manquante():
    df = pd.DataFrame({
        "station_arrivee": ["S1", None, "S2"]
    })
    invalides = station_manquante(df)

    assert len(invalides) == 1
    assert invalides[0]["identifiant"] == 1
    assert pd.isna(invalides[0]["valeur"])
    assert invalides[0]["décision"] == "gardé"


def test_format_statut():
    df = pd.DataFrame({
        "statut": ["ouvert", "RESOLU", "En_Cours"]
    })
    df_clean, invalides = format_statut(df)

    assert list(df_clean["statut"]) == ["ouvert", "resolu", "en_cours"]
    assert len(invalides) == 2
    assert invalides[0]["identifiant"] == 1
    assert invalides[0]["valeur"] == "RESOLU"
    assert invalides[1]["identifiant"] == 2
    assert invalides[1]["valeur"] == "En_Cours"
    assert invalides[0]["décision"] == "rejet"