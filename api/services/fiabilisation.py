"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""
import pandas as pd
import datetime as dt

df_incidents = pd.read_csv("./data/incidents.csv")
df_stations = pd.read_csv("./data/stations.csv")
df_trajets = pd.read_csv("./data/trajets.csv")

# def afficher_anomalie(code, description, df, masque):
#     # loc[] sélectionne les lignes pour lesquelles le masque vaut True.
#     lignes = df.loc[masque]

#     print(f"\n=== {code} — {description} ===")
#     print(f"Nombre de lignes concernées : {len(lignes)}")

#     if len(lignes) > 0:
#         # head(3) conserve les 3 premières lignes.
#         # to_string() transforme le DataFrame en texte.
#         print(lignes.head(3).to_string(index=False))
#     else:
#         print("Aucune ligne concernée.")

# # ---------------------------------------------------------------------------
# # Audit de documents.csv
# # ---------------------------------------------------------------------------
# incidents = pd.read_csv("./data/incidents.csv")
# stations = pd.read_csv("./data/stations.csv")
# trajets = pd.read_csv("./data/trajets.csv")

# incidents_doublons = incidents.duplicated(keep="first")
# stations_doublons = stations.duplicated(keep="first")
# trajets_doublons = trajets.duplicated(keep="first")
# print(incidents_doublons)
# print(stations_doublons)
# print(trajets_doublons)


# # ---------------------------------------------------------------------------
# # Audit de stations.csv
# # ---------------------------------------------------------------------------

# station_id_format= stations["station_id"].str.match(
#     r"S([0-9]{2})"
# )

# nom_vide = stations["nom"].isna()

# commune_vide = stations["commune"].isna()

# capacite_vide = stations["capacite"].isna()
# capacite_inferieure_0 = (
#     stations["capacite"].notna()
#     & (stations["capacite"] > 0)
# )

# latitude_vide = stations["latitude"].isna()

# longitude_vide = stations["longitude"].isna()

# date_mise_en_service_vide = stations["date_mise_en_service"].isna()


# # ---------------------------------------------------------------------------
# # Audit de trajets.csv
# # ---------------------------------------------------------------------------

# trajet_id_format= trajets["trajet_id"].str.match(
#     r"T([0-9]{6})"
# )

# velo_id_vide = trajets["velo_id"].isna()
# velo_id_format= trajets["velo_id"].str.match(
#     r"V([0-9]{4})"
# )

# depart_horodatage_vide = trajets["depart_horodatage"].isna()
# station_depart_vide = trajets["station_depart"].isna()
# type_usager_vide = trajets["type_usager"].isna()

# usager_ref_format= (
#     trajets["usager_ref"].notna()
#     & trajets["usager_ref"].str.match(r"U([0-9]{8})")
# )


# # ---------------------------------------------------------------------------
# # Audit de incidents.csv
# # ---------------------------------------------------------------------------

# incident_id_format= incidents["incident_id"].str.match(
#     r"I2026-([0-9]{4})"
# )

# date_signalement_vide = incidents["date_signalement"].isna()
# cible_vide = incidents["cible"].isna()

# velo_id_format= (
#     incidents["velo_id"].notna()
#     & incidents["velo_id"].str.match(r"V([0-9]{4})")
# )

# type_incident_vide = incidents["type_incident"].isna()
# statut_vide = incidents["statut"].isna()

# def delete_duplicates (incidents, stations, trajets) :
#     df_incidents = incidents.drop_duplicates()
#     df_stations = stations.drop_duplicates()
#     df_trajets = trajets.drop_duplicates()
#     return (df_incidents, df_stations, df_trajets)

def correction_doublons(df, df_nom):
    df_doublons=df[df.duplicated()] # donnees a supprimer
    df_clean=df[~(df.duplicated())] # donnees a garder
    lignes_invalides=[]
    for index, row in df_doublons.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "toutes",
            "valeur" : "/",
            "motif" : "lignes dupliquées",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def capacite_zero(df):
    df_incorrect=df[df["capacite"] <= 0] # donnees a supprimer
    df_clean=df[df["capacite"] > 0] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "stations.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "capacite",
            "valeur" : row["capacite"],
            "motif" : "capacité invalide : capacité inférieure à 1",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def format_date(df, df_nom, df_date, df_format):
    dates_propres = df.copy()

    date_iso = pd.to_datetime(
        dates_propres[df_date],
        format=df_format,
        errors="coerce",
    )

    date_fr = pd.to_datetime(
        dates_propres[df_date],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )

    dates_normalisees = date_iso.fillna(date_fr)

    dates_propres[df_date] = (
        dates_normalisees.dt.strftime(df_format)
    ) # donnees a garder

    df_clean = df
    df_clean[df_date] = pd.to_datetime(dates_propres[df_date]).dt.date

    df_incorrect = df[(df[df_date] != (df_clean[df_date])) & df[df_date].notna()]
    
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : df_date,
            "valeur" : row[df_date],
            "motif" : "date invalide : mauvais format de date",
            "décision" : "modification"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_dates(df):
    df_incorrect=df[df["date_signalement"] >= df["date_resolution"]] # donnees a supprimer
    df_clean=df[df["date_signalement"] < df["date_resolution"]] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "date_resolution",
            "valeur" : row["date_resolution"],
            "motif" : "durée invalide : date de résolution antérieure à date de signalement",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_cible(df):
    df_incorrect=df[
        (
            (df["cible"] == "velo")
            & ((df["velo_id"].isna()) 
            | (df["station_id"].notna()))
        ) 
        | 
        (
            (df["cible"] == "station")
            & ((df["velo_id"].notna()) 
            | (df["station_id"].isna()))
        )
    ] # donnees a supprimer
    df_clean=df[
        (
            (df["cible"] == "velo") 
            & (df["velo_id"].notna())
            & (df["station_id"].isna())
        ) 
        | 
        (
            (df["cible"] == "station")
            & (df["velo_id"].isna())
            & (df["station_id"].notna())
        )
    ] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "cible",
            "valeur" : row["cible"],
            "motif" : "durée invalide : incident ne correspond pas",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def id_existant(df, df_ref, id, id_ref, df_nom):
    df_incorrect=df[(~df[id].isin(df_ref[id_ref])) & df[id].notna()] # donnees a supprimer
    df_clean=df[df[id].isin(df_ref[id_ref]) | df[id].isna()] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : df_nom,
            "identifiant" : index, # indice de la ligne, 
            "colonne" : id,
            "valeur" : row[id],
            "motif" : "durée invalide : id non existant",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def correlation_usager(df):
    df_incorrect=df[
        (
            (df["type_usager"] == "occasionnel")
            & (df["usager_ref"].notna())
        ) 
        | 
        (
            (df["type_usager"] == "abonne")
            & (df["usager_ref"].isna())
        )
    ] # donnees a supprimer
    df_clean=df[
        (
            (df["type_usager"] == "occasionnel")
            & (df["usager_ref"].isna())
        ) 
        | 
        (
            (df["type_usager"] == "abonne")
            & (df["usager_ref"].notna())
        ) 
    ] # donnees a garder
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "trajets.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "usager_ref",
            "valeur" : row["usager_ref"],
            "motif" : "usager invalide : usager_ref n'est pas valide",
            "décision" : "rejet"
        }
        lignes_invalides.append(ligne_invalide)
    return df_clean, lignes_invalides


def technicien_manquant(df):
    df_incorrect=df[
        (
            (df["statut"] == ("resolu" or "en_cours"))
            & df["technicien"].isna()
        )
    ]
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "incidents.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "technicien",
            "valeur" : row["technicien"],
            "motif" : "technicien invalide : technicien manquant après résolution",
            "décision" : "gardé"
        }
        lignes_invalides.append(ligne_invalide)
    return lignes_invalides


def station_manquante(df):
    df_incorrect=df[df["station_arrivee"].isna()]
    lignes_invalides=[]
    for index, row in df_incorrect.iterrows(): # index : indice en cours, row : dictionnaire representant la ligne en cours
        ligne_invalide={
            "fichier_source" : "trajets.csv",
            "identifiant" : index, # indice de la ligne, 
            "colonne" : "station_arrivee",
            "valeur" : row["station_arrivee"],
            "motif" : "station d'arrivée invalide : station manquante",
            "décision" : "gardé"
        }
        lignes_invalides.append(ligne_invalide)
    return lignes_invalides

oe, nan = format_date(df_incidents, "incidents.csv", "date_resolution", "%Y-%m-%d %H:%M")

print(nan)