"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""
import pandas as pd

def afficher_anomalie(code, description, df, masque):
    # loc[] sélectionne les lignes pour lesquelles le masque vaut True.
    lignes = df.loc[masque]

    print(f"\n=== {code} — {description} ===")
    print(f"Nombre de lignes concernées : {len(lignes)}")

    if len(lignes) > 0:
        # head(3) conserve les 3 premières lignes.
        # to_string() transforme le DataFrame en texte.
        print(lignes.head(3).to_string(index=False))
    else:
        print("Aucune ligne concernée.")

# ---------------------------------------------------------------------------
# Audit de documents.csv
# ---------------------------------------------------------------------------
incidents = pd.read_csv("./data/incidents.csv")
stations = pd.read_csv("./data/stations.csv")
trajets = pd.read_csv("./data/trajets.csv")

incidents_doublons = incidents.duplicated(keep="first")
stations_doublons = stations.duplicated(keep="first")
trajets_doublons = trajets.duplicated(keep="first")
print(incidents_doublons)
print(stations_doublons)
print(trajets_doublons)


# ---------------------------------------------------------------------------
# Audit de stations.csv
# ---------------------------------------------------------------------------

station_id_format= stations["station_id"].str.match(
    r"S([0-9]{2})"
)

nom_vide = stations["nom"].isna()

commune_vide = stations["commune"].isna()

capacite_vide = stations["capacite"].isna()
capacite_inferieure_0 = (
    stations["capacite"].notna()
    & (stations["capacite"] > 0)
)

latitude_vide = stations["latitude"].isna()

longitude_vide = stations["longitude"].isna()

date_mise_en_service_vide = stations["date_mise_en_service"].isna()


# ---------------------------------------------------------------------------
# Audit de trajets.csv
# ---------------------------------------------------------------------------

trajet_id_format= trajets["trajet_id"].str.match(
    r"T([0-9]{6})"
)

velo_id_vide = trajets["velo_id"].isna()
velo_id_format= trajets["velo_id"].str.match(
    r"V([0-9]{4})"
)

depart_horodatage_vide = trajets["depart_horodatage"].isna()
station_depart_vide = trajets["station_depart"].isna()
type_usager_vide = trajets["type_usager"].isna()

usager_ref_format= (
    trajets["usager_ref"].notna()
    & trajets["usager_ref"].str.match(r"U([0-9]{8})")
)


# ---------------------------------------------------------------------------
# Audit de incidents.csv
# ---------------------------------------------------------------------------

incident_id_format= incidents["incident_id"].str.match(
    r"I2026-([0-9]{4})"
)

date_signalement_vide = incidents["date_signalement"].isna()
cible_vide = incidents["cible"].isna()

velo_id_format= (
    incidents["velo_id"].notna()
    & incidents["velo_id"].str.match(r"V([0-9]{4})")
)

type_incident_vide = incidents["type_incident"].isna()
statut_vide = incidents["statut"].isna()

def get_dataframes () :
    df_incidents = pd.read_csv("./data/incidents.csv")
    df_stations = pd.read_csv("./data/stations.csv")
    df_trajets = pd.read_csv("./data/trajets.csv")
    return (df_incidents, df_stations, df_trajets)

def delete_duplicates (incidents, stations, trajets) :
    df_incidents = incidents.drop_duplicates()
    df_stations = stations.drop_duplicates()
    df_trajets = trajets.drop_duplicates()
    return (df_incidents, df_stations, df_trajets)

