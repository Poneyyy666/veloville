"""Import et fiabilisation des trois exports CSV dans PostgreSQL.

À compléter : lire data/stations.csv, data/trajets.csv et data/incidents.csv,
appliquer les règles de fiabilisation (api/services/fiabilisation.py),
charger les lignes valides, journaliser les rejets et les avertissements.
Le script doit être idempotent : deux exécutions successives laissent la
base dans le même état.

Usage prévu : python scripts/importer.py [--dossier data]
"""

import sys
import psycopg2
import pandas as pd

sys.path.append('../veloville')
import api.services.fiabilisation as fi
from sqlalchemy import create_engine


import os
from dotenv import load_dotenv

# Charge les variables du fichier .env.
load_dotenv()

# Chaîne de connexion PostgreSQL.
DATABASE_URL = os.environ["DATABASE_URL"]
SORTIE_RAPPORT = "docs/journal-rejets-avertissements.md"
standard_url = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

lignes_rapport = []

def main() -> None:
    df_incidents = pd.read_csv("./data/incidents.csv")
    df_stations = pd.read_csv("./data/stations.csv")
    df_trajets = pd.read_csv("./data/trajets.csv")

    lignes_rapport = []

    engine = create_engine(standard_url)

    empty_df = pd.DataFrame()
    empty_df.to_sql('incidents', con=engine, if_exists='delete_rows',index=False)
    empty_df.to_sql('trajets', con=engine, if_exists='delete_rows',index=False)
    empty_df.to_sql('stations', con=engine, if_exists='delete_rows',index=False)

    # # ---------------------------------------------------------------------------
    # # Importation des stations.csv
    # # ---------------------------------------------------------------------------

    df_stations, lignes_ajout = fi.correction_doublons(df_stations, "stations.csv")
    lignes_rapport.append(lignes_ajout)

    df_stations, lignes_ajout = fi.capacite_zero(df_stations)
    lignes_rapport.append(lignes_ajout)

    df_stations, lignes_ajout = fi.format_date(df_stations, "stations.csv", "date_mise_en_service", "%Y-%m-%d")
    lignes_rapport.append(lignes_ajout)

    df_stations.to_sql('stations', con=engine, if_exists='delete_rows',index=False)


    # # ---------------------------------------------------------------------------
    # # Importation des trajets.csv
    # # ---------------------------------------------------------------------------

    df_trajets, lignes_ajout = fi.correction_doublons(df_trajets, "trajets.csv")
    lignes_rapport.append(lignes_ajout)

    df_trajets, lignes_ajout = fi.format_date(df_trajets, "trajets.csv", "depart_horodatage", "%Y-%m-%d %H:%M:%S")
    lignes_rapport.append(lignes_ajout)

    df_trajets, lignes_ajout = fi.correlation_usager(df_trajets)
    lignes_rapport.append(lignes_ajout)

    lignes_ajout = fi.station_manquante(df_trajets)
    lignes_rapport.append(lignes_ajout)

    df_trajets, lignes_ajout = fi.id_existant(df_trajets, df_stations, "station_depart", "station_id", "trajets.csv")
    lignes_rapport.append(lignes_ajout)

    df_trajets, lignes_ajout = fi.id_existant(df_trajets, df_stations, "station_arrivee", "station_id", "trajets.csv")
    lignes_rapport.append(lignes_ajout)

    df_trajets.to_sql('trajets', con=engine, if_exists='delete_rows',index=False)


    # # ---------------------------------------------------------------------------
    # # Importation des incidents.csv
    # # ---------------------------------------------------------------------------

    df_incidents, lignes_ajout = fi.correction_doublons(df_incidents, "incidents.csv")
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.format_date(df_incidents, "incidents.csv", "date_signalement", "%Y-%m-%d %H:%M")
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.format_date(df_incidents, "incidents.csv", "date_resolution", "%Y-%m-%d %H:%M")
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.correlation_dates(df_incidents)
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.correlation_cible(df_incidents)
    lignes_rapport.append(lignes_ajout)

    lignes_ajout = fi.technicien_manquant(df_incidents)
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.id_existant(df_incidents, df_stations, "station_id", "station_id", "incidents.csv")
    lignes_rapport.append(lignes_ajout)

    df_incidents, lignes_ajout = fi.format_statut(df_incidents)
    lignes_rapport.append(lignes_ajout)

    df_incidents.to_sql('incidents', con=engine, if_exists='delete_rows',index=False)


    with engine.begin() as conn :
        
        conn.autocommit = True

        pass

    lignes_texte = [" ".join(str(mot) for mot in ligne) for ligne in lignes_rapport]
    with open(
        SORTIE_RAPPORT,
        "w",
        encoding="utf-8",
    ) as fichier:
        fichier.write("\n".join(lignes_texte))


if __name__ == "__main__":
    main()
